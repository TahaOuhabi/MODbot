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
    except discord.Forbidden:
        await context.send("Je n'ai pas la permission de créer des salons!")
@bot.command()
@commands.has_permissions(administrator=True)
async def create_voicechannel(context,nom_channel):
    guild=context.guild
    channel=discord.utils.get(guild.channels,name=nom_channel)
    if channel:
        await context.send(f"Salon vocal de nom {nom_channel} existe deja")
        return
    try:
        nouvelle_channel= await guild.create_voice_channel(nom_channel)
        await context.send(f"Salon vocal de nom {nom_channel} créé")
    except discord.Forbidden:
        await context.send("Je n'ai pas la permission de créer des salons!")
@bot.command()
@commands.has_permissions(manage_channels=True)
async def delete_textchannel(context,channel:discord.TextChannel):
    try:
        await channel.delete()
        await context.send(f"Salon de texte {channel.name} effacé")
    except discord.Forbidden:
        context.send(f"J'ai pas la permission d'effectuer cette action")
    except discord.NotFound:
        context.send(f"Salon de texte non trouvé")
@bot.command()
@commands.has_permissions(manage_channels=True)
async def delete_voicechannel(context,channel:discord.VoiceChannel):
    try:
        await channel.delete()
        await context.send(f"Salon vocal {channel.name} supprimé")
    except discord.Forbidden:
        await context.send(f"J'ai pas la permission pour effectuer cette action")
    except discord.NotFound:
        await context.send(f"Salon vocal non trouvé")
@bot.command()
async def commandes(context):
    await context.send(f"\n\n**1- Créer un salon vocal: ?create_voicechannel [nom]**"
                       f"\n\n**2- Créer un salon texte: ?Create_textchanne [nom]**"
                       f"\n\n**3- Supprimer un salon vocal: ?delete_voicechannel [nom]** "
                       f"\n\n**4- Supprimer un Salon texte: ?delete_textchannel [nom]**"
                       f"\n\n**5- afficher les commandes: ?commandes**")




bot.run(token,log_handler=handler,log_level=logging.DEBUG)

