import discord
from discord.ext import commands
import asyncio
from colorama import Fore, init
import requests
import datetime
import re
import json
import os
import sys


# This will let us do cross platform console clear
def cls():
    os.system("cls" if os.name == "nt" else "clear")
    # NOTE: this will only work with linux and windows unsure about macOSX


# NOTE: I will be working on adding multiple token support but I made this script in like 5 minutes so it's not going to be anything fancy
# this script is purely a PoC
start = datetime.datetime.now()
__version__ = "2.0"
__author = "Daddie0 || https://daddie.xyz"


# NOTE: This is yoinked from DiscoRape once again lmao
with open("./config.json") as f:
    config = json.load(f)

TOKEN = config.get("TOKEN")
PREFIX = config.get("PREFIX")
SNIPER = config.get("SNIPER")
GW = config.get("GIVEAWAY")
SLOT = config.get("SLOT")


# config wiazard for idiots that can't just edit config.json themselves
def run_wizard():
    """Wizard for first start"""
    print("------------------------------------------")
    token = input("Enter your token:\n> ")
    print("------------------------------------------")
    prefix = input("Enter a prefix for your selfbot:\n> ")
    print("------------------------------------------")
    sniper = input("Do you want to snipe discord nitro codes? [y/n]\n> ")
    print("------------------------------------------")
    slot = input("Do you want to automtically yoink slotbot stuff? [y/n]\n> ")
    print("------------------------------------------")
    gw = input("Do you want to automatically join giveaways? [y/n]\n> ")
    data = {
        "TOKEN": token,
        "PREFIX": prefix,
        "SNIPER": sniper,
        "SLOT": slot,
        "GIVEAWAY": gw,
        "NOTE": "To toggle stuff on and off change the y to a n NOTE IT MUST BE LOWERCASE",
    }
    with open("./config.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    print("------------------------------------------")
    print("Restarting...")
    print("------------------------------------------")
    cls()
    os.execv(sys.executable, ["python"] + sys.argv)


# If config token is default run wizard
if TOKEN == "-":
    run_wizard()


# Define shit to optimize speed for nitro commands etc.. on message event
# aka just define shit once instead of for every message


def NitroData(elapsed, code, message):
    print(
        f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]"
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"
        f"\n{Fore.WHITE} - AUTHOR: {Fore.YELLOW}[{message.author}]"
        f"\n{Fore.WHITE} - ELAPSED: {Fore.YELLOW}[{elapsed}]"
        f"\n{Fore.WHITE} - CODE: {Fore.YELLOW}{code}" + Fore.RESET
    )


# Credits to j/ for for giving me code to base this on
def GiveawayData(elapsed, message):
    print(
        f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]"
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]{Fore.RESET}"
        f"\n{Fore.WHITE} - ELAPSED: {Fore.YELLOW}[{elapsed}]{Fore.RESET}"
    )


def SlotBotData(elapsed, message, time):
    print(
        f"\n{Fore.CYAN}[{time} - Yoinked slotbot]"
        f"\n{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]"
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"
        f"\n{Fore.WHITE} - ELAPSED: {Fore.YELLOW}[{elapsed}]"
    )


# Uncomment the line below if you are wanting to host this on heroku and are using an environment variable to store the token.
# TOKEN = os.getenv("TOKEN")
# If you are using this on a server or your home pc uncomment the line below and put the discord token for the account you want it to snipe with
# TOKEN = "ur_token"
# NOTE: This is now obsolete as we have a config.json due to the increased variables

bot = commands.Bot(command_prefix=PREFIX)


