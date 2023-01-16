import discord
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.group(aliases = ('ow','o', 'dev'))
    async def owner(self, ctx):
        pass

    @owner.command(aliases = ('ae',))
    async def add_ed(self, ctx, user:discord.Member = None):
        if not user:
            return await ctx.reply('Where is the user argument.')
        user = user or ctx.author
        data = self.bot.mongo.setting.find_one({'_id': 1})
        if data:
            if user.id not in data['editors']:
                data['editors'].append(user.id)
                self.bot.mongo.setting.update_one({'_id': 1}, {'$set': data})
            else:
                return await ctx.send('User already in the list.')
        else:
            new_data = self.bot.mongo.settingstr
            new_data['editors'].append(user.id)
            self.bot.mongo.setting.insert_one(new_data)
        await ctx.send(f'<@{user.id}> added as admin of database.')

    @owner.command(aliases = ('re',))
    async def remove_ed(self, ctx, user:discord.Member = None):
        if not user:
            return await ctx.reply()
        data = self.bot.mongo.setting.find_one({'_id': 1})
        if data:
            if user.id not in data['editors']:
                new_data = data['editors'].remove(user.id)
                self.bot.mongo.setting.update_one({'_id': 1}, {'$set': new_data})
            else:
                return await ctx.send('User is not in list.')
        else:
           return
        await ctx.send('<@{user.id}> removed as admin of database.')

    @owner.command(aliases = ('r',))
    async def reload(self, ctx, cog:str = None):
        if not cog:
            for cogs in self.bot.lcog:
                await self.bot.reload_extension(cogs)
        else:
            await self.bot.reload_extension(cog if 'cogs.' in cog else f'cogs.{cog.lower()}')
        return await ctx.send('Cogs reloaded.')

    @owner.command(aliases = ('u',))
    async def unload(self, ctx, cog:str = None):
        if not cog:
            for cogs in self.bot.locog:
                await self.bot.unload_extension(cogs)
        else:
            await self.bot.unload_extension(cog if 'cogs.' in cog else f'cogs.{cog.lower()}')
        return await ctx.send('Cogs unloaded.')

    @owner.command(aliases = ('l',))
    async def load(self, ctx, cog:str = None):
        if not cog:
            for cogs in self.bot.locog:
                await self.bot.load_extension(cogs)
        else:
            await self.bot.load_extension(cog if 'cogs.' in cog else f'cogs.{cog.lower()}')
        return await ctx.send('Cogs loaded.')

async def setup(bot):
    await bot.add_cog(Owner(bot))