# Technical Specification & API Documentation

&emsp;*This document outlines the technical specifications and API models for the Action-Reaction automation platform. The system allows users to create automated workflows by connecting triggers (Actions) from one service to resulting tasks (REActions) in another*

- **System Architecture Summary :**
    ✮ **Application Server ~** Made in Python
    ✮ **Web Client ~** A React frontend served on port 8081.
    ✮ **Mobile Client ~** An Android app made in Kotlin
<br>

### **Data Models**

**User ~**
```
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class User(UserCreate):
    id: int
    is_active: bool
    created_at: datetime
```

**OAuthConnection ~**

```
class OAuthConnection(BaseModel):
		service_id: id
		id: int
		usser_id: int
		access_token: str
		refresh_token: str
		is_active: bool
		connected_at:
```

**Action ~**

```
class Action(BaseModel):
		service_id: id
		name: str
		display_name: str
		description: str
		action_type: ActionType
		is_active: bool
		created_at: datetime

class ActionType(str, Enum)
```

**Reaction ~**

```
class Reaction(BaseModel):
		service_id: id
		name: str
		display_name: str
		description: str
		is_active: bool
		created_at: datetime
```

**Service ~**

```
class Service(BaseModel):
		id: int
		name: str
		display_name: str
		description: str
		service_type: ServiceType
		auth_url:
		is_active: bool
		created_at: datetime

class ServiceType(str, Enum)
```

**Area ~**

```
class Area(BaseModel):
		id: int
		name: str
		description: str
		action_id: int
		reaction_id: int
		user_id: int

class AreaUpdate(BaseModel):
		name: str
		description: str
		action_id: int
		reaction_id: int
		update_at: datetime
```
<br>

### **API Endpoints**

#### **AUTHENTIFICATION**:

&emsp;**POST /api/auth/register**

&emsp;**Description**: Create a new account

&emsp;**Request body:**

    {
        ****"email ****":  ****"user@example.com ****"
        "password": "password123",
        "username": "username"
    }

&emsp;**Response Success:**

    {
        ****"message": "Account created successfuly",
        "user" {
            "email": "“user@example.com",
            "id": "1234",
            "username": "username"
        }
    }

&emsp;**Response Error:**

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
<br>

&emsp;**POST /api/auth/login**

&emsp;**Description**: Connect a user to his account

&emsp;**Request body:**

    {
        ****"email ****":  ****"user@example.com"
        "password": "password123",
    }

&emsp;**Response Success:**

    {
        "message": "connexion successfull",
        "user" {
            "id": "1234",
            "email ****":  ****"user@example.com ****"
            "username": "username"
        }
    }

&emsp;**Response Error:**

    {
        "status": 401,
            "error": {
            "code": 2,
            "message": [
                "Invalid email or password"
            ]
        }
    }
<br>

#### **SERVICE:**

&emsp;**GET /api/services**

&emsp;**Description:** List of available services

&emsp;**Response Success:**

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

&emsp;**Response Error:**

    {
        "status": 401,
            "error": {
            "code": 3,
            "message": [
                "Authentication required"
            ]
        }
    }
<br>

#### **AREA:**

&emsp;**POST /api/areas**

&emsp;**Description:** Create an AREA

&emsp;**Request Body:**

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

&emsp;**Response Success:**

    {
        "message": "AREA created with succes",
        "area": {
        "id": "area_meteo_1",
        "name": "Heart wave alert",
        "active": true
        }
    }

&emsp;**Response Error:**

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
<br>

#### **SYSTEM:**

&emsp;**GET /about.json**

&emsp;**Description:** Server informations

&emsp;**Response Success:**

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


<br>

⣧⢮⢭⠛⢲⣦⣀⠀⠀⠀⠀⡀⠀⠀⠀\
⠈⠻⣶⡛⠲⣄⠀⠙⠢⣀⠀⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⢻⣿⣥⡬⠽⠶⠤⣌⣣⣼⡔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⢠⣿⣧⣤⡴⢤⡴⣶⣿⣟⢯⡙⠒⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⠘⣗⣞⣢⡟⢋⢜⣿⠛⡿⡄⢻⡮⣄⠈⠳⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⠀⠈⠻⠮⠴⠵⢋⣇⡇⣷⢳⡀⢱⡈⢋⠛⣄⣹⣲⡀⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣱⡇⣦⢾⣾⠿⠟⠿⠷⠷⣻⠧⠀⠀⠀⠀⠀⠀⠀⠀\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠽⠞⠊⠀⠀  _<sub>By ✧˖°. Winx magic .°˖✧</sub>_
