import typing

import discord
from discord.ext import commands

from utility import checks

class Admin(commands.Cog):
    """Strictly for Bot Admins or Editors."""
    def __init__(self, bot):
        self.bot = bot

    @checks.is_editor()
    @commands.group(invoke_without_command = True, aliases = ('ad',))
    async def admin(self, ctx):
        """Can only be used by existing editors."""
        e = discord.Embed(
            title = 'Available commands.',
            description = 'set, list',
            color = discord.Color.green()
        )
        await ctx.send(embed = e)

    @admin.command()
    async def set(self, ctx, user:discord.Member = None,key:str = None, value:typing.Union[str, int] = None):
        """Subcommand used to set a value to any key of the user.
        Syntax : bf admin set <user> <key> <value>
            user: Any member of the server.
            key: Any in the List [username, win, lose, draw, chat]
            value: Any new valid value.
        """
        data = await self.bot.mongo.update(user.id, {key:value})
        if data:
            e = discord.Embed(
                title = f'User Update {user.name}',
                description = f"Changed following value: \n{key}: {value}",
                color = discord.Color.green(),
                timestamp = discord.utils.utcnow()
            )
            e.add_field(name = 'Responsible editor', value = f'<@{ctx.author.id}>')

            return await ctx.send(embed = e)

    @admin.command()
    async def list(self, ctx):
        """List all the editors."""
        user = self.bot.mongo.setting.find_one({'_id': 1})['editors']
        if user:
            user = [f'<@{a}>' for a in user]
            e = discord.Embed(
                title = 'All editors.',
                description = f"{', '.join(user)}", 
                timestamp = discord.utils.utcnow(),
                color = discord.Color.blurple()
            )
            return await ctx.send(embed = e)
        return await ctx.send('No editors found.')

async def setup(bot):
    await bot.add_cog(Admin(bot))