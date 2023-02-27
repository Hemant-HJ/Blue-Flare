import random
import asyncio
from contextlib import suppress

import discord
from discord.ext import commands 

class WTP(commands.Cog):
    """Used to play Who's That Pokemon."""
    def __init__(self, bot):
        self.bot = bot
        self.unanswered = 0
        self.channel = []
        self.ch_trivia = []
        self.un_trivia = 0 

    async def get_img(self):
        poke_id = random.randint(1, 900)
        img_h = f'https://raw.githubusercontent.com/Hemant-HJ/whosthatpokemon/main/images/hidden/{poke_id:>03}.png'
        img_r = f'https://raw.githubusercontent.com/Hemant-HJ/whosthatpokemon/main/images/revealed/{poke_id:>03}.png'
        
        return img_h, img_r, poke_id

    async def get_name(self, url):
        async with self.bot.session.get(url) as response:
            return await response.json(content_type=None)

    @commands.command(aliases = ('trivias', 'tr',))
    async def trivia(self, ctx, time:int = 1):
        """Can start a round of trivia."""

        if ctx.channel.id in self.ch_trivia:           
            return await ctx.send('This command is already running in this channel.')

        self.ch_trivia.append(ctx.channel.id)
        for times in range(time):
            
            id = await self.get_img()
            data = self.bot.trivia[str(id[2])]

            e = discord.Embed(
                title = 'Guess the Pokemon.',
                description = f'{data["que"]}',
                color = discord.Color.red(),
                timestamp = discord.utils.utcnow()
        )
            msg = await ctx.send(embed = e)

            def check(msg):
                return msg.channel.id == ctx.channel.id

            attempt = 0
            while attempt != 3:
                try:
                    guess = await ctx.bot.wait_for('message', timeout = 10, check = check)
                except asyncio.TimeoutError:
                    attempt = 3
                    e = discord.Embed(
                        title = 'You were not able to guess the right answer.',
                        description = f"It was **{data['name']}**\nRemaining:{time - times - 1}",
                        color = discord.Color.red(),
                        timestamp = discord.utils.utcnow()
                    )
                
                    self.un_trivia += 1
                    await ctx.send(embed = e)

                    if self.unanswered == 3:
                        e = discord.Embed(
                            title = 'Game Stopped',
                            description = "Trivia game has been stopped because of 3 unanswered question you can restart it using the command.\n\n`bf wtp <count = 1>`",
                            timestamp = discord.utils.utcnow(),
                            color = discord.Color.red()
                        )
                        self.ch_trivia.remove(ctx.channel.id)
                        self.un_trivia = 0

                        return await ctx.send(embed = e)
                        
                    elif time + 1 == times:
                        return
                    else:
                        continue
                
                if guess.content.lower() in data['name']:
                    attempt = 3
                    right_ans = True
                    self.un_trivia = 0
                else:
                    attempt += 1
                    right_ans = False
                
                if attempt == 3:
                    e = discord.Embed(
                        title = f'{guess.author.name} got it right!!' if right_ans else 'You were not able to guess the right answer.',
                        description = f"It was **{data['name']}**\nRemaining:{time - times - 1}",
                        color = discord.Color.green() if right_ans else discord.Color.red(),
                        timestamp = discord.utils.utcnow()
                        )
                    
                    await ctx.send(embed = e)

            await asyncio.sleep(2)
        self.ch_trivia.remove(ctx.channel.id)
        self.un_trivia = 0

    @commands.command()
    async def wtp(self, ctx, time: int = 1):
        """Command that allow you to start a Who's That Pokemon game."""
        if ctx.channel.id in self.channel:
           
            return await ctx.send('This command is already running in this channel.')
        self.channel.append(ctx.channel.id)
        for times in range(time):
            
            imgs = await self.get_img()

            e = discord.Embed(
                title = "Who's That Pokemon.",
                description = "Guess the pokemon within 30secs. You get 3 chances to guess.",
                color = discord.Color.red(),
                timestamp = discord.utils.utcnow()
            )
            e.set_image(url = imgs[0])

            msg = await ctx.send(embed = e)

            species_data = await self.get_name(f'https://pokeapi.co/api/v2/pokemon-species/{imgs[2]}')
            names = species_data.get('names', [{}])
            eligible_names = [x["name"].lower() for x in names]
            english_name = [x["name"] for x in names if x["language"]["name"] == "en"][0]

            def check(msg):
                return msg.channel.id == ctx.channel.id

            attempt = 0
            while attempt != 3:
                try:
                    guess = await ctx.bot.wait_for('message', timeout = 10, check = check)
                except asyncio.TimeoutError:
                    attempt = 3
                    e = discord.Embed(
                        title = 'You were not able to guess the right answer.',
                        description = f"It was **{english_name}**\nRemaining:{time - times - 1}",
                        color = discord.Color.red(),
                        timestamp = discord.utils.utcnow()
                    )
                    e.set_image(url = imgs[1])
                    self.unanswered += 1
                    await ctx.send(embed = e)
                    if self.unanswered == 3:
                        e = discord.Embed(
                            title = 'Game Stopped',
                            description = "Who's that Pokemon game has been stopped because of 3 unanswered question you can restart it using the command.\n\n`bf wtp <count = 1>`",
                            timestamp = discord.utils.utcnow(),
                            color = discord.Color.red()
                        )
                        self.channel.remove(ctx.channel.id)
                        self.unanswered = 0

                        return await ctx.send(embed = e)
                        
                    elif time + 1 == times:
                        return
                    else:
                        continue
                
                if guess.content.lower() in eligible_names:
                    attempt = 3
                    right_ans = True
                    self.unanswered = 0
                else:
                    attempt += 1
                    right_ans = False
                
                if attempt == 3:
                    e = discord.Embed(
                        title = f'{guess.author.name} got it right!!' if right_ans else 'You were not able to guess the right answer.',
                        description = f"It was **{english_name}**\nRemaining:{time - times - 1}",
                        color = discord.Color.green() if right_ans else discord.Color.red(),
                        timestamp = discord.utils.utcnow()
                        )
                    e.set_image(url = imgs[1])
                    await ctx.send(embed = e)

            await asyncio.sleep(2)
        self.channel.remove(ctx.channel.id)
        self.unanswered = 0

async def setup(bot):
    await bot.add_cog(WTP(bot))