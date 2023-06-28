"""
    Informations Générales
"""
DISCORD_TOKEN   = ""
TEST_GUILDS     = []
CLIENT_ID       = 0
DEV_MODE        = True
VERSION         = "1.7.3"
TIMEZONE        = "Europe/Paris"
LOGS_CHANNEL_ID = 0

SUPPORT_SERVER  = ""
ADD_BOT_LINK    = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions=137439463488&scope=bot%20applications.commands"
GITHUB_LINK     = "https://github.com/Yarkis01/Ayo"


"""
    Modules
"""
MODULES = {
    "bestof"                : True,
    "callout"               : True,
    "cephalochic"           : True,
    "codesamis"             : True,
    "feedback"              : True,
    "festivals"             : True,
    "informationcommands"   : True,
    "liquider"              : True,
    "loterie"               : True, 
    "odyssee"               : True,
    "ping"                  : True,
    "rotations"             : True
}


"""
    API
"""
HEADERS_BASE = {
    "User-Agent": "",
    "From": ""
}

SPLATOON3_API = "https://splatoon3.ink/data"
SPLATOON2_API = "https://splatoon2.ink/data"

PTERO_API_URL = ""
PTERO_API_KEY = ""

WATCH_API_URL = f"https://api.watchbot.app/bot/{CLIENT_ID}"
WATCH_API_KEY = ""

TIMEOUT   = 5
ADD_HOURS = 1


"""
    Rotations - Config
"""
ROTATION_CHANNEL_ID = 0
ROTATION_ROLES_ID   = 0