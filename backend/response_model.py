from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
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