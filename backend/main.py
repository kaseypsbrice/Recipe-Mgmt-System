from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from keys import IRMS_ADMIN_PASS

# Uses SQLAlchemy, an Object-Relational Mapper (ORM).
# Provides a way to interact with a database using OOP principles
# rather than writing raw SQL queries.

Base = declarative_base()
# Constructs a base class for declarative class definitions

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', username='{self.username}')>"
    # Defines how instances of the class should be represented as a string.
    # When debugging or logging, the object will be in a readable format 
    # instead of a generic object reference.

class Recipe(Base):
    __tablename__ = 'recipes'

    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(100), nullable=False)
    img_path = Column(String(255))
    description = Column(Text)
    servings = Column(Integer)
    cook_time_min = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship('User', back_populates='recipes')
    # Establishes a relationship between 'recipes' and 'users'
    # back_populates ensures a bidirectional relationship between classes

    def __repr__(self):
        return f"<Recipe(recipe_id={self.recipe_id}, name='{self.name}', user_id={self.user_id})>"

class Step(Base):
    __tablename__ = 'steps'

    step_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), nullable=False)
    img_path = Column(String(255), nullable=False)
    step_number = Column(Integer)
    instruction = Column(Text)

    recipe = relationship('Recipe', back_populates='steps')

    def __repr__(self):
        return f"<Step(step_id={self.step_id}, instruction='{self.instruction}', recipe_id={self.recipe_id})>"
    
class Ingredient(Base):
    __tablename__ = 'ingredients'

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), nullable=False)
    name = Column(String(100), nullable=False)
    quantity = Column(DECIMAL(5,2), nullable=False)
    unit = Column(String(20))

    recipe = relationship('Recipe', back_populates='ingredients')

    def __repr__(self):
        return f"<Ingredient(ingredient_id={self.ingredient_id}, name='{self.name}', recipe_id={self.recipe_id})>"

DATABASE_URL = f"postgresql://irms_admin:{IRMS_ADMIN_PASS}@localhost/irms"
# DATABASE_URL = postgresql://username:password@localhost/dbname

engine = create_engine(DATABASE_URL)
# Creates a connection to the PostgreSQL database

Base.metadata.create_all(engine)
# Creates tables (only if they don't already exist)