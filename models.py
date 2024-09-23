from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(Text, nullable=False)
    email = Column(Text, nullable=False)

    # Relationships
    sessions = relationship("Session", back_populates="user")
    targets = relationship("Target", back_populates="user")

class BodySection(Base):
    __tablename__ = 'body_section'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    body_section_name = Column(Text, nullable=False)

    # Relationships
    muscles = relationship("Muscle", back_populates="body_section")
    workouts = relationship("Workout", back_populates="body_section")

class Muscle(Base):
    __tablename__ = 'muscles'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    muscle_name = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    body_section_id = Column(Integer, ForeignKey('body_section.id'), nullable=False)

    # Relationships
    body_section = relationship("BodySection", back_populates="muscles")
    exercises = relationship("Exercise", back_populates="muscle")

class Exercise(Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    exercise_name = Column(Text, nullable=False)
    reps = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    muscle_id = Column(Integer, ForeignKey('muscles.id'), nullable=False)
    intensity_id = Column(Integer, ForeignKey('workouts.intensity'), nullable=False)

    # Relationships
    muscle = relationship("Muscle", back_populates="exercises")
    workout = relationship("Workout", back_populates="exercises")

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    workout_name = Column(Text, nullable=False)
    intensity = Column(Integer, nullable=False)
    body_section_id = Column(Integer, ForeignKey('body_section.id'), nullable=False)

    # Relationships
    body_section = relationship("BodySection", back_populates="workouts")
    sessions = relationship("Session", back_populates="workout")
    exercises = relationship("Exercise", back_populates="workout")

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, ForeignKey('users.username'), nullable=False)
    date = Column(Text, nullable=False)
    workout_id = Column(Integer, ForeignKey('workouts.id'), nullable=False)
    target_id = Column(Integer, ForeignKey('targets.id'), nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")
    workout = relationship("Workout", back_populates="sessions")
    target = relationship("Target", back_populates="sessions")

class Target(Base):
    __tablename__ = 'targets'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, ForeignKey('users.username'), nullable=False)
    month = Column(Text, nullable=False)
    back_and_shoulder_target = Column(Integer, nullable=False)
    back_and_shoulder_progress = Column(Integer, nullable=False)
    arms_target = Column(Integer, nullable=False)
    arms_progress = Column(Integer, nullable=False)
    core_target = Column(Integer, nullable=False)
    core_progress = Column(Integer, nullable=False)
    legs_target = Column(Integer, nullable=False)
    legs_progress = Column(Integer, nullable=False)

    # Relationships
    user = relationship("User", back_populates="targets")
    sessions = relationship("Session", back_populates="target")