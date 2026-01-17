# Backend documentation

### **Technologies used :**

- **FastAPI**  - Modern API framework
- **SQLAlchemy**  - ORM for PostgreSQL
- **PostgreSQL** - Database
- **Oauth2** - Third party authentication
- **Threading** - Hook execution
<br>
### **API endpoints :**

**Authentication:**

- `POST /auth/register` - Registration (username, email, password)
- `POST /auth/login` - Login (email, password)
- `GET /auth/google/login` - OAuth2 Google

**Services:**

- `GET /services/` - List of all the services
- `GET /services/{id}` - Details d'of a service
- `GET /services/{id}/actions` - Actions of a service
- `GET /services/{id}/reactions` - Reactions of a service

**Areas (workflow):**

- `POST /areas/` - Create an AREA (name, user_id, action_id, reaction_id)
- `GET /areas/?user_id={id}` - View user’s Areas
- `DELETE /areas/{id}` - Delete an Area

**Informations:**

- `GET /` - Test API
- `GET /about.json` - Required format by the project
<br>
### Services :

&emsp; ʚɞ Dropbox

&emsp; ʚɞ Github

&emsp; ʚɞ Google (Gmail)

&emsp; ʚɞ Microsoft

&emsp; ʚɞ Notion

&emsp; ʚɞ Twitch

*To know the action and reaction of each service, see this documentation SERVICES_ACTION_AND_REACTIONS*
<br>
### Automatic features when you start the project :

&emsp; ✧ Database verification

&emsp; ✧ Table creation if they doesn’t exist

&emsp; ✧ Service initialization

&emsp; ✧ Background hook system starts
<br>
### **Database :**

**Tables**:

&emsp;**users** (id, username, email, hashed_password)

&emsp;**services** (id, name, display_name)

&emsp;**actions** (id, service_id, name)

&emsp;**reactions** (id, service_id, name)

&emsp;**areas** (id, name, user_id, action_id, reaction_id)

&emsp;**service_oauth** (id, service_id, client_id, client_secret, redirect_uti)

&emsp;**user_oauth** (id, user_id, service_id, access_token, refresh_token)
<br>
### **Testing the API:**

Example:

- *Basic test ~* curl http://localhost:8080/
- *API information ~* curl http://localhost:8080/about.json
<br>
### How to start the project in your terminal :

- docker-compose up —build
- docker-compose down

<br>
<br>

⣧⢮⢭⠛⢲⣦⣀⠀⠀⠀⠀⡀⠀⠀⠀
⠈⠻⣶⡛⠲⣄⠀⠙⠢⣀⠀⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢻⣿⣥⡬⠽⠶⠤⣌⣣⣼⡔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⣿⣧⣤⡴⢤⡴⣶⣿⣟⢯⡙⠒⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠘⣗⣞⣢⡟⢋⢜⣿⠛⡿⡄⢻⡮⣄⠈⠳⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠻⠮⠴⠵⢋⣇⡇⣷⢳⡀⢱⡈⢋⠛⣄⣹⣲⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣱⡇⣦⢾⣾⠿⠟⠿⠷⠷⣻⠧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠽⠞⠊⠀⠀  _<sub>By ✧˖°. Winx magic .°˖✧</sub>_