"""Initialize Flask app."""

from flask import Flask, render_template
# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from games.domainmodel.model import Game
from games.adapters import database_repository, repository_populate, memory_repository
from games.adapters.orm import metadata, map_model_to_tables
import games.adapters.repository as repo  # Import repo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool
from pathlib import Path
import os



# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
# def create_some_game():
#     some_game = Game(1, "Call of Duty® 4: Modern Warfare®")
#     some_game.release_date = "Nov 12, 2007"
#     some_game.price = 9.99
#     some_game.description = "The new action-thriller from the award-winning team at Infinity Ward, the creators of " \
#                             "the Call of Duty® series, delivers the most intense and cinematic action experience ever. "
#     some_game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
#     return some_game
#

def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'
    #app.secret_key = os.getenv("SECRET_KEY")
    if test_config is not None:
        app.config.from_mapping(test_config)

    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = memory_repository.MemoryRepository()
        database_mode = False
        repository_populate.populate(repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass = NullPool, echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)
        if len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())
            map_model_to_tables()
            repository_populate.populate(repo.repo_instance)
            print("REPOPULATING DATABASE... FINISHED")
        else:
            map_model_to_tables()



    with app.app_context():
        from .browse import browse_bp
        app.register_blueprint(browse_bp.browse_blueprint)
        from .home import home
        app.register_blueprint(home.home_blueprint)
        from .description import description
        app.register_blueprint(description.description_blueprint)
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)
        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)
        from .wishlist import wishlist
        app.register_blueprint(wishlist.wishlist_blueprint)
        #from .games import games
        #app.register_blueprint(games.games_blueprint)
    return app

"""    @app.route('/')
    def home():
        some_game = create_some_game()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('home.html', game=some_game)

    @app.route('/description')
    def description():
        return render_template('gameDescription.html')

    @app.route('/games')
    def show_games():
        return render_template('games.html')"""


