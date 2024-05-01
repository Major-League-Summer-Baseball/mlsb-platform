
from api.errors import HaveLeagueRequestException, InvalidField, \
    TeamDoesNotExist
from api.extensions import DB
from api.models.player import Player
from api.models.shared import validate
from api.models.team import Team
from api.validators import gender_validator, string_validator
from sqlalchemy import and_, func


class JoinLeagueRequest(DB.Model):
    """
        A class used to store requests to join a league.
        Columns:
            team_id: the team they want to join
            name: the name they want to use
            email: the email from the Oauth provider
            pending: whether waiting for the outcome of the request
    """
    id = DB.Column(DB.Integer, primary_key=True)
    team_id = DB.Column(DB.Integer, DB.ForeignKey(Team.id), nullable=False)
    team = DB.relationship(Team)
    email = DB.Column(DB.String(120), nullable=False)
    name = DB.Column(DB.String(120), nullable=False)
    pending = DB.Column(DB.Boolean)
    gender = DB.Column(DB.String(1))

    def __init__(self, email: str, name: str, team: 'Team', gender: str):
        validate(
            gender,
            gender_validator,
            InvalidField(payload={'details': "Player League Request - gender"})
        )
        validate(
            email,
            string_validator,
            InvalidField(payload={"details": "Player League Request - email"})
        )
        validate(
            name,
            string_validator,
            InvalidField(payload={"details": "Player League Request - name"})
        )
        validate(
            -1 if team is None or not isinstance(team, Team) else team.id,
            lambda id: Team.does_team_exist(id),
            TeamDoesNotExist(payload={"details": "Given team does not exist"})
        )

        self.email = Player.normalize_email(email)
        self.name = name
        self.team_id = team.id
        self.pending = True
        self.gender = gender.lower()

    def accept_request(self) -> 'Player':
        """Accept the request and add the player to the team"""
        # create a player if they do not exit already
        if not self.pending:
            raise HaveLeagueRequestException(
                payload={"details": "Request already submitted"}
            )

        player = Player.find_by_email(self.email)
        if player is None:
            player = Player(self.name, self.email, gender=self.gender)
            DB.session.add(player)
            DB.session.commit()
        self.pending = False
        team = Team.query.get(self.team_id)
        team.insert_player(player.id)
        DB.session.commit()
        return player

    def decline_request(self) -> None:
        """Decline the request."""
        self.pending = False
        DB.session.commit()

    def json(self) -> dict:
        """Get a json version of the model"""
        team = (None if self.team_id is None
                else Team.query.get(self.team_id).json())
        return {
            "team": team,
            "email": self.email,
            "id": self.id,
            "pending": self.pending,
            "player_name": self.name,
            "gender": self.gender
        }

    @classmethod
    def create_request(
        cls,
        player_name: str,
        player_email: str,
        gender: str,
        team_id: int,
    ) -> 'JoinLeagueRequest':
        """Create a join league request"""
        pending_request = JoinLeagueRequest.query.filter(
            func.lower(JoinLeagueRequest.email) == player_email.lower()
        ).first()
        if pending_request is not None:
            raise HaveLeagueRequestException(
                payload={'detail': "Already pending request"}
            )

        return JoinLeagueRequest(
            player_email, player_name, Team.query.get(team_id), gender
        )

    @classmethod
    def find_request(cls, player_email: str) -> 'JoinLeagueRequest':
        """Find a pending request for the given email"""
        return JoinLeagueRequest.query.filter(
            and_(
                JoinLeagueRequest.email == player_email,
                JoinLeagueRequest.pending == True
            )
        ).first()
