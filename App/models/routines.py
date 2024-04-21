from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from App.database import db  # Import the SQLAlchemy database object

class Routine(db.Model):  # Change db.model to db.Model
    __tablename__ = 'routines'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    exercise_type = Column(String)
    muscle_group = Column(String)
    difficulty_level = Column(String)
    exercises = relationship("Exercise", back_populates="routine")

    def __init__(self, name, exercise_type, muscle_group, difficulty_level):
        self.name = name
        self.exercise_type = exercise_type
        self.muscle_group = muscle_group
        self.difficulty_level = difficulty_level

