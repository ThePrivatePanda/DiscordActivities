from discord import embeds
import requests, json, discord
from discord.ext import commands
import config
from string import printable
if any(item in list(config.prefix) for item in printable):
    pass
else:
    print("Prefix contains a character which i cant parse!")
    raise SystemExit

bot = commands.Bot(command_prefix = config.prefix) # I just like this one better
bot.help_command=None
token = config.token

app_ids = {
    "chess": 832012774040141894,
    "fish": 814288819477020702,
    "poker": 755827207812677713,
    "yt": 755600276941176913,
    "betrayal": 773336526917861400
    }

def make(t, vcid):
    t = app_ids[t.lower()]
    url = f"https://discord.com/api/v8/channels/{vcid}/invites"
    body = {
        "max_age": 86400,
        "max_uses": 0,
        "target_application_id": t,
        "target_type": 2,
        "temporary": False,
        "validate": None
    }
    auth = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }

    obj = json.dumps(body, separators=(',', ':'), ensure_ascii=True)
    code = (requests.post(url, json=body, headers=auth))
    code = json.loads(code.text)["code"]

    invite = f"https://discord.gg/{code}"
    return invite

@bot.event
async def on_ready():
    print("Online")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"{config.prefix}help"))

@bot.command(name="play")
async def play(ctx, game):
    voiceChannel = ctx.author.voice.channel
    if voiceChannel != None:
        await ctx.send(make(game, voiceChannel.id))
    else:
        await ctx.send("Connect to VC first")

@bot.command(name="help")
async def help(ctx):
    emb = discord.Embed(title="Help command", description="\u200b")
    emb.add_field(name="command `play`", value=f"Join a voice channel and type out the command `{config.prefix}play <game>` and click on the link which the bot gives.")
    await ctx.send(embed=emb)
@play.error
async def play(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"""
Only 5 games i have now from which you must say:
1) Chess In The Park `chess`
2) Fishington.io `fish`
3) Poker Night `poker`
4) Youtube Together `yt`
5) Betrayal.io `betrayal`

Example usage: `{config.prefix}play poker`
""")
    else:
        await ctx.send("Some error occured.")


bot.run(token)
