import os
from dotenv import load_dotenv

load_dotenv()

TANK_ID = int(os.environ.get("TANK"))
SUPPORT_ID = int(os.environ.get("SUPPORT"))
ASSASSIN_ID = int(os.environ.get("ASSASSIN"))
OFFLANE_ID = int(os.environ.get("OFFLANE"))
TANK_FILL_ID = int(os.environ.get("TANK_FILL"))
SUPPORT_FILL_ID = int(os.environ.get("SUPPORT_FILL"))
ASSASSIN_FILL_ID = int(os.environ.get("ASSASSIN_FILL"))
OFFLANE_FILL_ID = int(os.environ.get("OFFLANE_FILL"))
BOT_ENGINEER_ID = int(os.environ.get("BOT_ENGINEER"))
