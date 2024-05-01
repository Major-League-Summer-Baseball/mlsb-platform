from api.extensions import DB
from datetime import date


class Fun(DB.Model):
    """
        A class used to store the amount of fun had by all.
        Columns:
            id: the unique id
            year: the year the fun count is for
            count: the total count for the year
    """
    id = DB.Column(DB.Integer, primary_key=True)
    year = DB.Column(DB.Integer)
    count = DB.Column(DB.Integer)

    def __init__(self, year: date = date.today().year, count: int = 0):
        """ Fun constructor. """
        self.year = year
        self.count = count

    def update(self, count=None, year=None):
        """Update an existing fun count."""
        if count is not None:
            self.count = count
        if year is not None:
            self.year = year

    def increment(self, change):
        """Increment the fun count.

        Parameters:
            change: the amount the fun count has changed by (int)
        """
        self.count += change

    def json(self):
        """Returns a jsonserializable object."""
        return {
            'fun_id': self.id,
            'year': self.year,
            'count': self.count
        }
