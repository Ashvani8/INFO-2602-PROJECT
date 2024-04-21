from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from App.database import db  # Import the SQLAlchemy database object

class Exercise(db.Model):  # Change db.model to db.Model
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    desc = Column(String)
    exercise_type = Column(String)
    body_part = Column(String)
    equipment = Column(String)
    level = Column(String)
    rating = Column(Integer)
    rating_desc = Column(String)
    routine_id = Column(Integer, ForeignKey('routines.id'))
    routine = relationship("Routine", back_populates="exercises")

    def __init__(self, title, desc, exercise_type, body_part, equipment, level, rating, rating_desc):
        self.title = title
        self.desc = desc
        self.exercise_type = exercise_type
        self.body_part = body_part
        self.equipment = equipment
        self.level = level
        self.rating = rating
        self.rating_desc = rating_desc
