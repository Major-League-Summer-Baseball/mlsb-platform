import csv
import click
import logging
from api.extensions import DB
from api.model import Sponsor, Team


@click.command('import-season')
@click.argument('year')
@click.argument('sponsor_csv')
@click.argument('team_standings_csv')
@click.argument('homeruns_csv')
@click.argument('special_singles_csv')
def import_season_command(
    year, sponsor_csv, team_standings_csv, homeruns_csv, special_singles_csv
):
    """Import a season from a list of csv files

        year: the year the season occurred

        sponsor_csv: is the a csv file with the sponsors for the season
        
        team_standings_csv: is a csv file of the team standings with their:
            wins, loses, ties, runs for, runs against, espys
        
        homeruns_csv: is a csv file with player's name, email and their season homerun total
        
        special_singles_csv: is a csv file with player's  name, email and their season special singles total
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    sponsor_map = setup_sponsor_map(sponsor_csv, logger)
    logger.info(sponsor_map)
    team_map = create_teams(team_standings_csv, sponsor_map, logger)


def create_teams(team_csv: str, sponsors_map: dict[str, 'Sponsor'], logger) -> dict[str, 'Team']:
    """Create the various teams"""
    teams = {}
    with open(team_csv, newline='') as teamfile:
        reader = csv.DictReader(teamfile)
        for row in reader:
            print(row)


def setup_sponsor_map(sponsor_csv: str, logger) -> dict[str, 'Sponsor']:
    """Parse out the sponsors and lookup/create them."""
    sponsors = {}
    with open(sponsor_csv, newline='') as sponsorfile:
        reader = csv.DictReader(sponsorfile)
        for row in reader:
            sponsor_name = row['sponsor-name'].strip()
            print(sponsor_name)
            sponsor = DB.session.query(Sponsor).filter(Sponsor.name == sponsor_name).one()
            if not sponsor:
                sponsor = Sponsor(sponsor_name, active=False)
                DB.session.add(Sponsor(sponsor_name, active=False))
                logger.info(f'Added sponsor {sponsor_name}')
            sponsors[sponsor_name] = sponsor
    return sponsors
