"""Extensions module. Each extension is initialized in the app factory."""
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_login import LoginManager
from api.config import Config


DB = SQLAlchemy()
cache = Cache(config=Config.REDIS_CACHE)
login_manager = LoginManager()
tailsman = Talisman()
