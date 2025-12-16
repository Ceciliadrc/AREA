# Technical Specification & API Documentation

*This document outlines the technical specifications and API models for the Action-Reaction automation platform. The system allows users to create automated workflows by connecting triggers (Actions) from one service to resulting tasks (REActions) in another*

- **System Architecture Summary :**
    - **Application Server ~** Made in Python
    - **Web Client ~** A React frontend served on port 8081.
    - **Mobile Client ~** An Android app made in Kotlin

---

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

---

### **API Endpoints**

**AUTHENTIFICATION**:

**POST /api/auth/register**

**Description**: Crée un nouveau compte utilisateur

**Request body:**
```
{
    "email":  "user@example.com"
    "password": "password123",
    "username": "username"
}
```
**Response Success:**
```
{
    "message": "Compte crée avec succès",
    "user" {
        "email": "“user@example.com",
        "id": "1234",
        "username": "username"
    }
}
```
**Response Error:**
```
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

**Description**: Connecter l’utilisateur a son compte

**Request body:**
```
{
    "email": "user@example.com"
    "password": "password123",
}
```
**Response Success:**
```
{
    "message": "connexion réussie",
    "user" {
        "id": "1234",
        "email": "user@example.com"
        "username": "username"
    }
}
```
**Response Error:**
```
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

**Description:** Liste des services disponibles

**Response Success:**
```
{
    "services": [
        {
            "name": "meteo_france",
            "displayName": "Météo France",
            "actions": [
                {
                    "name": "weather_alert",
                    "description": "Alerte météo quelque part"
                },
                {
                    "name": "temperature_above",
                    "description": "Température dépasse X degrés"
                }
            ],
            "reactions": [
                {
                    "name": "send_weather_alert",
                    "description": "Envoyer une alerte météo"
                }
            ]
        }
    ]
}
```
**Response Error:**
```
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

**Description:** Créer une AREA

**Request Body:**
```
{
    "name": "Alerte canicule",
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
            "subject": "Alerte canicule Toulouse",
            "body": "La température a dépassé 30°C !"
        }
    }
}
```
**Response Success:**
```
{
    "message": "AREA créée avec succès",
    "area": {
        "id": "area_meteo_1",
        "name": "Alerte canicule",
        "active": true
    }
}
```
**Response Error:**
```
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
**SYSTÈME:**

**GET /about.json**

**Description:** Informations du serveur

**Response Success:**
```
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
                        "description": "Alerte météo quelque part"
                    },
                    {
                        "name": "temperature_above ",
                        "description": "Température dépasse X degrés"
                    }
                ],
                "reactions": [
                    {
                        "name": "send_weather_alert",
                        "description": "Envoyer une alerte météo"
                    }
                ]
            }
        ]
    }
}
```

---

### List of services

- OpenAI ([https://openai.com/fr-FR/api/](https://openai.com/fr-FR/api/))
- Spotify (g pas le lien j'ai pas cherché )
- Instagram ([https://developers.facebook.com/products/instagram/apis/?utm_source=chatgpt.com](https://developers.facebook.com/products/instagram/apis/?utm_source=chatgpt.com))
- Letterbox ([https://api-docs.letterboxd.com/](https://api-docs.letterboxd.com/))
- Google services ([https://cloud.google.com/apis?hl=fr](https://cloud.google.com/apis?hl=fr))
- Twitch ([https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/))
- Notion ([https://developers.notion.com/docs/authorization](https://developers.notion.com/docs/authorization))