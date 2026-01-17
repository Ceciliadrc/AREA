# DOCKER DOCUMENTATION

*This documentation explains the Docker setup for a multi-service application consisting of a PostgreSQL database, Python backend server, React web client, and Android mobile client.*

---

## Architecture overview

The application uses Docker Compose to orchestrate 4 services:

- **db :** PostgreSQL database
- **server :** Python/FastAPI backend
- **client_mobile :** Android APK builder
- **client_web :** React/Vite web client with Nginx

---

## Service details

### 1. Database service (db)
**Image :** `postgres:16`

**Purpose :** Provides PostgreSQL database for the application.

**Configuration :**
```yaml
environment:
  - POSTGRES_DB=${POSTGRES_DB}
  - POSTGRES_USER=${POSTGRES_USER}
  - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
volumes:
  - db-data:/var/lib/postgresql/data
networks:
  - back-tier
```
**Description :**
- Uses persistent volume `db-data` to retain data between restarts
- Connected to `back-tier` network for backend communication
- Credentials are set up in an environment file (see `.env.example`)

<br>

### 2. Server Service (server)

**Dockerfile Location :** `./server/Dockerfile`

**Base Image :** `python:3.11-slim`

**Purpose :** FastAPI/Uvicorn backend server handling API requests.

**Dockerfile :** [See the Dockerfile](../server/Dockerfile)

**Exposed Port :** 8080

**Dependencies :** Requires `db` service to be running

**Access :** http://localhost:8080/about.json

<br>

### 3. Mobile Client Service (client_mobile)

**Dockerfile Location :** `./mobile/Dockerfile`

**Base Image :** `gradle:8.14.3-jdk21`

**Purpose :** Builds Android APK file for mobile distribution.

**Dockerfile :** [See the Dockerfile](../mobile/Dockerfile)

**Description :**
- Uses Android SDK 34
- Builds a release APK
- Outputs APK to shared volume `/apk/client.apk`

**Volume :** Shares `common` volume with `client_web` service

**Access (Download) :** http://localhost:8081/client.apk

<br>

### 4. Web Client Service (client_web)

**Dockerfile Location :** `./web/Dockerfile`

**Base Image :** Multi-stage build using `node:18-alpine` and `nginx:alpine`

**Purpose :** Serves React/Vite web application and provides APK download.

**Dockerfile :** [See the Dockerfile](../web/Dockerfile)

**Exposed Port :** 8081

**Dependencies :** Requires both `server` and `client_mobile` services

**Volume: ** Mounts `common` volume at `/apk` to access the built APK

**Access (Web app) :** http://localhost:8081

---

## Volumes

### `common`
- Shared between `client_mobile` and `client_web`
- Mobile service writes APK to `/apk/client.apk`
- Web service serves it via Nginx

### `db-data`
- Persists PostgreSQL database data
- Prevents data loss on container restart

---

## Networks

### `back-tier`
- Connects: `db`, `server`, and `client_web`
- Mobile service doesn't need network access, it only builds APK

---

## Docker Compose Commands
```bash
# stop all services
docker-compose down -v

# rebuild all images and start all services
docker-compose up --build

# view all running services
docker-compose ps
```

<br>

⣧⢮⢭⠛⢲⣦⣀⠀⠀⠀⠀⡀⠀⠀⠀\
⠈⠻⣶⡛⠲⣄⠀⠙⠢⣀⠀⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⢻⣿⣥⡬⠽⠶⠤⣌⣣⣼⡔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⢠⣿⣧⣤⡴⢤⡴⣶⣿⣟⢯⡙⠒⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⠘⣗⣞⣢⡟⢋⢜⣿⠛⡿⡄⢻⡮⣄⠈⠳⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⠀⠈⠻⠮⠴⠵⢋⣇⡇⣷⢳⡀⢱⡈⢋⠛⣄⣹⣲⡀⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣱⡇⣦⢾⣾⠿⠟⠿⠷⠷⣻⠧⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠽⠞⠊⠀⠀  _<sub>By ✧˖°. Winx magic .°˖✧</sub>_
