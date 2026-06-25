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
from twitchAPI.helper import first
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticationStorageHelper
from twitchAPI.object.eventsub import ChannelFollowEvent
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.type import AuthScope
import asyncio
from dotenv import dotenv_values

config = dotenv_values(".env")

APP_ID = 'your_app_id'
APP_SECRET = 'your_app_secret'
TARGET_SCOPES = [AuthScope.MODERATOR_READ_FOLLOWERS]


async def on_follow(data: ChannelFollowEvent):
    print(f'{data.event.user_name} now follows {data.event.broadcaster_user_name}!')


async def run():
    twitch = await Twitch(APP_ID, APP_SECRET)
    helper = UserAuthenticationStorageHelper(twitch, TARGET_SCOPES)
    await helper.bind()

    user = await first(twitch.get_users())

    eventsub = EventSubWebsocket(twitch)
    eventsub.start()
    
    await eventsub.listen_channel_follow_v2(user.id, user.id, on_follow)
n
    try:
        input('press Enter to shut down...')
    except KeyboardInterrupt:
        pass
    finally:
        await eventsub.stop()
        await twitch.close()


asyncio.run(run())
