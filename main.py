from flask import Flask
from threading import Thread
from highrise.__main__ import *  # Ensure the necessary imports from highrise
import time
from importlib import import_module
from asyncio import run as arun

class WebServer:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index() -> str:
            return "Funcionando"

    def run(self) -> None:
        self.app.run(host='0.0.0.0', port=8080)

    def keep_alive(self):
        t = Thread(target=self.run)
        t.start()

class RunBot:
    room_id = "66f415af909919e249920aa0"
    bot_token = "c2aea350339802a562ec32a9a7b86a66a27405ee660247f9ae9f178e40da18b0"
    bot_file = "xenoichi"
    bot_class = "xenoichi"

    def __init__(self) -> None:
        self.definitions = [
            BotDefinition(
                getattr(import_module(self.bot_file), self.bot_class)(),
                self.room_id, self.bot_token)
        ]  # More BotDefinition classes can be added to the definitions list

    def run_loop(self) -> None:
        while True:
            try:
                arun(main(self.definitions))
            except Exception as e:
                print("Error: ", e)
                time.sleep(5)

if __name__ == "__main__":
    # Start the Flask web server
    WebServer().keep_alive()

    # Start the bot
    RunBot().run_loop()
