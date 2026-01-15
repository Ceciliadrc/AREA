# AREA

## Project by
- anna.bardoux@epitech.eu
- carla.thierry@epitech.eu
- cecilia.deriche@epitech.eu
- doha.mansour@epitech.eu
- jules.de-rus@epitech.eu

---

## Start the project

### Prerequisites
- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git**

### Installation & Setup

- **Clone the repository**
```bash
   git clone <repository-url>
   cd AREA
```
- **Configure environment variables**
```bash
# Copy the example environment file
cp .env.example .env
# Edit the .env file with your configuration
```
- **Build and start all services**
```bash
docker-compose up --build -d
```

- **Verify the services are running**
```bash
docker-compose ps
```

### Access the services

- API Server: http://localhost:8080
- Web Client: http://localhost:8081
- Download APK: http://localhost:8081/client.apk
- About endpoint: http://localhost:8080/about.json

### Architecture

The project consists of 4 main services:
- PostgreSQL Database : Stores user data and AREA configurations 
- Server (API) : Python/FastAPI backend (port 8080)
- Web Client : Web interface (port 8081)
- Mobile Client : Generates mobile application

---

## API details

**AUTHENTIFICATION**:

**POST /api/auth/register**

**Description**: Create a new account

**Request body:**
```bash
{
    "email": "user@example.com"
    "password": "password123",
    "username": "username"
}
```

**Response Success:**
```bash
{
    "message": "Account created successfuly",
    "user" {
        "email": "“user@example.com",
        "id": "1234",
        "username": "username"
    }
}
```

**Response Error:**
```bash
{
    "status": 400,
    "error": {
        "code": 1,
        "message": [
            "Email already used",
            "Password not strong enough",
        ]
    }
}
```

**POST /api/auth/login**

**Description**: Connect a user to his account

**Request body:**
```bash
{
    "email": "user@example.com"
    "password": "password123",
}
```
**Response Success:**
```bash
{
    "message": "connexion successful",
    "user" {
        "id": "1234",
        "email": "user@example.com"
        "username": "username"
    }
}
```
**Response Error:**
```bash
{
    "status": 401,
    "error": {
        "code": 2,
        "message": [
            "Invalid email or password"
        ]
    }
}
```

**SERVICE:**

**GET /api/services**

**Description:** List of available services

**Response Success:**

```bash
{
    "services": [
        {
            "name": "meteo_france",
            "displayName": "Météo France",
            "actions": [
                {
                   "name": "weather_alert",
                   "description": "Weather alert somewhere"
                },
               {
                   "name": "temperature_above",
                   "description": "Temperature above X degrees"
               }
            ],
            "reactions": [
                {
                    "name": "send_weather_alert",
                    "description": "Send a weather alert"
                }
            ]
        }
    ]
}
```
**Response Error:**
```bash
{
    "status": 401,
        "error": {
        "code": 3,
        "message": [
            "Authentication required"
        ]
    }
}
```
**AREA:**

**POST /api/areas**

**Description:** Create an AREA

**Request Body:**
```bash
{
    "name": "Heat wave alert",
    "action": {
       "service": "meteo_france",
       "name": "temperature_above",
       "config": {
           "city": "Toulouse",
           "temperature": 30
       }
    },
    "reaction": {
     "service": "gmail",
     "name": "send_emailt",
     "config": {
          "to": "username@example.com",
           "subject": "Heat wave alert in Toulouse",
           "body": "The weather went above 30°C !"
      }
    }
}
```
**Response Success:**
```bash
{
    "message": "AREA created with succes",
    "area": {
       "id": "area_meteo_1",
       "name": "Heart wave alert",
       "active": true
    }
}
```
**Response Error:**
```bash
{
    "status": 400,
    "error": {
        "code": 4,
        "message": [
            "Service not found",
            "Invalid action configuration"
        ]
    }
}
```
**SYSTEM:**

**GET /about.json**

**Description:** Server informations

**Response Success:**
```bash
{
    "client": {
    "host": "127.0.0.1"
    },
    "server": {
    "services": [
        {
        "name": "meteo_france",
        "actions": [
            {
                "name": "weather_alert",
                "description": "Weather alert somewhere”
            },
            {
                "name": "temperature_above ",
                "description": "Temperature above X degrees"
            }
        ],
        "reactions": [
            {
                "name": "send_weather_alert",
                "description": "Send a weather alert"
            }
            ]
        }
        ]
    }
}
```