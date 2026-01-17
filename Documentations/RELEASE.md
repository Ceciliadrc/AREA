# Creating a release

### Current release : v0.0.0

### Step 1: Ensure your code is ready
Make sure all your changes are committed and pushed to the main branch.
```bash
# Commit your changes
git add .
git commit -m "[ADD/FIX/DEL/...]: message"
git push origin main
```

### Step 2: Create and push a version tag
Create a tag following this format : vX.Y.Z.\
The tag must start with v followed by the version number (e.g., v1.0.0, v2.1.3, v1.0.0-beta)
```bash
# Create a tag locally
git tag v1.0.0

# Push the tag to trigger the release workflow
git push origin v1.0.0
```

### Step 3: Monitor the Workflow

Go to the Actions tab in the repository and watch the workflow execute:
- Mirrors code to the target repository
- Creates a release in this repository
- Creates a release in the mirror repository

### Step 4: Update This README
After successful release, update the current release version at the top of this section.

### Version Numbering
- Major (v2.0.0): Breaking changes
- Minor (v1.1.0): New features, backward compatible
- Patch (v1.0.1): Bug fixes, backward compatible

### Delete a Tag
```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin --delete v1.0.0
```

### Check All Tags
```bash
# List all tags
git tag -l

# View tag details
git show v1.0.0
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
