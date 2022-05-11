# PsiBot
A Discord chat bot to provide administration, utility, and fun to your server.

## Prerequisites
Firstly, you'll need to install [Python version 3.8 or higher](https://www.python.org/downloads/). 

Secondly, you'll need the main [discord.py](https://discordpy.readthedocs.io/en/stable/) API. Details on how to use and install the API can be found on their site and [Github](https://github.com/Rapptz/discord.py).
For most users, the following powershell/terminal commands should suffice...
```
# Linux/macOS
python3 -m pip install -U discord.py

# Windows
py -m pip install -U discord.py
```

Thirdly, you'll need to install the [discord-py-interactions](https://pypi.org/project/discord-py-slash-command/) extension.
```
python3 -m pip install -U discord-py-slash-command.py

# Windows
py -m pip install -U discord-py-slash-command.py
```

## Configuration
Firstly, you'll need to set up a Discord Application through the [Discord Applications Portal](https://discord.com/developers/applications/). 
### GUI
To be added...
### Manual Configuration
The only file to configure will be the bot_config.txt file in the config folder.
Here, you'll need to enter the following information in the according spots...
1. token = The bot token. [Click here](https://www.writebots.com/discord-bot-token/) for more information.
2. botownerid = Your Discord User ID. [Click here](https://www.remote.tools/remote-work/how-to-find-discord-id) for more information

## Running the Bot
That's all the necessary configuration! After you can either run the bot using the GUI (to be added...) or by running the following command inside the directory using powershell/terminal...
```
py index.py
```