from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy import and_, func, or_, not_
from werkzeug.security import generate_password_hash, check_password_hash
from api.extensions import DB
from api.errors import InvalidField, NonUniqueEmail
from api.helper import normalize_string
from api.validators import string_validator, gender_validator
from api.models.shared import notNone, validate
from api.variables import PLAYER_PAGE_SIZE, UNASSIGNED_EMAIL


class Player(UserMixin, DB.Model):
    """
    A class that stores a player's information.
        id: the player's unique id
        name: the name of the player
        email: the unique player's email
        gender: the player's gender
        password: the password for the player
        team: the teams the player plays for
        active: a boolean to say whether the player is active
                currently or not (retired or not)
        kik: the kik user name associated with the player
    """
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80))
    email = DB.Column(DB.String(120), unique=True)
    gender = DB.Column(DB.String(1))
    password = DB.Column(DB.String(120))
    bats = DB.relationship(
        'Bat', backref='player', lazy='dynamic'
    )
    team = DB.relationship(
        'Team', backref='player', lazy='dynamic'
    )
    active = DB.Column(DB.Boolean)
    kik = DB.Column(DB.String(120))
    is_convenor = DB.Column(DB.Boolean, default=False)

    def __init__(
        self,
        name: str,
        email: str,
        gender: str = "m",
        password: str = "default",
        active: bool = True
    ):
        """The constructor.

            Raises:
                InvalidField
                NonUniqueEmail
        """
        validate(
            email,
            string_validator,
            InvalidField(payload={'details': "Player - email"})
        )
        validate(
            Player.normalize_email(email),
            lambda email: Player.is_email_unique(email),
            NonUniqueEmail(payload={'details': email})
        )
        validate(
            name,
            string_validator,
            InvalidField(payload={"details": "Player - name"})
        )
        validate(
            gender,
            gender_validator,
            InvalidField(payload={'details': "Player - gender"})
        )
        self.is_convenor = False
        self.__update(
            name=name,
            email=email,
            gender=gender,
            password=password,
            active=active
        )

    def __update(
        self,
        name: str,
        email: str,
        gender: str,
        password: str,
        active: bool
    ):
        self.name = notNone(name, self.name)
        self.email = Player.normalize_email(notNone(email, self.email))
        self.gender = Player.normalize_gender(notNone(gender, self.gender))
        self.set_password(notNone(password, self.password))
        self.active = notNone(active, self.active)

    def update(
        self,
        name: str = None,
        email: str = None,
        gender: str = None,
        password: str = None,
        active: bool = None
    ) -> None:
        """Update an existing player

            Parameters:
                name: the name of the player
                email: the unique email of the player
                gender: the gender of the player
                password: the password of the player
            Raises:
                InvalidField
                NonUniqueEmail
        """
        validate(
            email,
            string_validator,
            InvalidField(payload={'details': "Player - email"}),
            required=False
        )
        validate(
            None if email is None else Player.normalize_email(email),
            lambda email: Player.is_email_unique(email),
            NonUniqueEmail(payload={'details': email}),
            required=False
        )
        validate(
            name,
            string_validator,
            InvalidField(payload={"details": "Player - name"}),
            required=False
        )
        validate(
            gender,
            gender_validator,
            InvalidField(payload={'details': "Player - gender"}),
            required=False
        )

        self.__update(
            name=name,
            email=email,
            gender=gender,
            password=password,
            active=active
        )

    def set_password(self, password: str) -> None:
        """Update a player's password.

            Parameters:
                password: the player's new password (str)
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check a player's password.

            Parameters:
                password: attempted password (str)
            Returns:
                True passwords match
                False otherwise
        """
        return check_password_hash(self.password, password)

    def make_convenor(self) -> None:
        """Make the player a convenor."""
        self.is_convenor = True

    def remove_convenor(self) -> None:
        """The player is no longer a convenor."""
        self.is_convenor = False

    def __repr__(self) -> str:
        """Return the string representation of the player."""
        return self.name

    def update_kik(self, kik: str) -> None:
        """Update the player's kik profile."""
        self.kik = kik

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {
            "player_id": self.id,
            "player_name": self.name,
            "gender": self.gender,
            "active": self.active
        }

    def admin_json(self) -> dict:
        """Returns a jsonserializable object."""
        return {
            "player_id": self.id,
            "player_name": self.name,
            "gender": self.gender,
            "email": self.email,
            "active": self.active,
            "is_convenor": self.is_convenor
        }

    def activate(self) -> None:
        """Activate the player."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate the player (retire them)."""
        self.active = False

    @classmethod
    def does_player_exist(cls, player_id: str) -> bool:
        return Player.query.get(player_id) is not None

    @classmethod
    def normalize_email(cls, email: str) -> str:
        """Return a normalized email."""
        return normalize_string(email)

    @classmethod
    def normalize_gender(cls, gender: str) -> str:
        """Return a normalized email."""
        return normalize_string(gender)

    @classmethod
    def find_by_email(cls, email: str) -> "Player":
        """Returns the player with the given email."""
        if email is None:
            return None
        return Player.query.filter(
            func.lower(Player.email) == Player.normalize_email(email)
        ).first()

    @classmethod
    def search_player(
        cls,
        search_phrase: str,
        page_size: int = PLAYER_PAGE_SIZE
    ) -> list["Player"]:
        """Returns all players who meet the search phrase"""
        return Player.query.filter(
            and_(
                or_(
                    func.lower(Player.email).contains(search_phrase.lower()),
                    func.lower(Player.name).contains(search_phrase.lower())
                ),
                not_(Player.email.ilike(UNASSIGNED_EMAIL))
            )
        ).limit(page_size).all()

    @classmethod
    def get_unassigned_player(cls) -> "Player":
        """Returns the player used for unassigned bats"""
        return Player.query.filter(Player.email.ilike(UNASSIGNED_EMAIL)).first()

    @classmethod
    def is_email_unique(cls, email: str) -> bool:
        """Returns whether the email is unique and available."""
        return Player.find_by_email(email) is None


class OAuth(OAuthConsumerMixin, DB.Model):
    """A model for storing information about oauth"""
    provider_user_id = DB.Column(DB.String(256), unique=True, nullable=False)
    player_id = DB.Column(DB.Integer, DB.ForeignKey(Player.id), nullable=False)
    player = DB.relationship(Player)
