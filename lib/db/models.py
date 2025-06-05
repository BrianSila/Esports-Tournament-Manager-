from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///Esports.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Table-1
class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    genre = Column(String)
    rankings = Column(Integer)

    players = relationship('Player', back_populates='team', cascade='all, delete-orphan')
    matches_as_team1 = relationship('Match', foreign_keys='Match.team1_id', back_populates='team1')
    matches_as_team2 = relationship('Match', foreign_keys='Match.team2_id', back_populates='team2')
    wins = relationship('Match', foreign_keys='Match.winner_id', back_populates='winner')

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', genre='{self.genre}')>"

# Table-2
class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    team_id = Column(Integer, ForeignKey('teams.id'))

    team = relationship('Team', back_populates='players')
    
    def __repr__(self):
        return f"<Player(id={self.id}, name='{self.name}', role='{self.role}', team_id='{self.team_id}')>"

# Table-3
class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    team1_id = Column(Integer, ForeignKey('teams.id'))  
    team2_id = Column(Integer, ForeignKey('teams.id'))  
    date = Column(Date)
    winner_id = Column(Integer, ForeignKey('teams.id'))  

    team1 = relationship('Team', foreign_keys=[team1_id], back_populates='matches_as_team1')
    team2 = relationship('Team', foreign_keys=[team2_id], back_populates='matches_as_team2')
    winner = relationship('Team', foreign_keys=[winner_id], back_populates='wins')

    def __repr__(self):
        return f"<Match(id={self.id}, '{self.team1_id} vs {self.team2_id}' on {self.date})>"