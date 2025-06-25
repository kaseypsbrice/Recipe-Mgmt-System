# Setup

> [!NOTE]
> This project was setup in an Ubuntu VM.

## Database

Login to postgres:

```
-u postgres psql
```

Create a new database:

```
CREATE DATABASE irms
```

Confirm that the database was created by viewing all databases:

```
\l
```

Connect to the database:

```
\c irms
```

After creating tables, check if the tables were created:

```
\dt
```

Create a user that has full access to the database:

```
CREATE USER irms_admin WITH PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE irms TO irms_admin;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO irms_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO irms_admin;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO irms_admin;

// Ensure future tables and other objects are automatically accessible
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO irms_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO irms_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO irms_admin;
```

To login to psql with the new user role, a Linux user with the same name needs to be created:

```
sudo adduser <new_user_role>
```

Login as that user:

```
su - <username>
```

Login to the database:

```
psql -U irms_admin irms
```

For more information on using postgres with Python, visit the website [here](https://www.freecodecamp.org/news/postgresql-in-python/).