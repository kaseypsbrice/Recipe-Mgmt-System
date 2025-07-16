from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional, List
from datetime import datetime

# This file defines the response models for our API.
#
# Naming convention: <Subject>Out || <Subject>In
#
# -- Out -- 
# What the API returns to the user after a request is made.
#
# -- In -- 
# Controls what fields are accepted from the client when 
# making a request.
#

class UserOut(BaseModel):
    user_id: int
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
# Excludes password_hash from being returned in the API response
# from_attributes=True; Pydantic will extract data from the ORM object's attributes.

class UserIn(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    password: Annotated[str, Field(min_length=8, max_length=72)]
# Annotated helps validate input and implements constraints using Field()

class StepOut(BaseModel):
    step_id: int
    step_number: int
    instruction: str

    model_config = ConfigDict(from_attributes=True)

class StepIn(BaseModel):
    img_path: Optional[str]
    instruction: str

class IngredientOut(BaseModel):
    ingredient_id: int
    name: str
    quantity: float
    unit: str

    model_config = ConfigDict(from_attributes=True)

class IngredientIn(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]
    quantity: Annotated[float, Field(gt=0)]
    unit: Annotated[str, Field(max_length=20)]

class AuthorOut(BaseModel):
    user_id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
# Used to nest user info in RecipeOut

class RecipeOut(BaseModel):
    recipe_id: int
    name: str
    user: AuthorOut
    description: Optional[str]
    servings: int
    cook_time_min: int
    img_path: Optional[str]
    created_at: datetime
    steps: List[StepOut]
    ingredients: List[IngredientOut]

    model_config = ConfigDict(from_attributes=True)

class RecipeIn(BaseModel):
    name: Annotated[str, Field(min_length=3)]
    img_path: Optional[str]
    description: Optional[str]
    servings: int
    cook_time_min: int
    steps: List[StepIn]
    ingredients: List[IngredientIn]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None