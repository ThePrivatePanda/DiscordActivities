from nextcord import embeds
import nextcord
from nextcord.utils import utcnow
import asyncio
import aiohttp
import json
from nextcord.ext import commands
from nextcord import Status
import config

status_dict = {"dnd": Status.dnd, "idle": Status.idle, "online": Status.online, "offline": Status.offline}

class Dropdown(nextcord.ui.Select):
    def __init__(self):

        options = [
            nextcord.SelectOption(label='Poker', description='Play Poker!'),
            nextcord.SelectOption(label='Chess in the park', description='Play Chess!'),
            nextcord.SelectOption(label='Doodle Crew', description='Basically scribbl.io'),
            nextcord.SelectOption(label='Letter Tile', description='A game like skrabble!'),
            nextcord.SelectOption(label='Spellcast', description='A unique game, play it and see!'),
            nextcord.SelectOption(label='Youtube Together', description='Watch youtube together, everyone can access the controls.'),
            nextcord.SelectOption(label='Watch Together', description='Watch youtube together, only the host can control.'),
            nextcord.SelectOption(label='Checkers in the park', description='Play checkers!'),
            nextcord.SelectOption(label='Wordsnacks', description='Another unique discord VC Game, try it out!'),
            nextcord.SelectOption(label='Betrayal.io', description='The VC version of the web version.'),
            nextcord.SelectOption(label='Fishington.io', description='The VC version of the web version.')
        ]

        super().__init__(placeholder='Choose the game you wish to play.', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        async with interaction.channel.typing():
            # await interaction.response.send_message(f'discord.gg/{await make(interaction.user)}')
            pass

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(Dropdown())

bot = commands.Bot(
    command_prefix=config.prefix,
    status=status_dict.get(config.status, Status.online),
    activity=nextcord.Game(name=config.activity),
    help_command=None)

app_ids = {
    1 : 755827207812677713,
    2 : 832012774040141894,
    3 : 878067389634314250,
    4 : 879863686565621790,
    5 : 852509694341283871,
    6 : 880218394199220334,
    7 : 832013003968348200,
    8 : 879863976006127627,
    9 : 773336526917861400,
    10 : 814288819477020702
}

async def make(t, vcid):
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
        "Authorization": f"Bot {config.token}",
        "Content-Type": "application/json",
    }
    resp = await bot.session.post(url, data = json.dumps(body, separators=(',', ':'), ensure_ascii=True), headers = auth)
    code = await resp.json()["code"]
    # code = json.loads((requests.post(url, data = json.dumps(body, separators=(',', ':'), ensure_ascii=True), headers = auth)).text)["code"]
    return f"https://discord.gg/{code}"

@bot.event
async def on_ready():
    print("Online")

@bot.command(name="invite")
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=19457&scope=bot")

@bot.command(name="help")
async def help(ctx):
    emb = nextcord.Embed(
        title="Help command",
        colour=nextcord.Colour.blue())

    emb.add_field(name="Command `play`:", value=f"""
1) Poker:`poker`, `pokernight`
-  Play Poker! 

2) Chess in the park: `chess`
- Play Chess!

3) Doodle Crew: `skribble`, `doodle`, `dc`
- Basically skribbl.io

4) Letter Tile: `scrabble`, `lt`
- A game like scrabble! 

5) `Spellcast`:
- desc

6) Youtube Together: `ytt`, `youtube`
- Everyone can access, i.e. add/remove video, play/pause etc.

7) Watch Together: 'wt', 'watchyt'
- Only host can access, host can share or hand over the \"remote\".

8) Checkers in the park: `checkers`
- Play Checkers! 

9) `Wordsnacks`: `ws`, `wordsnakes`
-  A unique discord VC Game, try it out!

10) Betrayal.io: `btrio`, `btr`, `betrayal`
-  The VC version of the web version.

11) Fishington.io: `fish`, `fishington`, `ftio`
- The VC version of the web version.

""")
    emb.add_field(name="Usage", value=f"Join a voice channel and type out the command `{config.prefix}play`\nSelect the game you want to play from the **dropdown** and **click on the link the bot responds with**.", inline=False)
    emb.set_footer(icon_url=ctx.author.avatar.url)
    emb.set_thumbnail(url=bot.user.avatar.url)
    emb.timestamp = utcnow()
    await ctx.reply(embed=emb)


# @bot.command(name="play")
# async def play(ctx, game=None):


async def startup():
    async with aiohttp.ClientSession() as session:
        bot.session = session
        bot.run(config.token)

asyncio.run(startup)