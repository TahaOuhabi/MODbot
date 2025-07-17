import discord
from aiohttp.web_routedef import delete
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
load_dotenv()
token=os.getenv('DISCORD_TOKEN')
handler=logging.FileHandler(filename='discord.log',encoding='UTF-8',mode='w')
intents=discord.Intents.default()
intents.message_content=True
intents.members=True
intents.polls=True
permissions=discord.Permissions.administrator
bot=commands.Bot(command_prefix='?', intents=intents)
@bot.event
async def on_ready():
    print(f"{bot.user.name} IS READY TO GOOO!!!!")
@bot.event
async def on_member_join(member):
    channel=discord.utils.get(member.guild.channels,name="general")
    if channel:
        await channel.send(f"Bienvenu Au Serveur {member.name} !🎉")
    else:
        print(f"Salon {channel.name} introuvable sur {member.guild.name}")
import json
with open('package.json','r') as fichier:
    donnees=json.load(fichier)
    gros_mots=donnees["gros_mots"]
    greetings=donnees["greetings"]
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if any(mot in message.content.lower() for mot in gros_mots):
        await message.delete()
        await message.channel.send(f"{message.author.mention} On est entre gens civilisés ici, les jurons passent à la trappe ! 😉")
    elif any(mot.lower() in message.content.lower() for mot in greetings):
        await message.channel.send(f"Salut {message.author.mention} ! 👋")
    await bot.process_commands(message)
@bot.command()
@commands.has_permissions(administrator=True)
async def create_textchannel(context,nom_channel):
    guild=context.guild
    channel=discord.utils.get(guild.channels,name=nom_channel)
    if channel:
        await context.send(f"Salon de texte existe deja")
        return
    try:
        nouvelle_channel= await guild.create_text_channel(nom_channel)
        await context.send(f"Salon textuel de nom {nom_channel} créé")
@bot.command()
@commands.has_permissions(admninistrator=True)
async def create_voicechannel(context,nom_channel):
    guild=context.guild
    channel=discord.utils.get(guild.channels,name=nom_channel)
    if channel:
        await context.send(f"Salon vocal de nom {nom_channel} existe deja")
        return
    try:
        nouvelle_channel= await guild.create_voice_channel(nom_channel)
        await context.send(f"Salon vocal de nom {nom_channel} créé")




bot.run(token,log_handler=handler,log_level=logging.DEBUG)

