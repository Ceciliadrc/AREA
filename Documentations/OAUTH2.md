# Oauth2 doc

*Oauth2 is an authorization protocol that allows users to log in using a third party service.*

**For the services we choose :**

&emsp; **❀** Dropbox
&emsp; **❀** Github
&emsp; **❀** Gmail
&emsp; **❀** Microsoft
&emsp; **❀** Notion
&emsp; **❀** Twitch

## Oauth2 implementation in our project ~

**How it works :**

1. The user log in with the service
2. The user is redirected to the service login page
3. The user consent
4. The service gives a code to our project backend
5. The code is exchanged with an access token
6. The access token is used to retreive the user’s profile on the service
7. The tokens are stored in the database
&emsp;

**Endpoints :**

&emsp; ***Login*** → redirect the user to the login page of the service

&emsp; ***Callback*** → after the user authenticates himself on the service
<br>

### Service Configuration with the Database ~

**In our project, we can :**

**✴︎** Retrieve the OAuth configuration of a service by its name
**✴︎** Create or update OAuth tokens for a user and a specific service
**✴︎** Fetch OAuth token data for a user based on the service name
**✴︎** Initialize default OAuth-enabled services in the database
<br>

**Requirements :**

pip install fastapi uvicorn python-dotenv httpx


<br>

⣧⢮⢭⠛⢲⣦⣀⠀⠀⠀⠀⡀⠀⠀⠀
⠈⠻⣶⡛⠲⣄⠀⠙⠢⣀⠀⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢻⣿⣥⡬⠽⠶⠤⣌⣣⣼⡔⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⣿⣧⣤⡴⢤⡴⣶⣿⣟⢯⡙⠒⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠘⣗⣞⣢⡟⢋⢜⣿⠛⡿⡄⢻⡮⣄⠈⠳⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠻⠮⠴⠵⢋⣇⡇⣷⢳⡀⢱⡈⢋⠛⣄⣹⣲⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣱⡇⣦⢾⣾⠿⠟⠿⠷⠷⣻⠧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⠽⠞⠊⠀⠀  _<sub>By ✧˖°. Winx magic .°˖✧</sub>_