# ------------------------------------------------------------------------------- #

import discord
from dhooks import Webhook
from dhooks import Embed
from discord.ext import commands
from termcolor import colored
from colorama import Fore, init
import asyncio, json
import traceback
from datetime import datetime, timedelta
import requests
import json

# ------------------------------------------------------------------------------- # SET PREFIX

bot = commands.Bot(command_prefix='+')

# ------------------------------------------------------------------------------- # SET LOGGER

def sprint(text):
    print(colored(f"[{datetime.now().strftime('%H:%M:%S')}] - [R2Riccardo - Footlocker Order Checker] - {text}", 'yellow'))
def sprint2(text):
    print(colored(f"[{datetime.now().strftime('%H:%M:%S')}] - [R2Riccardo - Footlocker Order Checker] - {text}", 'red'))

# ------------------------------------------------------------------------------- # LOG

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Footlocker Order Checker, +help'))
    sprint('Logged in as')
    sprint(bot.user.name)
    sprint(bot.user.id)
    sprint('prouldy made by @R2Riccardo#2002')
    sprint('------')

# ------------------------------------------------------------------------------- # REMOVE STANDARD HELP MESSAGE

bot.remove_command('help')

# ------------------------------------------------------------------------------- # PING

@bot.command(aliases=['Ping'])
async def ping(ctx):
    ping = discord.Embed(colour =3997605, title = 'Pong! :ping_pong:', description = (f'`Bot latency:`\n{round(bot.latency * 1000)} ms'))
    ping.set_thumbnail(url="https://avatars.githubusercontent.com/u/47792964?s=460&u=918fe41f6a6c442dc10434baf4ed2bdeaf61b10f&v=4")
    ping.set_footer(text="Footlocker Order Checker", icon_url='https://avatars.githubusercontent.com/u/47792964?s=460&u=918fe41f6a6c442dc10434baf4ed2bdeaf61b10f&v=4')
    ping.timestamp = datetime.utcnow()
    await ctx.send(embed=ping) 

# ------------------------------------------------------------------------------- # HELP

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="**Footlocker Order Checker**", description="`+ping` - use this to check helper status\n \n`+ftlcheck 'ordernumber'` - use this to automatically check your order status on Footlocker", color=3997605)
    embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/47792964?s=460&u=918fe41f6a6c442dc10434baf4ed2bdeaf61b10f&v=4")
    embed.set_footer(text="Footlocker Order Checker", icon_url='https://avatars.githubusercontent.com/u/47792964?s=460&u=918fe41f6a6c442dc10434baf4ed2bdeaf61b10f&v=4')
    embed.timestamp = datetime.utcnow()

    await ctx.send(embed=embed)

# ------------------------------------------------------------------------------- # FTL ORDER CHECKER

@bot.command(pass_context=True)
async def ftlcheck(ctx, sku):

    headers = {
    'authority': 'footlocker.narvar.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en;q=0.9'
    }

    url = 'https://footlocker.narvar.com/tracking/itemvisibility/v1/footlocker/orders/' + sku + '?order_number=' + sku + '&tracking_url=https%3A%2F%2Ffootlocker.narvar.com%2Ffootlocker%2Ftracking%2Fuk-mail%3Forder_number%' + sku + ' '
    response = requests.get(url, headers=headers, timeout=10)
    content = response.json()

    name = content["order_info"]["order_items"][0]["name"]
    image = content["order_info"]["order_items"][0]["item_image"]
    status = content["order_info"]["order_items"][0]["fulfillment_status"]

    embed = discord.Embed(title="**Footlocker Order Checker**", color=3997605)
    embed.add_field(name='Product', value=name, inline=False)
    embed.add_field(name='Order Link', value=f'[Click Here!](https://footlocker.narvar.com/footlocker/tracking/uk-mail?order_number={sku})', inline=False)
    embed.add_field(name='Order ID', value=f'||{sku}||', inline=True)
    embed.add_field(name='Order Status', value=status, inline=True)
    embed.set_thumbnail(url='http://www.footlocker.com' + image + '')
    embed.set_footer(text="Footlocker Order Checker", icon_url='https://avatars.githubusercontent.com/u/47792964?s=460&u=918fe41f6a6c442dc10434baf4ed2bdeaf61b10f&v=4')
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed=embed)

# ------------------------------------------------------------------------------- #

bot.run('bot-token-here')