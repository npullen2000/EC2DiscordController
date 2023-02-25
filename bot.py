import discord, boto3
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

region = os.getenv('region')
instance_ids = os.getenv('instance_ids')
discord_guild_ids = os.getenv('discord_guild_ids')
discord_bot_token = os.getenv('discord_bot_token')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/',intents = intents)
ec2 = boto3.resource('ec2', region_name= region)
instance = ec2.Instance(instance_ids)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command(name="serverstop", guild_ids=[discord_guild_ids])
async def serverstop(ctx):
    if getInstanceState() == "stopped":
        await ctx.channel.send('Minecraft Server is currently shutdown.')
    else:
        turnOffInstance()
        await ctx.channel.send('Minecraft Server has been stopped!')

@bot.command(name="serverstart", guild_ids=[discord_guild_ids])
async def serverstart(ctx):
    if getInstanceState() == "running":
        await ctx.channel.send('Minecraft Server is already running!')
    elif getInstanceState() == "stopped":
        turnOnInstance()
        await ctx.channel.send('Minecraft Server has been started.')
    else:
        await ctx.channel.send('An error occurred, please check the log files or reboot the bot')
@bot.command(name="serverstatus", guild_ids=[discord_guild_ids])
async def serverstatus(ctx):
    if getInstanceState():
        await ctx.channel.send("Minecraft Server is " + getInstanceState())
    else:
        await ctx.channel.send("An error occured, please check the log files or reboot the bot")

@bot.command(name="serverreboot", guild_ids=[discord_guild_ids])
async def rebootInstance(ctx):
    if getInstanceState() == "stopped":
        await ctx.channel.send("Minecraft server is currently shutdown, please type /serverstart to start the server")
    elif getInstanceState() == "running":
        await ctx.channel.send("Server is rebooting, type /serverstatus for server status")
    else:
        ctx.channel.send("An error occured, please check the log files or reboot the bot.")

def turnOffInstance():
    try:
        instance.stop()
        return True
    except:
        return False

def turnOnInstance():
    try:
        instance.start()
        return True
    except:
        return False

def getInstanceState():
    return instance.state['Name']

def rebootInstance():
    try:
        instance.reboot()
        return True
    except:
        return False

bot.run(discord_bot_token)
