import discord
from discord.ext import commands

from utility import checks, embed

class UsernameButton(discord.ui.View):
    def __init__(self, ctx, user, username, mode, embed):
        super().__init__(timeout = 240)
        self.ctx = ctx
        self.user = user
        self.username = username
        self.mode = mode
        self.embed = embed

    @discord.ui.button(label = 'Confirm', style = discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.mode == 'set':
            data = await self.ctx.bot.mongo.fetch(self.user.id)
            if data:
                data['username'] = self.username
            else:
                data = self.ctx.bot.mongo.mainstr
                data['username'] = self.username
            await self.ctx.bot.mongo.update(self.user.id, data)
            self.embed.title = 'Successful Data Update'
            self.embed.description = 'The following data has been updated.'
            self.embed.color = discord.Color.green()

            await interaction.response.edit_message(embed = self.embed, view = None)
        
        elif self.mode == 'reset':
            data = await self.ctx.bot.mongo.fetch(self.user.id)
            if data:
                data['username'] = 'Not Set'
            else:
                data = self.ctx.bot.mongo.mongo.datastructure
            await self.ctx.bot.mongo.update(self.user.id, data)
            self.embed.title = 'Successful Data Update'
            self.embed.description = 'Following user\'s data have been reseted.'
            self.embed.color = discord.Color.green()
            
            await interaction.response.edit_message(embed = self.embed, view = None)

    @discord.ui.button(label = 'Cancel', style = discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content = f'<@{self.ctx.author.id}> process cancelled.', embed = None, view = None)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message(content = 'You are not allowed to click on the button.', ephemeral = True)
        return True

class Username(commands.Cog):
    """Use this to interact with the username in the database."""
    def __init__(self, bot):
        self.bot = bot

    @checks.is_editor()
    @commands.group(invoke_without_command = True, aliases = ('un',))
    async def username(self, ctx):
        """ Used to change the username of any user. """
        e = embed.error_embed(ctx, 'Please provide a subcommand. Available subcommands are: \n1.Set\n2.Reset')
        
        return await ctx.send(embed = e)

    @username.command(aliases = ('s',))
    async def set(self, ctx, user: discord.Member = None, username: str = None):
        """ Used to set the username for a user. """
        if not user:
            return await ctx.send('Please provide the user.')
        if not username:
            return await ctx.send('Please provide the username.')
        
        e = embed.data_update(ctx, 'Username Update', discord.Color.red())
        e.description = 'The following things will be updated.'
        e.add_field(name = 'User', value = f'<@{user.id}>', inline = False)
        e.add_field(name = 'Value', value = username.title(), inline = False)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)
        
        await ctx.send(embed = e, view = UsernameButton(ctx, user, username, 'set', e))

    @username.command(aliases = ('rs',))
    async def reset(self, ctx, user: discord.Member = None):
        """ Used to reset the username of a user. """
        if not user:
            return await ctx.send('Please provide the user.')
        
        e = embed.data_update(ctx, 'Username Update', discord.Color.red())
        e.description = 'The username of the user will be reseted.'
        e.add_field(name = 'User', value = f'<@{user.id}>', inline = False)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = UsernameButton(ctx, user, 'None', 'reset', e))

async def setup(bot):
    await bot.add_cog(Username(bot))