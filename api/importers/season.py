import csv
import click

@click.command('import-season')
@click.argument('sponsor_csv')
@click.argument('team_standings_csv')
@click.argument('homeruns_csv')
@click.argument('special_singles_csv')
def import_season_command(
    sponsor_csv, team_standing_csv, homeruns_csv, special_singles_csv
):
    """Import a season from a list of csv files
    
        sponsor_csv: is the a csv file with the sponsors for the season
        
        team_standings_csv: is a csv file of the team standings with their:
            wins, loses, ties, runs for, runs against, espys
        
        homeruns_csv: is a csv file with player's name, email and their season homerun total
        
        special_singles_csv: is a csv file with player's  name, email and their season special singles total
    """
    sponsors = []
    with open(sponsor_csv, newLine='') as sponsorfile:
        reader = csv.DictReader(sponsorfile)
        for row in reader:
            print(row)
