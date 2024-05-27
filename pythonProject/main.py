import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import asyncio
import pytz
from timezonefinder import TimezoneFinder
from datetime import datetime
from geopy.geocoders import Nominatim
from discord.utils import get

load_dotenv()
token = ''
bossID = 0

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
geolocator = Nominatim(user_agent="discord_bot")
tf = TimezoneFinder()
quotes = [
    "Nie ma rzeczy niemożliwych, są tylko trudne do wykonania.",
    "Każdy dzień jest nową szansą, by zmienić swoje życie.",
    "Nigdy nie rezygnuj z celu tylko dlatego, że osiągnięcie go wymaga czasu. Czas i tak upłynie.",
    "Sukces to suma małych wysiłków powtarzanych dzień po dniu.",
    "Życie zaczyna się tam, gdzie kończy się strach."
]


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('Hej'):
        await message.reply('siemanko')

    if message.content == 'test':
        await message.add_reaction('\U0001F4A9')

    # reakcja jak antyśmieszek coś napisze
    role = discord.utils.find(lambda r: r.name == 'ANTY_SMIESZEK', message.author.guild.roles)
    if role in message.author.roles:
        await message.add_reaction('\U0001F921')



    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    # jak ktoś coś napiszę i ja dam reakcję
    if reaction.emoji == '\U0001F6AB' and user.id == bossID:
        role = get(user.guild.roles, name='ANTY_SMIESZEK')
        await reaction.message.reply('BUU Nie jesteś zabawny')
        await reaction.message.author.add_roles(role)
    elif reaction.emoji == '\U0001F6AB': #jak ja coś napiszę
        if reaction.message.author.id == bossID:
            await reaction.message.reply("HAHAHAH MEGA ZABAWNE")





@bot.command(name='cytat')
async def send_quote(ctx):
    quote = random.choice(quotes)
    await ctx.send(quote)


@bot.command(name='timenow')
async def time_now(ctx, *, city: str):
    location = geolocator.geocode(city)

    if not location:
        await ctx.send(f'Nie znaleziono miasta {city}. Sprawdź poprawność nazwy miasta.')
        return

    lat = location.latitude
    lng = location.longitude
    timezone_str = tf.timezone_at(lng=lng, lat=lat)

    if timezone_str is None:
        await ctx.send(f'Nie można znaleźć strefy czasowej dla {city}.')
        return

    try:
        timezone = pytz.timezone(timezone_str)
        now = datetime.now(timezone)
        await ctx.send(f'Obecna godzina w {city} to {now.strftime("%Y-%m-%d %H:%M:%S")}')
    except Exception as e:
        await ctx.send(f'Wystąpił błąd podczas uzyskiwania czasu dla {city}: {str(e)}')


@bot.command(name='przypomnij')
async def remind(ctx, time: int, *, reminder_message: str):
    await ctx.send(f'Ok, przypomnę Ci o: {reminder_message} za {time} sekund.')
    await asyncio.sleep(time)
    await ctx.send(f'Przypomnienie: {reminder_message}')


bot.run(token)
