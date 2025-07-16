from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db, User, Recipe, Step, Ingredient
from backend.security import hash_password, verify_password, create_access_token, decode_access_token
from backend.response_model import UserOut, UserIn, Token, TokenData, RecipeIn, RecipeOut
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from datetime import datetime, timezone

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origin_regex=r"^http://localhost:\d+$",
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
# Allows connections originating from any ports on localhost.

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: Session = Depends(get_db)) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    username: str = payload.get("sub") if payload else None
    if username is None:
        raise credentials_exc

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exc
    return user

@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    pwd_hash = hash_password(user.password)
    new_user = User(username=user.username, password_hash=pwd_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return (new_user)
# Creates a new user

@app.get("/users/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return (db.query(User).all())
# Returns all users in database

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
# Login (issue JWT)

@app.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
# “Who am I?” endpoint

@app.post("/logout")
def logout():
    """
    With stateless JWTs, logout is handled client-side.
    Remove the stored token to “log out.”
    """
    return {"message": "Successfully logged out on client side. Please delete your JWT."}
# Logout hint (client–side removes token)

@app.post(
    "/create_recipe",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new recipe"
)

def create_recipe(
    payload: RecipeIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = Recipe(
        user_id=current_user.user_id,
        name=payload.name,
        description=payload.description,
        servings=payload.servings,
        img_path=payload.img_path or "",
        cook_time_min=payload.cook_time_min,
    )
    # Create Recipe tied to the logged-in user

    for idx, step_in in enumerate(payload.steps, start=1):
        recipe.steps.append(
            Step(
                step_number=idx,
                instruction=step_in.instruction,
                img_path=step_in.img_path or "",
            )
        )
    # Append Steps in order

    for ing_in in payload.ingredients:
        recipe.ingredients.append(
            Ingredient(
                name=ing_in.name,
                quantity=ing_in.quantity,
                unit=ing_in.unit or "",
            )
        )
    # Append Ingredients

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    # --- File write: append a log entry ---
    with open("backend/static/recipe_logs/recipe_log.txt", "a") as log_file:
        log_file.write(
            f"{datetime.now(timezone.utc).isoformat()}  "
            f"user={current_user.username}  "
            f"recipe_id={recipe.recipe_id}  "
            f"name={recipe.name}\n"
        )

    return {"recipe_id": recipe.recipe_id}

@app.get("/recipes/{recipe_id}", response_model=RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
# Returns a recipe that matches a specific recipe_id

@app.get("/my_recipes", response_model=List[RecipeOut])
def get_my_recipes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Recipe).filter(Recipe.user_id == current_user.user_id).all()
# Returns all recipes by the user currently signed in

@app.get("/recipes", response_model=List[RecipeOut])
def get_all_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).all()
# Returns all recipes from all users

@app.put(
    "/recipes/{recipe_id}",
    response_model=RecipeOut,
    summary="Update an existing recipe",
)
def update_recipe(
    recipe_id: int,
    payload: RecipeIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to edit this recipe",
        )
    # fetch and authorisation

    recipe.name          = payload.name
    recipe.description   = payload.description
    recipe.servings      = payload.servings
    recipe.cook_time_min = payload.cook_time_min
    recipe.img_path      = payload.img_path or recipe.img_path
    # Update the basic fields

    db.query(Step).filter(Step.recipe_id == recipe_id).delete()
    for idx, step_in in enumerate(payload.steps, start=1):
        recipe.steps.append(
            Step(
                step_number=idx,
                instruction=step_in.instruction,
                img_path=step_in.img_path or "",
            )
        )
    # Replace steps

    db.query(Ingredient).filter(Ingredient.recipe_id == recipe_id).delete()
    for ing_in in payload.ingredients:
        recipe.ingredients.append(
            Ingredient(
                name=ing_in.name,
                quantity=ing_in.quantity,
                unit=ing_in.unit or "",
            )
        )
    # Replace ingredients

    db.commit()
    db.refresh(recipe)
    return recipe
    # Commit and return updated recipe

@app.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(
    recipe_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipe = db.query(Recipe).get(recipe_id)
    if not recipe or recipe.user_id != current_user.user_id:
        raise HTTPException(404, "Not found or not yours")
    db.delete(recipe)
    db.commit()

@app.get("/help", response_class=PlainTextResponse)
def get_help_text():
    with open("backend/static/help.txt", "r") as help_file:
        content = help_file.read()
    return content