from highrise import BaseBot, User, Position, AnchorPosition
from highrise.__main__ import *
import highrise, random, asyncio, json
from emotes import Emotes, Dance_Floor
from pickuplines import PUL
import time

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

        self.plines = None

    async def on_start(self, session_metadata):

        print("Xenbot is armed and ready!")

        self.load_loc_data()
        self.load_vip()

        if self.bot_pos:
            await self.highrise.teleport(self.highrise.my_id, self.bot_pos)

        asyncio.create_task(self.dance_floor())

    async def on_chat(self, user: User, message: str) -> None:

        if user.username == "DJ._.ZAMPA" or "JN_JUNGKOOK" or "rythm" or "prettyeyedjenn":
               
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
                await self.highrise.chat(f"\nUser Commands:\n/emote\n/stop-emote\n/about\n\nAdmin Commands:\n/tip\n/addvip\n/removevip\n/vippos\n/botpos\n/djpos\n/televip\n/teledj\n/pos1\n/pos2\n/create\n/clear-df\n/clear-vip\n/emall\n/plines")


            elif message.lower().startswith("/tip-all"):

                try:

                    parts = message.split(" ")
                    if len(parts) != 2:
                        await self.highrise.chat("Invalid command. Usage: /tip-all {tip amount}.")
                        return

                    tip_amount_str = parts[1]

                    try:

                        tip_amount = int(tip_amount_str)

                        if tip_amount in (1, 5, 10, 50, 100, 500, 1000, 5000, 10000):

                            if tip_amount == 1:
                                tip = "gold_bar_1"
                            elif tip_amount == 5:
                                tip = "gold_bar_5"
                            elif tip_amount == 10:
                                tip = "gold_bar_10"
                            elif tip_amount == 50:
                                tip = "gold_bar_50"
                            elif tip_amount == 100:
                                tip = "gold_bar_100"
                            elif tip_amount == 500:
                                tip = "gold_bar_500"
                            elif tip_amount == 1000:
                                tip = "gold_bar_1000"
                            elif tip_amount == 5000:
                                tip = "gold_bar_5000"
                            elif tip_amount == 10000:
                                tip = "gold_bar_10000"

                        else:
                            raise ValueError("Invalid tip amount.")

                    except ValueError:
                        await self.highrise.chat("Invalid tip amount. Please provide a valid amount.")
                        return

                    bot_wallet = await self.highrise.get_wallet()
                    bot_amount = bot_wallet.content[0].amount

                    user_in_room = await self.get_users_in_room()

                    if user_in_room:

                        await self.highrise.chat(f"\nTipping all Users {tip_amount} gold. Please wait.")
                        await asyncio.sleep(2)

                        for user_id in user_in_room:

                            if bot_amount < tip_amount:
                                await self.highrise.chat("Not enough funds in bank.")
                                return

                            if user_id.id != self.highrise.my_id:
                                await self.highrise.tip_user(user_id.id, tip)
                                await self.highrise.chat(f"\n@{user_id.username} is tipped {tip_amount} gold!")
                                await asyncio.sleep(1)

                        await self.highrise.chat(f"\nTipping is done.")

                except Exception as e:
                    print(f"error tipping all: {e}")

            elif message.lower().startswith("/tip"):

                try:
                    parts = message.split(" ")
                    if len(parts) != 3:
                        await self.highrise.chat("Invalid command. Usage: /tip @{username} {tip amount}.")
                        return

                    target_username = parts[1]
                    if not target_username.startswith('@'):
                        await self.highrise.chat("Invalid username format. Use '@{username}'.")
                        return

                    target_username = target_username[1:]

                    tip_amount_str = parts[2]

                    target = await self.get_target_user_in_room(target_username)

                    if not target:
                        await self.highrise.chat(f"{target_username} is not in the room.")
                        return

                    try:

                        tip_amount = int(tip_amount_str)

                        if tip_amount in (1, 5, 10, 50, 100, 500, 1000, 5000, 10000):

                            if tip_amount == 1:
                                tip = "gold_bar_1"
                            elif tip_amount == 5:
                                tip = "gold_bar_5"
                            elif tip_amount == 10:
                                tip = "gold_bar_10"
                            elif tip_amount == 50:
                                tip = "gold_bar_50"
                            elif tip_amount == 100:
                                tip = "gold_bar_100"
                            elif tip_amount == 500:
                                tip = "gold_bar_500"
                            elif tip_amount == 1000:
                                tip = "gold_bar_1000"
                            elif tip_amount == 5000:
                                tip = "gold_bar_5000"
                            elif tip_amount == 10000:
                                tip = "gold_bar_10000"

                        else:
                            raise ValueError("Invalid tip amount.")

                    except ValueError:
                        await self.highrise.chat("Invalid tip amount. Please provide a valid amount.")
                        return

                    bot_wallet = await self.highrise.get_wallet()
                    bot_amount = bot_wallet.content[0].amount

                    if bot_amount < tip_amount:
                        await self.highrise.chat("Not enough funds in bank.")
                        return

                    try:
                        await self.highrise.tip_user(target.id, tip)
                        await self.highrise.chat(f"{target_username} has been tipped an amount of: {tip_amount} gold.")

                    except Exception as e:
                        await self.highrise.chat(f"Error tipping {target_username}: {str(e)}")
                except Exception as e:
                    await self.highrise.chat(f"Error tipping: {str(e)}")


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

            elif message.lower().startswith("/teledj"):

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
                    if not target
                            