@bot.event
async def on_connect():
    guilds = len(bot.guilds)
    users = len(bot.users)

    if SNIPER == "y":
        sniper = "On"
    elif SNIPER == "n":
        sniper = "off"
    else:
        sniper = "Error in configuration"

    if GW == "y":
        giveaway = "On"
    elif GW == "n":
        giveaway = "Off"
    else:
        giveaway = "Error in configuration"

    if SLOT == "y":
        slot = "On"
    elif SLOT == "n":
        slot = "Off"
    else:
        slot = "Error in configuration"

    elapsed = datetime.datetime.now() - start
    elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"
    print(
        f"""{Fore.GREEN}


██████╗ ██╗███████╗ ██████╗ ██████╗ ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
██║  ██║██║███████╗██║     ██║   ██║███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
██║  ██║██║╚════██║██║     ██║   ██║╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
██████╔╝██║███████║╚██████╗╚██████╔╝███████║██║ ╚████║██║██║     ███████╗██║  ██║
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝

                            (⌐■_■)–︻╦╤─

                                                                    Version > {Fore.RESET}{__version__}
                                                                    {Fore.GREEN}Made by > {Fore.YELLOW}{__author}
{Fore.GREEN}
________________________________________________________________________________________________________

Huston we're online!
=================================
Logged in as {Fore.RESET}{bot.user}
{Fore.GREEN}Servers: {Fore.RESET}{guilds}
{Fore.GREEN}Users:  {Fore.RESET}{users}{Fore.GREEN}


Config
- - - - - - - - - - - - - - - - -
NitroSniper: {Fore.RESET}{sniper}{Fore.GREEN}
GiveawaySniper: {Fore.RESET}{giveaway}{Fore.GREEN}
SlotSniper: {Fore.RESET}{slot}{Fore.GREEN}

=================================

Finished start up in {Fore.RESET}{elapsed}{Fore.GREEN} second(s)
We're ready to snipe shit
"""
    )


@bot.event
async def on_message(message):

    # NOTE: Reused unoptimized code frrom DiscoRape
    # you can find it here
    # https://github.com/GoByeBye/DiscoRape

    time = datetime.datetime.now().strftime("%H:%M %p")
    if "discord.gift/" in message.content:
        if SNIPER == "y":
            start = datetime.datetime.now()
            code = re.search("discord.gift/(.*)", message.content).group(1)

            if len(code) != 16:
                elapsed = datetime.datetime.now() - start
                elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"
                print(
                    ""
                    f"\n{Fore.RED}[{time} - Fake nitro code detected skipping]{Fore.RESET}"
                )
                NitroData(elapsed, code, message)
            else:
                headers = {"Authorization": TOKEN}

                r = requests.post(
                    f"https://discordapp.com/api/v7/entitlements/gift-codes/{code}/redeem",
                    headers=headers,
                ).text

                elapsed = datetime.datetime.now() - start
                elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"

                if "This gift has been redeemed already." in r:
                    print(
                        ""
                        f"\n{Fore.CYAN}[{time} - Nitro Already Redeemed]" + Fore.RESET
                    )
                    NitroData(elapsed, code, message)

                elif "subscription_plan" in r:
                    print("" f"\n{Fore.CYAN}[{time} - Nitro Success]" + Fore.RESET)
                    NitroData(elapsed, code, message)

                elif "Unknown Gift Code" in r:
                    print(
                        ""
                        f"\n{Fore.CYAN}[{time} - Nitro Unknown Gift Code]" + Fore.RESET
                    )
                    NitroData(elapsed, code, message)
        else:
            return

    if "Someone just dropped" in message.content:
        if SLOT == "y":
            start = datetime.datetime.now()
            if message.author.id == 123067977615540225:
                try:
                    await message.channel.send("~grab")
                except Exception as e:
                    print(f"Error while trying to yoink slotbot shit\nError: {e}")
                elapsed = datetime.datetime.now() - start
                elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"
                SlotBotData(elapsed, message, time)
        else:
            return

    if "GIVEAWAY" in message.content:
        if GW == "y":
            if message.author.id == 123067977615540225:
                start = datetime.datetime.now()
                try:
                    await message.add_reaction("🎉")
                    print("" f"\n{Fore.CYAN}[{time} - Giveaway Joined!]" + Fore.RESET)
                    elapsed = datetime.datetime.now() - start
                    elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"
                    GiveawayData(elapsed, message)
                except Exception as e:
                    print(f"Error while trying to join giveaway\nError: {e}")
        else:
            return

    if f"Congratulations <@!{bot.user.id}>" in message.content:
        if message.author.id == 123067977615540225:
            start = datetime.datetime.now()
            print(f"\n{Fore.CYAN}[{time} - Giveaway won! 🎉🎉🎉{Fore.RESET}")
            elapsed = datetime.datetime.now() - start
            elapsed = f"{elapsed.seconds}.{elapsed.microseconds}"
            GiveawayData(elapsed, message)
    else:
        return


bot.run(TOKEN, bot=False)
