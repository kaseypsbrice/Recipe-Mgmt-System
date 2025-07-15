from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text, DECIMAL, func, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from backend.keys import DB_USER, DB_PASS

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

    recipes = relationship('Recipe', back_populates='user')
    # Establishes a relationship between 'user' and 'recipes'
    # back_populates ensures a bidirectional relationship between classes

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
    img_path = Column(Text, nullable=True)
    description = Column(Text)
    servings = Column(Integer)
    cook_time_min = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship('User', back_populates='recipes')
    steps = relationship('Step', back_populates='recipe', cascade="all, delete-orphan")
    ingredients = relationship('Ingredient', back_populates='recipe', cascade="all, delete-orphan")
    # cascade="all"
    # When you do something to the parent, the same will apply to the children of the class.
    # delete-orphan
    # If the child object disassociates from it's parent, it'll automatically be deleted.

    def __repr__(self):
        return f"<Recipe(recipe_id={self.recipe_id}, name='{self.name}', user_id={self.user_id})>"

class Step(Base):
    __tablename__ = 'steps'

    step_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), nullable=False)
    img_path = Column(Text, nullable=True)
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

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@localhost:5432/irms"
# DATABASE_URL = postgresql://username:password@localhost:port_number/dbname

engine = create_engine(DATABASE_URL)
# Creates a connection to the PostgreSQL database

Base.metadata.create_all(engine)
# Creates tables only if they don't already exist

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Session maker factory, creates a session when called

def get_db():
    db = SessionLocal()
    try:
        yield db
        # Gives a database session to the path operation (api endpoint)
    finally:
        db.close()
        # Ensures the connection is closed after use