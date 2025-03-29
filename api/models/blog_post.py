from datetime import datetime
from api.extensions import DB
from api.errors import ImageDoesNotExist, InvalidField, PlayerDoesNotExist
from api.models.image import Image
from api.validators import date_validator, string_validator, time_validator
from api.models.shared import convert_date, notNone, split_datetime, validate
from api.models.player import Player


class BlogPost(DB.Model):
    """A class used to store a website blog post"""
    id = DB.Column(DB.Integer, primary_key=True)
    author_id = DB.Column(DB.Integer, DB.ForeignKey('player.id'), nullable=False)
    image_id = DB.Column(DB.Integer, DB.ForeignKey('image.id'), nullable=True)
    html = DB.Column(DB.Text(), nullable=False)
    summary = DB.Column(DB.Text(), nullable=False)
    title = DB.Column(DB.Text(), nullable=False)
    date = DB.Column(DB.DateTime, nullable=False)
    author = DB.relationship('Player', lazy=True)
    image = DB.relationship('Image', lazy=True)

    def __init__(
        self,
        author_id: int,
        title: str,
        summary: str,
        html: str,
        image_id: int = None,
        time: str = None,
        date: str = None
    ):
        """The constructor

            Raises:
                PlayerDoesNotExist
                InvalidField
        """
        validate(
            author_id,
            lambda id: Player.does_player_exist(author_id),
            PlayerDoesNotExist(payload={"details": author_id})
        )
        validate(
            html,
            string_validator,
            InvalidField(payload={"details": "Blog Post - html"})
        )
        validate(
            title,
            string_validator,
            InvalidField(payload={"details": "Blog Post - title"})
        )
        validate(
            image_id,
            lambda id: Image.does_image_exist(id),
            ImageDoesNotExist(payload={'details': image_id}),
            required=False
        )
        validate(
            summary,
            string_validator,
            InvalidField(payload={"details": "Blog Post - html"})
        )
        validate(
            date,
            date_validator,
            InvalidField(payload={'details': "Blog Post - date"}),
            required=False
        )
        validate(
            time,
            time_validator,
            InvalidField(payload={'details': "Blog Post - time"}),
            required=False
        )
        (current_date, current_time) = split_datetime(datetime.today())
        self.__update(
            author_id=author_id,
            title=title,
            summary=summary,
            html=html,
            image_id=image_id,
            time=notNone(time, current_time),
            date=notNone(date, current_date),
        )

    def __update(
        self,
        author_id: int,
        title: str,
        summary: str,
        html: str,
        image_id: int,
        time: str,
        date: str
    ):
        self.author_id = notNone(author_id, self.author_id)
        self.title = notNone(title, self.title)
        self.summary = notNone(summary, self.summary)
        self.html = notNone(html, self.html)
        self.image_id = notNone(image_id, self.image_id)
        self.date = convert_date(date, time)

    def update(
        self,
        author_id: int = None,
        title: str = None,
        summary: str = None,
        html: str = None,
        image_id: int = None,
        time: str = None,
        date: str = None
    ):
        validate(
            author_id,
            lambda id: Player.does_player_exist(author_id),
            PlayerDoesNotExist(payload={"details": author_id}),
            required=False
        )
        validate(
            title,
            string_validator,
            InvalidField(payload={"details": "Blog Post - title"}),
            required=False
        )
        validate(
            summary,
            string_validator,
            InvalidField(payload={"details": "Blog Post - summary"}),
            required=False
        )
        validate(
            html,
            string_validator,
            InvalidField(payload={"details": "Blog Post - html"}),
            required=False
        )
        validate(
            image_id,
            lambda id: Image.does_image_exist(id),
            ImageDoesNotExist(payload={'details': image_id}),
            required=False
        )
        validate(
            date,
            date_validator,
            InvalidField(payload={'details': "Blog Post - date"}),
            required=False
        )
        validate(
            time,
            time_validator,
            InvalidField(payload={'details': "Blog Post - time"}),
            required=False
        )
        (current_date, current_time) = split_datetime(self.date)
        self.__update(
            author_id=author_id,
            title=title,
            summary=summary,
            html=html,
            image_id=image_id,
            time=notNone(time, current_time),
            date=notNone(date, current_date)
        )

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        date, time = split_datetime(self.date)
        return {
            'author': self.author.json(),
            'author_id': self.author_id,
            'date': date,
            'blog_post_id': self.id,
            'html': self.html,
            'summary': self.summary,
            'time': time,
            'title': self.title,
            'image_id': self.image_id,
            'image': None if self.image_id is None else self.image.json()
        }
