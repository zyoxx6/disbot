import io
import os
import random

import discord
from dotenv import load_dotenv
from discord import  app_commands
from discord.ext import commands
import phonenumbers
from phonenumbers import carrier, timezone, geocoder
import requests
import webserver


load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
intents.members = True
intents.messages = True

secret_role = "Gamer"

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_member_join(member):
    await member.send(f"Hi {member.name} Welcome to our discord server!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} You are not allowed to do that.")
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")

@bot.command()
async def number(ctx, *, num):
    parsed = phonenumbers.parse(num)
    location = geocoder.description_for_number(parsed, 'en')
    time_zone = timezone.time_zones_for_number(parsed)
    num_carrier = carrier.name_for_number(parsed, 'en')

    await ctx.send(f'Your phone number location is `{location}`')
    await ctx.send(f'Your phone number carrier is `{num_carrier}`')
    await ctx.send(f'Your phone number time zone is `{time_zone}`')

@bot.command()
async def catfact(ctx):
    res = requests.get("https://catfact.ninja/fact")
    data = res.json()
    await ctx.send(f"Cat fact **{data['fact']}**")

@bot.command()
async def joke(ctx):
    res = requests.get("http://www.official-joke-api.appspot.com/random_joke")
    data = res.json()
    await ctx.send(f"**{data['setup']}** \n {data['punchline']}")

@bot.command()
async def dog(ctx):
    res = requests.get("https://dog.ceo/api/breeds/image/random")
    data = res.json()['message']
    image_data = requests.get(data).content
    await ctx.send(file=discord.File(io.BytesIO(image_data), filename="dog.jpg"))

@bot.command()
async def assign(ctx, *, role_name=None):
    if not role_name:
        return await ctx.send("Brooo type a role like `!assign VIP` 😭")

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} You are now assigned to {role}")
    else:
        await ctx.send(f"{ctx.author.mention} Role `{role_name}` not found 💀")

@bot.command()
async def cat(ctx):
    res = requests.get("https://api.thecatapi.com/v1/images/search")
    data = res.json()
    cat_url = data[0]['url']

    dl = requests.get(cat_url).content
    await ctx.send(file=discord.File(io.BytesIO (dl), filename="cat.jpg"))

@bot.command()
async def frog(ctx):
    frogs = [
        "https://upload.wikimedia.org/wikipedia/commons/1/12/Green_Frog_02.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/32/Closeup_of_a_Frog%2C_Thailand.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/2e/Green_frog_Pelophylax_clamitans_-_Massachusetts_%28cropped%29.jpg"
    ]
    frog_url = random.choice(frogs)
    img_data = requests.get(frog_url).content
    await ctx.send(file=discord.File(io.BytesIO(img_data), filename="frog.jpg"))

@bot.command()
async def remove(ctx, *, role_name=None):
    if not role_name:
        return await ctx.send("Brooo type a role like `!assign` `VIP` 😭")

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} You are now removed from {role}")
    else:
        await ctx.send(f"{ctx.author.mention} Role `{role_name}` not found 💀")


@bot.command()
@commands.has_role(secret_role)
async def reset(ctx):
    await ctx.send("Resetting bot status")

@reset.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f"{ctx.author.mention} You have no perms dude {error}")

@bot.command()
async def dm(ctx, *, msg):
   await ctx.author.send(f' u said "{msg}"')

@bot.command()
async def reply(ctx, *, msg):
   await ctx.reply(f'This is a reply to your message: `{msg}`')

@bot.command()
async def say(ctx, *, msg):
    await ctx.send(msg, tts=True)


webserver.keep_alive()
bot.run(TOKEN)