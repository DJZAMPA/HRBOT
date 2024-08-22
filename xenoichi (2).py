from highrise import BaseBot, User, Position, AnchorPosition
from highrise.__main__ import *
import highrise, random, asyncio, json
from emotes import Emotes, Dance_Floor
from pickuplines import PUL
import time
from flask import Flask
from keep_alive import keep_alive
keep_alive()
from threading import Thread

class xenoichi(BaseBot):
    def __init__(self):
        super().__init__()

        self.check_players_task = None
        self.emotes = Emotes
        self.pickuplines = PUL
        self.emotesdf = Dance_Floor
        self.active_emote_loops = {}
        self.emote_tasks = {}

        self.dancer = []
        self.on_dance_floor = []
        self.pos1 = None
        self.pos2 = None

        self.vip = []
        self.bot_pos = None
        self.vip_pos = None
        self.dj_pos = None
        self.host_pos = None
        self.down_pos = None 

        self.plines = None

    async def on_start(self, session_metadata):

        print("Xenbot is armed and ready!")

        self.load_loc_data()
        self.load_vip()

        if self.bot_pos:
            await self.highrise.teleport(self.highrise.my_id, self.bot_pos)

        asyncio.create_task(self.dance_floor())

    async def on_chat(self, user: User, message: str) -> None:

        if user.username == "DJ._.ZAMPA" or "JN_JUNGKOOK" or "rythm" or "prettyeyedjenn" or "LatinStar" or "codexne" or "Obito153" or "prettyeyedjenn" or "CHARLEZangel1" or "XCheekyX":

              
            if message.startswith("/emall"):

                try:
                    target_number = message.split("/emall ", 1)[1].strip().lower()
                    await self.highrise.walk_to(self.bot_pos)

                    if target_number.isdigit():
                        target = int(target_number)
                        if target > 91:
                            await self.highrise.chat(f"Invalid Emote.")
                            return
                        else:
                            await self.emote_all_users(target)
                    else:
                        await self.highrise.chat(f"Please provide a valid Emote number.")
                        return

                except Exception as e:
                        print(f"An error occurred: {e}" )               

            if message.startswith("/help"):
                await self.highrise.chat(f"JEJSVS")


        
          
            elif message.startswith("/addvip"):

                try:

                    parts = message.split(" ")
                    if len(parts) != 2:
                        await self.highrise.chat("Invalid command. Usage: /addvip @{username}")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    username_str = target_username[1:]

                    if username_str:

                        if username_str not in self.vip:

                            target_to_add = await self.webapi.get_users(username = username_str, limit=1)
                            if target_to_add.users:
                                target_username = target_to_add.users[0].username
                                await self.highrise.chat(f"@{target_username} has been added as VIP.")
                                self.vip.append(target_username)
                                self.save_vip()
                            else:
                                await self.highrise.chat(f"User not found with the username {username_str}.")
                        else:
                            await self.highrise.chat(f"@{username_str} is already a VIP.")
                            return
                    else:
                        await self.highrise.chat(f"User not found with the username {username_str}.")

                except Exception as e:
                    print(f"add_vip error: {e}")

            elif message.startswith("/removevip"):
                try:

                    parts = message.split(" ")
                    if len(parts) != 2:
                        await self.highrise.chat("Invalid command. Usage: /removevip @{username}")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    username = target_username[1:]

                    if username in self.vip:
                        await self.highrise.chat(f"@{username} has been removed as VIP.")
                        self.vip.remove(username)
                        self.save_vip()
                    else:
                        await self.highrise.chat(f"User not found in VIP list.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            elif message.startswith("/djpos"):
                try:
                    parts = message.split(" ")
                    if len(parts) != 2:
                        await self.highrise.chat("Invalid command. Usage: /teledj @{username}.")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    target_username = target_username[1:]
                    await self.teleport_target_user_to_loc(target_username, self.dj_pos)

                except Exception as e:
                    print(f"error teledj: {e}")

            elif message.lower().startswith("/telehost"):             
                try:

                    parts = message.split(" ")
                    if len(parts) != 2:
                        await self.highrise.chat("Invalid command. Usage: /telehost @{username}.")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    target_username = target_username[1:]
                    await self.teleport_target_user_to_loc(target_username, self.host_pos)

                except Exception as e:
                    print(f"error telehost: {e}")
                    
            elif message.lower().startswith("/teledown"):             
                try:

                    parts = message.split(" ")
                    if len(parts) != 2:
                        await self.highrise.chat("Invalid command. Usage: /teledown @{username}.")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    target_username = target_username[1:]
                    await self.teleport_target_user_to_loc(target_username, self.down_pos)

                except Exception as e:
                    print(f"error teledown: {e}")                
          
            elif message.lower().startswith("/televip"):

                try:

                    parts = message.split(" ")
                    if len(parts) != 2:
                        await self.highrise.chat("Invalid command. Usage: /televip @{username}.")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    target_username = target_username[1:]
                    await self.teleport_target_user_to_loc(target_username, self.vip_pos)

                except Exception as e:
                    print(f"error televip: {e}")

            elif message.lower().startswith("/listvip"):

                try:
                    if self.vip:
                        page_size = 20
                        num_pages = (len(self.vip) + page_size - 1) // page_size

                        try:
                            page_number = int(message.split(" ")[1])
                        except IndexError:
                            page_number = 1
                        except ValueError:
                            await self.highrise.chat("Invalid page number.")
                            return

                        start_index = (page_number - 1) * page_size
                        end_index = start_index + page_size
                        current_page = self.vip[start_index:end_index]

                        if current_page:
                            vip_list = "\n".join(f"{index + start_index + 1}. {user}" for index, user in enumerate(current_page))
                            await self.highrise.chat(f"VIP List (Page {page_number}/{num_pages}):\n{vip_list}")
                        else:
                            await self.highrise.chat("Page not found.")
                    else:
                        await self.highrise.chat("VIP list is empty.")

                except Exception as e:
                    print(f"list_vip_error : {e}")

            elif message.startswith("/vippos"):

                self.vip_pos = await self.get_actual_pos(user.id)
                await self.highrise.chat("VIP position set!")
                await asyncio.sleep(1)
                self.save_loc_data()

            elif message.startswith("/djpos"):

                self.dj_pos = await self.get_actual_pos(user.id)
                await self.highrise.chat("DJ position set!")
                await asyncio.sleep(1)
                self.save_loc_data()

            elif message.startswith("/downpos"):

                self.down_pos = await self.get_actual_pos(user.id)
                await self.highrise.chat("down position set!")
                await asyncio.sleep(1)
                self.save_loc_data()
              

            elif message.startswith("/hostpos"):

                self.host_pos = await self.get_actual_pos(user.id)
                await self.highrise.chat("host position set!")
                await asyncio.sleep(1)
                self.save_loc_data()
              
              
            elif message.startswith("/botpos"):

                self.bot_pos = await self.get_actual_pos(user.id)
                await self.highrise.chat("Bot position set!")
                await asyncio.sleep(1)
                await self.highrise.teleport(self.highrise.my_id, self.bot_pos)
                self.save_loc_data()

            elif message.startswith("/bank"):

                wallet = (await self.highrise.get_wallet()).content
                await self.highrise.chat(f"My bank has {wallet[0].amount} {wallet[0].type}.")

            elif message.startswith("/about"):

                await self.highrise.chat(f"In the grand tapestry of creations, I stand as one amongst the legion of xenbots meticulously fashioned by the skilled hands of @Xenoichi.")
                await asyncio.sleep(2)
                await self.highrise.chat(f"Should thou find thyself in need of bespoke automatons tailored to thy unique desires, I entreat thee to embark upon a quest to seek out my venerable creator, whose prowess in the arcane arts of botcraft knows no bounds.")
          


            elif message.startswith("/pos1"):

                self.pos1 = await self.get_actual_pos(user.id)
                await self.highrise.chat("Position 1 set.")

            elif message.startswith("/pos2"):

                self.pos2 = await self.get_actual_pos(user.id)
                await self.highrise.chat("Position 2 set.")

            elif message.startswith("/check"):

                await self.highrise.chat(f"{self.on_dance_floor}")

            elif message.startswith("/create"):

                if self.pos1 and self.pos2:
                    await self.create_dance_floor()
                    await self.highrise.chat("Dance floor created.")
                    self.pos1 = None
                    self.pos2 = None
                else:
                    await self.highrise.chat("Please set both Position 1 and Position 2 first.")

            elif message.startswith("/plines"):

                try:
                    parts = message.split(" ")
                    if len(parts) != 2:
                        await self.highrise.chat("Invalid command. Usage: /plines {number}")
                        return

                    number_input = parts[1]

                    if not number_input.isdigit():
                        await self.highrise.chat("Invalid input. Please provide a valid number.")
                        return

                    number_of_times = int(number_input)

                    if self.plines:
                        await self.highrise.chat("Command plines is in progress.")
                        return
                    else:
                        self.plines = True
                        await self.highrise.chat("Initiating Pick-up lines. Please wait.")
                        await asyncio.sleep(2)
                        await self.pick_up_lines(number_of_times)
                except Exception as e:
                    print(f"mng error: {e}")

            elif message.startswith("/stop-plines"):

                await self.highrise.chat("Stopping Pick-up lines. Please wait.")
                self.plines = False

            elif message.startswith("/clear-df"):

                self.on_dance_floor = []
                await self.highrise.chat("Dance floor/s removed.")
                self.save_loc_data()

            elif message.startswith("/clear-vip"):

                self.vip = []
                await self.highrise.chat("VIP list cleared.")
                self.save_vip()

            elif message.lower().startswith("/kick"):

                try:

                    parts = message.split(" ")
                    if len(parts) != 2:
                        await self.highrise.chat("Invalid command. Usage: /kick @{username}.")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    target_username = target_username[1:]

                    moderate_key = "kick"
                    await self.moderate_user(target_username, moderate_key)

                except Exception as e:
                    print(f"kick error: {e}")

            elif message.lower().startswith("/ban"):

                try:

                    parts = message.split(" ")
                    if len(parts) != 3:
                        await self.highrise.chat("Invalid command. Usage: /ban @{username} {length}.")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    target_username = target_username[1:]

                    length_input = parts[2]

                    if not length_input.isdigit():
                        await self.highrise.chat("Invalid input. Please provide a valid length.")
                        return

                    length = int(length_input)

                    moderate_key = "ban"
                    await self.moderate_user(target_username, moderate_key, length)

                except Exception as e:
                    print(f"ban error: {e}")

            elif message.lower().startswith("/unban"):

                try:

                    parts = message.split(" ")
                    if len(parts) != 2:
                        await self.highrise.chat("Invalid command. Usage: /unban @{username}.")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    target_username = target_username[1:]

                    moderate_key = "unban"
                    await self.moderate_user(target_username, moderate_key)

                except Exception as e:
                    print(f"unban error: {e}")

            elif message.lower().startswith("/mute"):

                try:

                    parts = message.split(" ")
                    if len(parts) != 3:
                        await self.highrise.chat("Invalid command. Usage: /mute @{username} {length}")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    target_username = target_username[1:]

                    length_input = parts[2]

                    if not length_input.isdigit():
                        await self.highrise.chat("Invalid input. Please provide a valid length.")
                        return

                    length = int(length_input)

                    moderate_key = "mute"
                    await self.moderate_user(target_username, moderate_key, length)

                except Exception as e:
                    print(f"mute error: {e}")


        if message.lower().lstrip().startswith(("-spam", "!spam")):
            await self.highrise.chat("#NSS #NSS")   
        if message.lower().lstrip().startswith(("-spam", "!spam")):
            await self.highrise.chat("#NSS #NSS")   
        if message.lower().lstrip().startswith(( "!spam", "!spam")):
            await self.highrise.chat("#NSS #NSS")

        if message.lower().lstrip().startswith(( "!spam", "!spam")):
            await self.highrise.chat("#NSS #NSS")
              
        if message.startswith("/emote"):
            try:
                target_number = message.split("/emote ", 1)[1].strip().lower()

                if target_number.isdigit():
                    target = int(target_number)
                    if target > 91:
                        await self.highrise.chat(f"Invalid Emote.")
                        return
                    else:
                        emote_text, emote_time = await self.get_emote(target)
                        if emote_text and emote_time:

                            user_id = user.id
                            if user_id in self.emote_tasks:
                                self.emote_tasks[user_id].cancel()

                            task = asyncio.create_task(self.emote_loop(emote_text, emote_time, user_id))
                            self.emote_tasks[user_id] = task
                else:
                    await self.highrise.chat(f"Please provide a valid Emote number.")
                    return
            except Exception as e:
                print(f"An error occurred: {e}")

        elif message.startswith("/stop-emote"):
            # Stop the emote loop for the player
            try:
                if self.active_emote_loops[user.id]:
                    self.active_emote_loops[user.id] = False
                    await self.highrise.send_whisper(user.id, f"Emote loop for @{user.username} stopped.")
            except Exception as e:
                # Handle other exceptions
                print(f"Unexpected error: {e}")

    async def moderate_user(self, target_user, moderate_key, length=None):

        try:

            if moderate_key == "unban":
                target_to_unban = await self.webapi.get_users(username = target_user, limit=1)

                if target_to_unban.users:
                    target_user_id = target_to_unban.users[0].user_id
                else:
                    await self.highrise.chat(f"User with username {target_user} not found.")

                await self.highrise.moderate_room(target_user_id, moderate_key)
                await self.highrise.chat(f"@{target_user} has been successfuly unbanned.")
                return

            if target_user:

                target = await self.get_target_user_in_room(target_user)

                if target:

                    if moderate_key == "kick":
                        await self.highrise.moderate_room(target.id, moderate_key)
                        await self.highrise.chat(f"@{target.username} has been successfully kicked.")

                    elif moderate_key == "ban":
                        await self.highrise.moderate_room(target.id, moderate_key, length)
                        await self.highrise.chat(f"@{target.username} has been successfully banned for {length} seconds.")

                    elif moderate_key == "mute":
                        await self.highrise.moderate_room(target.id, moderate_key, length)
                        await self.highrise.chat(f"@{target.username} has been successfully muted for {length} seconds.")

                else:
                    await self.highrise.chat(f"Username {target_user} is invalid.")

        except Exception as e:
            print(f"moderate_user error: {e}")


    async def get_actual_pos(self, user_id):

        room_users = await self.highrise.get_room_users()

        for user, position in room_users.content:
            if user.id == user_id:
                return position

    async def pick_up_lines(self, number_of_times):

        try:

            for _ in range(number_of_times):

                users_in_room = await self.get_users_in_room()
                users_in_room_except_bot = [user for user in users_in_room if user.id != self.highrise.my_id]

                if self.plines:

                    if users_in_room:

                        target = random.choice(users_in_room_except_bot)

                        if target:

                            targetloc = await self.get_actual_pos(target.id)

                            if isinstance(targetloc, Position):

                                loc_final = Position(targetloc.x + 1, targetloc.y, targetloc.z)
                                if targetloc:

                                    await self.highrise.teleport(self.highrise.my_id, loc_final)
                                    await asyncio.sleep(1)
                                    targetloc = await self.get_actual_pos(target.id)
                                    loc_final = Position(targetloc.x + 2, targetloc.y, targetloc.z, facing="FrontLeft")
                                    await self.highrise.walk_to(loc_final)
                                    await asyncio.sleep(2)
                                    reacts = ('wave', 'heart', 'wink')
                                    ran_reacts = random.choice(reacts)
                                    ran_PUL = random.choice(self.pickuplines)
                                    await self.highrise.react(ran_reacts, target.id)
                                    await self.highrise.chat(f"@{target.username} {ran_PUL}")

                            else:
                                continue    
                else:
                    break

                await asyncio.sleep(5)

            await self.highrise.teleport(self.highrise.my_id, self.bot_pos)
            await self.highrise.chat(f"Pick-up lines stopped.")
            self.plines = False

        except Exception as e:
            await self.highrise.teleport(self.highrise.my_id, self.bot_pos)
            self.plines = False
            print(f"plines error: {e}")

    async def teleport_target_user_to_loc(self, target_username, loc):

        try:
            if target_username:
                target = await self.get_target_user_in_room(target_username)

                if target:

                    if loc:
                        await self.highrise.teleport(target.id, loc)
                        await self.highrise.chat(f"@{target.username} has been successfuly teleported.")
                    else:
                        await self.highrise.chat(f"Target location is not set.")

                else:
                    await self.highrise.chat(f"Username {target_username} is invalid.")
        except Exception as e:
            print(f"teleport_target_user: {e}")

    async def get_target_user_in_room(self, target_username):

        room_users = await self.highrise.get_room_users()
        target_user = next((user for user, _ in room_users.content if user.username == target_username), None)
        return target_user

    async def get_users_in_room(self):

        try:
            room_users = await self.highrise.get_room_users()

            if room_users.content:
                for user in room_users.content:
                    get_user = [user for user, _ in room_users.content]
                    return get_user
            else:
                return []
        except Exception as e:
            print(f"{e}")

    async def get_user_ids_in_room(self):

        try:
            room_users = await self.highrise.get_room_users()

            if room_users.content:
                user_ids = [user.id for user, _ in room_users.content]
                return user_ids
            else:
                return []
        except Exception as e:
            print(f"{e}")

    async def get_emote(self, target) -> None:

        try:
            emote_info = self.emotes.get(target)
            return emote_info
        except ValueError:
            pass

    async def get_emote_df(self, target) -> None:

        try:
            emote_info = self.emotesdf.get(target)
            return emote_info
        except ValueError:
            pass

    async def emote_all_users(self, target):

        try:
            users_in_room = await self.get_users_in_room()
            emote_text, emote_time = await self.get_emote(target)

            if users_in_room:

                emote_all_task = [self.highrise.send_emote(emote_text, user.id) for user in users_in_room]
                await asyncio.gather(*emote_all_task)

            else:
                await self.highrise.chat("No users in the room to emote to.")

        except highrise.ResponseError as e:
                await self.highrise.chat(f"This emote is not free.")

    async def emote_loop(self, emote_text, emote_time, user_id):

        self.active_emote_loops[user_id] = True
        while self.active_emote_loops.get(user_id, False):

            try:
                if not self.active_emote_loops.get(user_id, False):
                    break
                else:
                    await self.highrise.send_emote(emote_text, user_id)
                    await asyncio.sleep(emote_time)

            except highrise.ResponseError as e:

                try:
                    await self.highrise.send_whisper(user_id, f"This emote is not free.")
                    print(f"Error sending freestyle emote: {e}")
                    break
                except highrise.ResponseError as e:
                    print(f"Error sending whisper: {e}")
                    break

              

    async def on_whisper(self, user: User, message: str):

        if user.username == "DJ._.ZAMPA":
            if message.startswith("/chat"):

                chat_message = message.replace("/chat", "", 1)
                await self.highrise.chat(f"{chat_message}")

    async def on_user_move(self, user: User, destination: Position | AnchorPosition) -> None:

        try:
            if user:
                user_pos = destination
                print(f"{user.username}: {destination}")

                # Check if user is in any dance floor area
                if self.on_dance_floor:

                    if isinstance(destination, Position):

                        for dance_floor_info in self.on_dance_floor:

                            if (
                                dance_floor_info[0] <= user_pos.x <= dance_floor_info[1] and
                                dance_floor_info[2] <= user_pos.y <= dance_floor_info[3] and
                                dance_floor_info[4] <= user_pos.z <= dance_floor_info[5]
                            ):

                                if user.id not in self.dancer:
                                    self.dancer.append(user.id)

                                return

                    # If not in any dance floor area
                    if user.id in self.dancer:
                        self.dancer.remove(user.id)
        except Exception as e:
            print(f"on_user_move error: {e}")

    async def create_dance_floor(self):

        # Assuming pos1 and pos2 are set as Position objects
        min_x = min(self.pos1.x, self.pos2.x)
        max_x = max(self.pos1.x, self.pos2.x)
        min_y = min(self.pos1.y, self.pos2.y)
        max_y = max(self.pos1.y, self.pos2.y)
        min_z = min(self.pos1.z, self.pos2.z)
        max_z = max(self.pos1.z, self.pos2.z)

        # Store the square area as a tuple and add it to on_dance_floor list
        dance_floor_pos = (min_x, max_x, min_y, max_y, min_z, max_z)
        self.on_dance_floor.append(dance_floor_pos)
        self.save_loc_data()


    def save_loc_data(self):

        loc_data = {
            'vip_position': {'x': self.vip_pos.x, 'y': self.vip_pos.y, 'z': self.vip_pos.z} if self.vip_pos else None,
            'bot_position': {'x': self.bot_pos.x, 'y': self.bot_pos.y, 'z': self.bot_pos.z} if self.bot_pos else None,
            'dj_position': {'x': self.dj_pos.x, 'y': self.dj_pos.y, 'z': self.dj_pos.z} if self.dj_pos else None,
            'dance_floor': self.on_dance_floor if self.on_dance_floor else None
        }

        with open('loc_data.json', 'w') as file:
            json.dump(loc_data, file)

    def load_loc_data(self):

        try:
            with open('loc_data.json', 'r') as file:
                loc_data = json.load(file)
                self.bot_pos = Position(**loc_data.get('bot_position')) if loc_data.get('bot_position') is not None else None
                self.vip_pos = Position(**loc_data.get('vip_position')) if loc_data.get('vip_position') is not None else None
                self.dj_pos = Position(**loc_data.get('dj_position')) if loc_data.get('dj_position') is not None else None
                self.on_dance_floor = loc_data.get('dance_floor') if loc_data.get('dance_floor') is not None else []
        except FileNotFoundError:
            pass

    def save_vip(self):
        if self.vip_pos:
            with open('vip.json', 'w') as file:
                json.dump({'vip_list': self.vip}, file)

    def load_vip(self):
        try:
            with open('vip.json', 'r') as file:
                vip_data = json.load(file)
                self.vip = vip_data.get('vip_list', [])
        except FileNotFoundError:
            self.vip = []

    async def dance_floor(self):

        while True:

            try:

                if self.on_dance_floor and self.dancer:

                    ran = random.randint(1, 73)
                    emote_text, emote_time = await self.get_emote_df(ran)
                    emote_time -= 1

                    emote_tasks = [self.highrise.send_emote(emote_text, user_id) for user_id in self.dancer]

                    await asyncio.gather(*emote_tasks)
                    await asyncio.sleep(emote_time)

                await asyncio.sleep(1)

            except Exception as e:
                print(f"{e}")



    async def on_user_join(self, user: User, Position):

        print(f"{user.username} joined the room standing at {Position}")

        try:

            if user.username in self.vip:
                await self.highrise.teleport(user.id, self.vip_pos)
            await self.highrise.chat(f"𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙏𝙤 𝙏𝙝𝙚 𝙏𝙞𝙥 𝘼 𝘽𝙖𝙙𝙙𝙞𝙚𝙨 𝙍𝙤𝙤𝙢 @{user.username} 𝘿𝙤𝙣'𝙩 𝙁𝙤𝙧𝙜𝙚𝙩 𝙏𝙤 𝙁𝙤𝙡𝙡𝙤𝙬 𝙔𝙤𝙪𝙧 𝙃𝙤𝙨𝙩 , 𝙑𝙞𝙥𝙨 𝘼𝙣𝙙 𝘿𝙟𝙨 𝙍𝙚𝙖𝙙 𝙍𝙤𝙤𝙢 𝘿𝙚𝙨𝙘𝙧𝙞𝙥𝙩𝙞𝙤𝙣 𝙁𝙤𝙧 𝙍𝙪𝙡𝙚𝙨 𝙍𝙤𝙤𝙢 𝙈𝙖𝙙𝙚 𝙗𝙮 @𝘿𝙅._𝙕𝘼𝙈𝙋𝘼")
            ran = random.randint(1, 73)
            emote_text, emote_time = await self.get_emote_df(ran)
            await self.highrise.send_emote(emote_text, self.highrise.my_id)

        except Exception as e:
            print(f"{e}")

    async def on_user_leave(self, user: User):

        try:
            if user.id in self.dancer:
                self.dancer.remove(user.id)

            await self.highrise.chat(f"left the room @{user.username}.")
            await self.highrise.send_emote("emote-bow", self.highrise.my_id)

      
        except Exception as e:
            print(f"{e}")


