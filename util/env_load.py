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
ADMIN_ID = int(os.environ.get("ADMIN"))
QUEUED_ID = int(os.environ.get("QUEUED"))

TANK_EMOJI = str(os.environ.get("TANK_EMOJI"))
SUPPORT_EMOJI = str(os.environ.get("SUPPORT_EMOJI"))
ASSASSIN_EMOJI = str(os.environ.get("ASSASSIN_EMOJI"))
OFFLANE_EMOJI = str(os.environ.get("OFFLANE_EMOJI"))

LOBBY_CHANNEL_ID = int(os.environ.get("LOBBY_CHANNEL_ID"))
TEAM_1_CHANNEL_ID = int(os.environ.get("TEAM_1_CHANNEL_ID"))
TEAM_2_CHANNEL_ID = int(os.environ.get("TEAM_2_CHANNEL_ID"))
GENERAL_CHANNEL_ID = int(os.environ.get("GENERAL_CHANNEL_ID"))
