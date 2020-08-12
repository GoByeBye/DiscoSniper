import discord
from discord.ext import commands
import asyncio
from colorama import Fore, init
import requests
import datetime
import re

# NOTE: I will be working on adding multiple token support but I made this script in like 5 minutes so it's not going to be anything fancy
# this script is purely a PoC

__version__ = "1.2"
__author = "Daddie0 || https://daddie.xyz"

# Uncomment the line below if you are wanting to host this on heroku and are using an environment variable to store the token.
# token = os.getenv("TOKEN")
# If you are using this on a server or your home pc uncomment the line below and put the discord token for the account you want it to snipe with
token = "ur_token_here"

bot = commands.Bot(command_prefix="$")


@bot.event
async def on_connect():
    print(
        f"""{Fore.GREEN}

 /$$$$$$$  /$$                                /$$$$$$            /$$
| $$__  $$|__/                               /$$__  $$ ︻デ┳═ー  |__/
| $$  \ $$ /$$  /$$$$$$$  /$$$$$$$  /$$$$$$ | $$  \__/ /$$$$$$$  /$$  /$$$$$$   /$$$$$$   /$$$$$$
| $$  | $$| $$ /$$_____/ /$$_____/ /$$__  $$|  $$$$$$ | $$__  $$| $$ /$$__  $$ /$$__  $$ /$$__  $$
| $$  | $$| $$|  $$$$$$ | $$      | $$  \ $$ \____  $$| $$  \ $$| $$| $$  \ $$| $$$$$$$$| $$  \__/
| $$  | $$| $$ \____  $$| $$      | $$  | $$ /$$  \ $$| $$  | $$| $$| $$  | $$| $$_____/| $$
| $$$$$$$/| $$ /$$$$$$$/|  $$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$| $$| $$$$$$$/|  $$$$$$$| $$
|_______/ |__/|_______/  \_______/ \______/  \______/ |__/  |__/|__/| $$____/  \_______/|__/
                                                                    | $$
                                                                    | $$
                                                                    |__/

                                                                    Version > {Fore.RESET}{__version__}
                                                                    {Fore.GREEN}Made by > {Fore.YELLOW}{__author}
{Fore.GREEN}
________________________________________________________________________________________________________

Huston we're online!
Ready to snipe some fucking nitro
=================================
"""
    )


@bot.event
async def on_message(message):
    def NitroData(elapsed, code):
        print(
            f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]"
            f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"
            f"\n{Fore.WHITE} - AUTHOR: {Fore.YELLOW}[{message.author}]"
            f"\n{Fore.WHITE} - ELAPSED: {Fore.YELLOW}[{elapsed}]"
            f"\n{Fore.WHITE} - CODE: {Fore.YELLOW}{code}" + Fore.RESET
        )

    # NOTE: Reused unoptimized code frrom DiscoRape
    # you can find it here
    # https://github.com/GoByeBye/DiscoRape

    time = datetime.datetime.now().strftime("%H:%M %p")
    if "discord.gift/" in message.content:
        start = datetime.datetime.now()
        code = re.search("discord.gift/(.*)", message.content).group(1)

        if len(code) != 16:
            elapsed = datetime.datetime.now() - start
            elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"
            print(
                ""
                f"\n{Fore.RED}[{time} - Fake nitro code detected skipping]{Fore.RESET}"
            )
            NitroData(elapsed, code)
        else:
            headers = {"Authorization": token}

            r = requests.post(
                f"https://discordapp.com/api/v7/entitlements/gift-codes/{code}/redeem",
                headers=headers,
            ).text

            elapsed = datetime.datetime.now() - start
            elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"

            if "This gift has been redeemed already." in r:
                print("" f"\n{Fore.CYAN}[{time} - Nitro Already Redeemed]" + Fore.RESET)
                NitroData(elapsed, code)

            elif "subscription_plan" in r:
                print("" f"\n{Fore.CYAN}[{time} - Nitro Success]" + Fore.RESET)
                NitroData(elapsed, code)

            elif "Unknown Gift Code" in r:
                print(
                    "" f"\n{Fore.CYAN}[{time} - Nitro Unknown Gift Code]" + Fore.RESET
                )
                NitroData(elapsed, code)


bot.run(token, bot=False)
