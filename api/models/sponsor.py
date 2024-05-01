from api.extensions import DB
from api.errors import InvalidField
from api.validators import boolean_validator, string_validator
from api.models.shared import notNone, validate


class Sponsor(DB.Model):
    """
    A class that stores information about a sponsor.
    Columns:
        id: the sponsor's unique id
        name: the name of the sponsor
        teams: the teams the sponsor is associated with
        description: a description of the sponsor
        link: a link to the sponsor's website or facebook
        active: a boolean telling whether the sponsor
                is currently sponsoring a team
        espys: all the espys transaction associated with the sponsor
    """
    __tablename__ = 'sponsor'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(120), unique=True)
    teams = DB.relationship(
        'Team', backref='sponsor', lazy='dynamic'
    )
    description = DB.Column(DB.String(200))
    link = DB.Column(DB.String(100))
    active = DB.Column(DB.Boolean)
    espys = DB.relationship('Espys', backref='sponsor', lazy='dynamic')
    nickname = DB.Column(DB.String(100))

    def __init__(
        self,
        name: str,
        link: str = None,
        description: str = None,
        active: bool = True,
        nickname: str = None
    ):
        """The constructor.

           Raises:
               InvalidField
        """
        validate(
            name,
            string_validator,
            InvalidField(payload={'details': "Sponsor - name"})
        )
        validate(
            nickname,
            string_validator,
            InvalidField(payload={'details': "Sponsor - nickname"}),
            required=False
        )
        validate(
            link,
            string_validator,
            InvalidField(payload={'details': "Sponsor - link"})
        )
        validate(
            description,
            string_validator,
            InvalidField(payload={'details': "Sponsor - description"})
        )
        validate(
            active,
            boolean_validator,
            InvalidField(payload={'details': "Sponsor - active"})
        )
        self.__update(
            name=name,
            description=description,
            link=link,
            active=active,
            nickname=nickname if nickname is not None else name
        )

    def __update(
        self,
        name: str,
        link: str,
        description: str,
        active: bool,
        nickname: str
    ):
        self.name = notNone(name, self.name)
        self.description = notNone(description, self.description)
        self.link = notNone(link, self.link)
        self.active = notNone(active, self.active)
        self.nickname = notNone(nickname, self.nickname)

    def __repr__(self) -> str:
        """Returns the string representation of the sponsor."""
        return self.name if self.name is not None else ""

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {'sponsor_id': self.id,
                'sponsor_name': self.name,
                'link': self.link,
                'description': self.description,
                'active': self.active}

    def update(
        self,
        name: str = None,
        link: str = None,
        description: str = None,
        active: bool = None,
        nickname: str = None
    ) -> None:
        """Updates an existing sponsor.

           Raises:
               InvalidField
        """
        validate(
            name,
            string_validator,
            InvalidField(payload={'details': "Sponsor - name"}),
            required=False
        )
        validate(
            nickname,
            string_validator,
            InvalidField(payload={'details': "Sponsor - nickname"}),
            required=False
        )
        validate(
            link,
            string_validator,
            InvalidField(payload={'details': "Sponsor - link"}),
            required=False
        )
        validate(
            description,
            string_validator,
            InvalidField(payload={'details': "Sponsor - description"}),
            required=False
        )
        validate(
            active,
            boolean_validator,
            InvalidField(payload={'details': "Sponsor - active"}),
            required=False
        )
        has_nickname = self.name != self.nickname
        self.__update(
            name=name,
            description=description,
            link=link,
            active=active,
            nickname=nickname if nickname is not None else (
                name if not has_nickname else self.nickname
            )
        )

    def activate(self) -> None:
        """Activate a sponsor (they are back baby)."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate a sponsor (they are no longer sponsoring). """
        self.active = False

    @classmethod
    def does_sponsor_exist(cls, sponsor_id: str) -> bool:
        return Sponsor.query.get(sponsor_id) is not None
