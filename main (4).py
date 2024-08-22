import sys
import os
import time
import traceback
from importlib import import_module
from highrise.__main__ import *

# BOT SETTINGS
bot_file_name = "xenoichi"
bot_class_name = "xenoichi"
room_id = "65e93ab505782ba2fe3745c7"
bot_token ="559e0fc1599e679b49704bd55939f00dc57057a41a976826d52afebcee9b22ad"

my_bot = BotDefinition(getattr(import_module(bot_file_name), bot_class_name)(), room_id, bot_token)

while True:
    try:
        definitions = [my_bot]
        arun(main(definitions))
    except Exception as e:
        print(f"An exception occurred: {e}")
        traceback.print_exc()
    time.sleep(5)

