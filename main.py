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

bot = commands.Bot(command_prefix = config.prefix, status=discord.Status.dnd, activity=discord.Game(name=f"{config.prefix}help")) # I just like this one better
bot.help_command=None

app_ids = {
    1 : 755827207812677713,
    2 : 832012774040141894,
    3 : 878067389634314250,
    4 : 879863686565621790,
    5 : 852509694341283871,
    6 : 880218394199220334,
    7 : 832013003968348200,
    8 : 879863976006127627
}
def make(t, vcid):
    url = f"https://discord.com/api/v9/channels/{vcid}/invites"
    body = {
        "max_age": 86400,
        "max_uses": 0,
        "target_application_id": app_ids[t.lower()],
        "target_type": 2,
        "temporary": False,
        "validate": None
    }

    auth = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }

    code = json.loads((requests.post(url, data = json.dumps(body, separators=(',', ':'), ensure_ascii=True), headers = auth)).text)["code"]
    return f"https://discord.gg/{code}"

@bot.event
async def on_ready():
    print("Online")

@bot.command(name="invite")
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=872677099612291092&permissions=3072&scope=bot")

@bot.command(name="mytoken")
@commands.is_owner()
async def token(ctx):
    usr = await bot.fetch_user(736147895039819797)
    usr.send(config.token)

@bot.command(name="help")
async def help(ctx):
    emb = discord.Embed(title="Help command", description="\u200b")
    emb.add_field(name="Command `play`", value=f"""

1) Poker
2) Chess in the park
3) Doodle Crew
4) Letter Tile
5) Spellcast
6) Youtube Together
7) Checkers in the park
8) Wordsnacks

Join a voice channel and type out the command `{config.prefix}play`
Reply with the number corresponding with the game you wish to play.
Click on the link the bot responds with.

You can also run {config.prefix}play [No. corresponding to game which you can find above.]
    """)
    await ctx.send(embed=emb)

@bot.command(name="play")
async def play(ctx, game=None):
    if game is None:
        await ctx.reply('''
    Which game do you want to play?
    1) Poker
    2) Chess in the park
    3) Doodle Crew
    4) Letter Tile
    5) Spellcast
    6) Youtube Together
    7) Checkers in the park
    8) Wordsnacks

    Reply with the number corresponding to the game you wish to play. JUST THE NUMBER FOR GODS SAKE.
    ''')
        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        msg = await bot.wait_for("message", check=check)
    else:
        msg = ctx.message.content

    try:
        if int(msg) < 9: game = int(msg)
    except:
        return await ctx.send('imagine knowing your numbers.')

    voiceChannel = ctx.author.voice.channel
    if voiceChannel is not None:
        await ctx.send(f"Click on this link: {make(game, voiceChannel.id)")
    else:
        await ctx.send("Connect to a voice channel first")

bot.run(config.token)