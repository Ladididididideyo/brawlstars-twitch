#    [Brawl Stars Streaming Integration]
#    Copyright (C) [2026]  [Ogr1sh]
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


#  Twitch Imports
from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.object.eventsub import ChannelFollowEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import AuthScope
from twitchAPI.oauth import UserAuthenticator

import asyncio
#  Flask Imports
from flask import Flask, Response, render_template
#  Misc Imports
from dotenv import dotenv_values
import random
import time
import json
import threading
from queue import Queue
import aiohttp
from playsound3 import playsound
from pathlib import Path

config = dotenv_values(".env")

PROJECT_DIR = Path(__file__).resolve().parent
APP_ID = config["APPLICATION_CLIENT_ID"]
APP_SECRET = config["APPLICATION_CLIENT_SECRET"]
TARGET_SCOPES = [AuthScope.MODERATOR_READ_FOLLOWERS]

new_follower_queue = Queue()
ranks_pool = ["Bronze", "Silver", "Gold", "Diamond", "Mythic", "Legendary", "Masters", "Pro"]
follower_display_time = 5
check_for_new_followers_time = 1
FAKE_NAMES = [
    "ShellySpammer", "ElPrimoLeap", "SpikeEnjoyer", "ColtMain99", 
    "MortisGod", "LeonInvis", "BrawlStarsPro", "GamerTag420",
    "NoobMaster69", "StarPlayer", "EdgarMain", "CrowPoison"
]
DEMO_MODE = True

def trigger_fake_follow():

    fake_user = random.choice(FAKE_NAMES)
    random_rank = random.choice(ranks_pool)
    
    new_follower_queue.put({"username": fake_user, "rank": random_rank})
    
    print(f'{fake_user} now follows Ogr1sh!')

async def on_follow(data: ChannelFollowEvent):
    random_rank = random.choice(ranks_pool)
    
    new_follower_queue.put({"username": data.event.user_name, "rank": random_rank})
    
    print(f'{data.event.user_name} now follows {data.event.broadcaster_user_name}!')

async def run_twitch():
    twitch = await Twitch(APP_ID, APP_SECRET)
    helper = UserAuthenticationStorageHelper(twitch, TARGET_SCOPES)
    await helper.bind()

    user = await first(twitch.get_users())

    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    
    await eventsub.listen_channel_follow_v2(user.id, user.id, on_follow)

    while True:
        await asyncio.sleep(1)

def start_twitch_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_twitch())

threading.Thread(target=start_twitch_thread, daemon=True).start()

# Flask App Setup
app = Flask(__name__)

@app.route('/follower_stream')
def follower_stream():
    def event_stream():
        while True:
            if not new_follower_queue.empty():
                follower_info = new_follower_queue.get()
            
                json_data = json.dumps(follower_info)
                yield f"data: {json_data}\n\n"
                if DEMO_MODE:
                    trigger_fake_follow()
                soundfile = PROJECT_DIR / "static" / "ranked_audio" / f"{follower_info["rank"]}.mp3"
                playsound(soundfile)
                time.sleep(follower_display_time)
            else:
                if DEMO_MODE:
                    trigger_fake_follow()
                time.sleep(check_for_new_followers_time)
            
    return Response(event_stream(), mimetype='text/event-stream')

@app.route('/followers_rank')
def index():
    return render_template('follower_rank.html')

if __name__ == '__main__':
    app.run(port=int(config["WEB_SERVER_PORT"]), debug=False, threaded=True)