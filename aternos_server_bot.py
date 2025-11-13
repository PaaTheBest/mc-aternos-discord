import discord
import os
import time
from python_aternos import Client

# ------------------------------
# LOAD ENVIRONMENT VARIABLES
# ------------------------------

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_USERNAME = os.getenv("ATERNOS_USERNAME")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")
ATERNOS_SERVER = os.getenv("ATERNOS_SERVER")  # optional if you want

client = discord.Client()

# ------------------------------
# LOGIN TO ATERNOS SAFELY
# ------------------------------

aternos = Client(ATERNOS_USERNAME, password=ATERNOS_PASSWORD)
atservers = aternos.servers
myserv = atservers[0]  # First server in account


# ------------------------------
# DISCORD BOT EVENTS
# ------------------------------

@client.event
async def on_ready():
    print(f"We are logged in as {client.user}")


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)

    if message.author == client.user:
        return

    if channel == "bot-cmnds":

        # hello command
        if user_message.lower() == "?hello":
            await message.channel.send(f"Hello {username}!")
            return

        # START SERVER
        if user_message.lower() == "?server_start":
            myserv.start()
            await message.channel.send("Starting server... please wait 2–3 minutes.")

            # OPTIONAL: ping loop
            while True:
                time.sleep(1)
                ping = str(os.popen(f"mcstatus {ATERNOS_SERVER} status | grep description").read())
                if "offline" in ping:
                    continue
                else:
                    break

            await message.channel.send(f"Server is online: **{ATERNOS_SERVER}**")
            return

        # STOP SERVER
        if user_message.lower() == "?server_stop":
            myserv.stop()
            await message.channel.send("Server stopped.")
            return


# ------------------------------
# RUN DISCORD BOT
# ------------------------------
client.run(DISCORD_TOKEN)
