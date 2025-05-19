import csv
import click
import logging
import math
from sqlalchemy import func
from sqlalchemy.sql.expression import and_
from api.extensions import DB
from api.model import Sponsor, Team, League, Player, Division, Game, Bat
from typing import List, TypedDict
from api.models.espys import Espys
from api.variables import UNASSIGNED_EMAIL, UNASSIGNED_TEAM


class TeamGamesScore(TypedDict):
    homeruns: List[int]
    singles: List[int]
    score: int
    other_score: int


class PlayerRecord(TypedDict):
    player: Player
    homeruns: int
    singles: int


class TeamRecord(TypedDict):
    wins: int
    losses: int
    ties: int
    runs_for: int
    runs_allowed: int
    espys: int


class TeamInfo(TypedDict):
    team: Team
    record: TeamRecord
    homeruns: List[PlayerRecord]
    singles: List[PlayerRecord]


def normalize_team_name(team_name: str) -> str:
    """Normalize team name so easier to compare them."""
    return str(team_name).strip().lower().replace("'", "").replace(" ", "")


def cleanup_value(value: str) -> str:
    """Cleanup a given user input"""
    return value.strip()


@click.command('import-season')
@click.argument('league_name')
@click.argument('division_name')
@click.argument('year')
@click.argument('sponsor_csv')
@click.argument('team_standings_csv')
@click.argument('homeruns_csv')
@click.argument('special_singles_csv')
def import_season_command(
    league_name,
    division_name,
    year,
    sponsor_csv,
    team_standings_csv,
    homeruns_csv,
    special_singles_csv
):
    """Import a season from a list of csv files.

        league_name: the name of the league

        division_name: the name of the division

        year: the year the season occurred

        sponsor_csv: is the a csv file with the sponsors for the season

        team_standings_csv: is a csv file of the team standings with their:
            wins, loses, ties, runs for, runs against, espys

        homeruns_csv: is a csv file with player's name, email and their season homerun total

        special_singles_csv: is a csv file with player's  name, email and their season special singles total
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)

    league = DB.session.query(League).filter(
        func.lower(League.name) == func.lower(league_name)
    ).first()
    if league is None:
        logger.error(f'Unable to find league {league_name}')
        return

    division = DB.session.query(Division).filter(
        func.lower(Division.name) == func.lower(division_name)
    ).first()
    if division is None:
        logger.error(f'Unable to find division {division_name}')
        return

    sponsor_map = setup_sponsor_map(sponsor_csv, logger)
    team_map = set_teams_map(
        year, league.id, team_standings_csv, sponsor_map, logger
    )
    add_players_to_team__map(team_map, homeruns_csv, special_singles_csv, logger)
    save_team_record(team_map, year, league, division, logger)


def save_team_record(
    team_map: dict[str, TeamInfo], year: int, league: League, division: Division, logger
):
    """Save the team record and player records by adding games and scores."""

    unassigned_player = DB.session.query(Player).filter(
        Player.email.ilike(UNASSIGNED_EMAIL)
    ).first()
    if unassigned_player is None:
        logger.error('Cannot find un-assigned player')
        exit(1)

    unknown_team = DB.session.query(Team).filter(
        and_(
            Team.year == year,
            Team.color == UNASSIGNED_TEAM
        )
    ).first()
    if unknown_team is None:
        unknown_team = Team(UNASSIGNED_TEAM, year=year, league_id=league.id)
        DB.session.add(unknown_team)
        DB.session.commit()

    def add_game_score(
        index: int,
        team_id: int,
        score: TeamGamesScore,
    ):
        game_date = f'{year}-05-{index}'
        game = Game(game_date, '12:00', team_id, unknown_team.id, league.id, division.id)
        DB.session.add(game)
        DB.session.commit()
        for player_id in score['singles']:
            bat = Bat(player_id, team_id, game.id, 'ss')
            DB.session.add(bat)
        for player_id in score['homeruns']:
            bat = Bat(player_id, team_id, game.id, 'hr', rbi=1)
            DB.session.add(bat)
        for unassigned_run in range(score['score'] - len(score['homeruns'])):
            bat = Bat(unassigned_player.id, team_id, game.id, 's', rbi=1)
            DB.session.add(bat)
        for unassigned_run in range(score['other_score']):
            bat = Bat(unassigned_player.id, unknown_team.id, game.id, 's', rbi=1)
            DB.session.add(bat)
        DB.session.commit()
        return

    for team in team_map.values():
        team_season = create_team_season(team, logger)
        for index, game in enumerate(team_season):
            add_game_score(index + 1, team['team'].id, game)
        logger.info(team_season)
        logger.info(f'Add games for {team} and hr/ss for its players')
    return


def add_players_to_team__map(
    team_map: dict[str, TeamInfo],
    homeruns_csv: str,
    special_singles_csv: str,
    logger
):
    logger.info(team_map)
    """Find/Create the various players."""
    def parse_file(file, stat, gender):
        with open(file, newline='') as stat_file:
            reader = csv.DictReader(stat_file)
            for row in reader:
                team_name = cleanup_value(row['team-name'])
                email = cleanup_value(row['email'])
                team = team_map.get(normalize_team_name(team_name))
                if team is None:
                    logger.error(f'Unable to find {email} team {team_name}')
                    exit(1)
                player = DB.session.query(Player).filter(
                    func.lower(Player.email) == func.lower(email)
                ).first()
                if player is None:
                    player = Player(
                        cleanup_value(row['player-name']),
                        email,
                        gender=gender
                    )
                    DB.session.add(player)
                    DB.session.commit()
                    logger.info(f'Added player {player}')
                team[stat].append({
                    'player': player,
                    'homeruns': int(row.get('hr', 0)),
                    'singles': int(row.get('ss', 0))
                })
                team['team'].insert_player(player.id)
                DB.session.commit()
    parse_file(homeruns_csv, 'homeruns', 'm')
    parse_file(special_singles_csv, 'singles', 'f')


def set_teams_map(
    year: int,
    league_id: int,
    team_csv: str,
    sponsors_map: dict[str, 'Sponsor'],
    logger
) -> dict[str, TeamInfo]:
    """Find/Create the various teams."""
    teams = {}
    with open(team_csv, newline='') as teamfile:
        reader = csv.DictReader(teamfile)
        for row in reader:
            sponsor = cleanup_value(row['sponsor'])
            team_sponsor = sponsors_map.get(sponsor.lower())
            if team_sponsor is None:
                logger.error(f'Unable to find teams sponsor {sponsor}')
                exit(1)
            # see if team already exists
            team_color = cleanup_value(row['color'])
            team = DB.session.query(Team).filter(
                and_(
                    and_(
                        Team.sponsor_id == team_sponsor.id,
                        Team.year == year
                    ),
                    func.lower(Team.color) == func.lower(team_color)
                )
            ).first()
            if not team:
                team = Team(
                    color=team_color,
                    sponsor_id=team_sponsor.id,
                    league_id=league_id,
                    year=year
                )
                DB.session.add(team)
                DB.session.commit()
                logger.info(f'Created team {team}')
            espys = int(row['espys'])
            if team.espys_total < espys:
                DB.session.add(
                    Espys(
                        team.id,
                        points=espys,
                        description='Season total',
                        date=f"{year}-05-01"
                    )
                )

            teams[normalize_team_name(team)] = {
                'team': team,
                'homeruns': [],
                'singles': [],
                'record': {
                    'wins': int(row['wins']),
                    'ties': int(row['ties']),
                    'losses': int(row['losses']),
                    'runs_for': int(row['runs-for']),
                    'runs_allowed': int(row['runs-allowed']),
                    'espys': int(row['espys']),
                }
            }
    logger.info('Parsed Teams data')
    return teams


def setup_sponsor_map(sponsor_csv: str, logger) -> dict[str, 'Sponsor']:
    """Parse out the sponsors and lookup/create them."""
    sponsors = {}
    with open(sponsor_csv, newline='') as sponsorfile:
        reader = csv.DictReader(sponsorfile)
        for row in reader:
            sponsor_name = cleanup_value(row['sponsor-name'])
            sponsor = DB.session.query(Sponsor).filter(
                func.lower(Sponsor.name) == func.lower(sponsor_name)
            ).first()
            if not sponsor:
                sponsor = Sponsor(sponsor_name, active=False)
                DB.session.add(Sponsor(sponsor_name, active=False))
                logger.info(f'Added sponsor {sponsor_name}')
            sponsors[sponsor_name.lower()] = sponsor
    DB.session.commit()
    logger.info('Parsed sponsors data')
    return sponsors


def create_team_season(team: TeamInfo, logger) -> list[TeamGamesScore]:
    """Take the team record and create games scores"""
    losses = team['record']['losses']
    wins = team['record']['wins']
    ties = team['record']['ties']
    total_games = losses + wins + ties
    runs_for = team['record']['runs_for']
    runs_against = team['record']['runs_allowed']
    average_run_for = math.floor(runs_for / total_games)
    average_run_against = math.floor(runs_against / total_games)
    game_scores: List[TeamGamesScore] = []

    # valid the date
    if wins == 0 and average_run_against < average_run_for:
        logger.error('Team didnt win so cannot have more runs for than against')
        raise Exception('Team didnt win so cannot have more runs for than against')
    if losses == 0 and average_run_for < average_run_against:
        logger.error('Team didnt lose cannot have more runs against for than for')
        raise Exception('Team didnt win cannot have more runs against than for')

    # setup the ties
    tie_score = min(average_run_for, average_run_against)
    for game in range(ties):
        runs_for -= tie_score
        runs_against -= tie_score
        game_scores.append({
            'homeruns': [],
            'singles': [],
            'score': tie_score,
            'other_score': tie_score,
        })

    # evenly distribute rest of the scores
    for game in range(total_games - ties):
        runs_for -= average_run_for
        runs_against -= average_run_against
        game_scores.append({
            'homeruns': [],
            'singles': [],
            'score': average_run_for,
            'other_score': average_run_against,
        })

    # ties at front, wins in middle, losses at end
    win_indices = [index for index in range(ties, wins + ties)]
    loss_indices = [index for index in range(wins + ties, total_games)]

    # evenly distribute the remaining runs
    run_for_indices = win_indices if wins > 0 else loss_indices
    run_against_indices = loss_indices if losses > 0 else win_indices
    index = 0
    while runs_for > 0:
        game_scores[run_for_indices[index]]['score'] += 1
        index = (index + 1) % len(run_for_indices)
        runs_for -= 1
    index = 0
    while runs_against > 0:
        game_scores[run_against_indices[index]]['other_score'] += 1
        index = (index + 1) % len(run_against_indices)
        runs_against -= 1

    if team['record']['runs_for'] >= team['record']['runs_allowed'] and len(loss_indices) > 0:
        # wins should be setup properly so handle losses
        win_index = 0
        winning_game = game_scores[win_indices[win_index]]
        for loss_index in loss_indices:
            losing_game = game_scores[loss_index]
            while losing_game['score'] >= losing_game['other_score']:
                while winning_game['other_score'] == 0:
                    win_index += 1
                    if win_index > len(win_indices):
                        logger.error('Not enough run against for losses')
                        raise Exception('Not enough run against for losses')
                    winning_game = game_scores[win_indices[win_index]]
                losing_game['other_score'] += 1
                winning_game['other_score'] -= 1
    elif team['record']['runs_for'] <= team['record']['runs_allowed'] and len(win_indices) > 0:
        # losses should be setup properly so handle wins
        loss_index = 0
        losing_game = game_scores[loss_indices[loss_index]]
        for win_index in win_indices:
            winning_game = game_scores[win_index]
            while winning_game['score'] <= winning_game['other_score']:
                while losing_game['score'] == 0:
                    loss_index += 1
                    if loss_index >= len(loss_indices):
                        logger.error('Not enough run for for losses')
                        raise Exception('Not enough run for for losses')
                    losing_game = game_scores[loss_indices[loss_index]]
                winning_game['score'] += 1
                losing_game['score'] -= 1

    # distribute singles across games
    for player in team['singles']:
        singles = player['singles']
        game_index = 0
        while singles > 0:
            singles -= 1
            game_scores[game_index]['singles'].append(player['player'].id)
            game_index = (game_index + 1) % len(game_scores)
    # distribute homeruns acrss games
    for player in team['homeruns']:
        homeruns = player['homeruns']
        game_index = 0
        while homeruns > 0:
            if (len(game_scores[game_index]['homeruns']) <= game_scores[game_index]['score']):
                homeruns -= 1
                game_scores[game_index]['homeruns'].append(player['player'].id)
            elif all(
                game_scores[i]['score'] == len(game_scores[i]['homeruns'])
                for i in range(len(game_scores))
            ):
                team_name = str(team['team'])
                logger.error(f'Homeruns exceed runs for team {team_name}')
                raise Exception(f'Homeruns exceed runs for {team_name}')
            game_index = (game_index + 1) % len(game_scores)
    return game_scores
