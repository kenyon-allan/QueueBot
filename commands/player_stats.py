from typing import Dict, Self
import trueskill
from sqlalchemy import Engine, Float, create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

ENGINE: Engine = create_engine(f"sqlite:///{os.getenv('DB_PATH')}", echo=True)
Base: DeclarativeMeta = declarative_base()


class PlayerData(Base):
    """Database model class to represent a player's statistics."""

    __tablename__ = "players"

    user_id = Column(Integer, primary_key=True, nullable=False)

    # Rating info
    tank_mu = Column(Float, nullable=False, default=trueskill.MU)
    tank_sigma = Column(Float, nullable=False, default=trueskill.SIGMA)
    support_mu = Column(Float, nullable=False, default=trueskill.MU)
    support_sigma = Column(Float, nullable=False, default=trueskill.SIGMA)
    assassin_mu = Column(Float, nullable=False, default=trueskill.MU)
    assassin_sigma = Column(Float, nullable=False, default=trueskill.SIGMA)
    offlane_mu = Column(Float, nullable=False, default=trueskill.MU)
    offlane_sigma = Column(Float, nullable=False, default=trueskill.SIGMA)

    # Play History Info
    tank_games_played = Column(Integer, nullable=False, default=0)
    tank_games_won = Column(Integer, nullable=False, default=0)
    support_games_played = Column(Integer, nullable=False, default=0)
    support_games_won = Column(Integer, nullable=False, default=0)
    assassin_games_played = Column(Integer, nullable=False, default=0)
    assassin_games_won = Column(Integer, nullable=False, default=0)
    offlane_games_played = Column(Integer, nullable=False, default=0)
    offlane_games_won = Column(Integer, nullable=False, default=0)

    def get_stats(self: Self) -> Dict[str, int | str]:
        """Return a representation of the player's stats."""
        return_dict = {}
        for role in ["tank", "support", "assassin", "offlane"]:
            games_played = getattr(self, f"{role}_games_played")
            games_won = getattr(self, f"{role}_games_won")
            if games_played != 0:
                win_rate = games_won / games_played * 100
            else:
                win_rate = 0
            return_dict[role] = {
                "games_played": games_played,
                "games_won": games_won,
                "win_rate": str(win_rate) + "%",
            }
        return return_dict


Base.metadata.create_all(ENGINE)
Session = sessionmaker(bind=ENGINE)
session = scoped_session(Session)


def find_player_stats(user_id: int) -> Dict[str, int | str]:
    """Find a player's stats in the database."""
    db_session: scoped_session = session()
    search_attempt = db_session.query(PlayerData).filter_by(user_id=user_id).first()
    if search_attempt is None:
        logger.info(f"Creating new player entry for {user_id}")
        new_player = PlayerData(user_id=user_id)
        db_session.add(new_player)
        db_session.commit()
        search_attempt = new_player

    return search_attempt.get_stats()
