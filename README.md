# HealthSync

### Setup for development
Create a `.env` file at the root of project, refer to [this](./.env.example) for creating the `.env`.

Create a virtual environment
For linux
```
python3 -m venv .venv && source ./.venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```

#### Setup db
For setting up local mongodb, you can use docker
Create a folder `tests` in the root directory, cd to `tests`.
Create a directory `mongodb_data`.
Create a file `docker-compose.yml` and put the following contents.
```
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: [username]
      MONGO_INITDB_ROOT_PASSWORD: [password]
      MONGO_INITDB_DATABASE: [dbname]
    volumes:
      - ./mongodb_data:/data/db

```
Then execute `docker compose up -d`.
Edit the `.env` accordingly.

Generate `SECRET_KEY` with the following
```
python3 -c 'import secrets; print(secrets.token_hex(16))'
```

Then start the server by `flask run`.

API docs [here](https://documenter.getpostman.com/view/24270306/2s9YysE2d6).