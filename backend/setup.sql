CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recipes (
	recipe_id SERIAL PRIMARY KEY,
	user_id INTEGER REFERENCES users(user_id),
	name VARCHAR(100),
	img_path VARCHAR(255),
	description TEXT,
	servings INTEGER,
	cook_time_min INTEGER,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE steps (
    step_id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(recipe_id),
    img_path VARCHAR(255),
    step_number INTEGER,
    instruction TEXT
);

CREATE TABLE ingredients (
    ingredient_id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(recipe_id),
    name VARCHAR(100),
    quantity DECIMAL(5,2),
    unit VARCHAR(20)
);
