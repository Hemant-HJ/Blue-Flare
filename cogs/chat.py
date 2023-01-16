import discord
from discord.ext import commands

from utility import checks, embed

class ChatButton(discord.ui.View):
    def __init__(self, ctx, users, data, mode, embed):
        super().__init__(timeout = 240)
        self.ctx = ctx
        self.users = users
        self.data = data
        self.embed = embed
        self.mode = mode 

    @discord.ui.button(label = 'Confirm', style = discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        for user in self.users:
            data = await self.ctx.bot.mongo.fetch(user)
            if data:
                if self.mode == 'add':
                    data['chat'] += self.data
                elif self.mode == 'remove':
                    data['chat'] -= self.data
                elif self.mode == 'set':
                    data['chat'] = self.data
                elif self.mode == 'reset':
                    data['chat'] = 0

                await self.ctx.bot.mongo.update(user, data)
            else:
                await self.ctx.send(f'<@{user}> have no entry in database.\nPlease add the username first.')

        self.embed.color = discord.Color.green()
        self.embed.title = 'Successful Data Update'
        self.embed.description = 'Following things will be updated.'

        await interaction.response.edit_message(embed = self.embed, view = None)

    @discord.ui.button(label = 'Cancel', style = discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content = f'<@{self.ctx.author.id}> process cancelled.', embed = None, view = None)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message(content = 'You are not allowed to click on the button.', ephemeral = True)
        return True

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_editor()
    @commands.group(invoke_without_command = True)
    async def chat(self, ctx):
        """ Used to change the top weekly chat winners for many user. """
        e = embed.error_embed(ctx, 'Please provide a subcommand. Available subcommands are: \n1.Add\n2.Remove\n3.Set\n4.Reset')

        await ctx.send(embed = e)

    @chat.command(aliases = ('a',))
    async def add(self, ctx, members: commands.Greedy[discord.Member] = None, value: int = None):
        """ Used to add value to specified users. """
        if not members:
            return await ctx.send('Please provide the member(s).')
        if not value:
            return await ctx.send('Please provide the value to add.')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Chat Value', value = f'{value}', inline = True)
        e.add_field(name = 'Mode', value = 'Add', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = ChatButton(ctx, user, value, 'add', e))

    @chat.command(aliases = ('r',))
    async def remove(self, ctx, members: commands.Greedy[discord.Member] = None, value: int = None):
        """ Used to remove value from specified users. """
        if not members:
            return await ctx.send('Please provide the member(s).')
        if not value:
            return await ctx.send('Please provide the value to remove.')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Chat Value', value = f'{value}', inline = True)
        e.add_field(name = 'Mode', value = 'Remove', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = ChatButton(ctx, user, value, 'remove', e))

    @chat.command(aliases = ('s',))
    async def set(self, ctx, members: commands.Greedy[discord.Member] = None, value: int = None):
        """ Used to set donation as specified for specified users.  """
        if not members:
            return await ctx.send('Please provide the member(s).')
        if not value:
            return await ctx.send('Please provide the value to set.')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Chat Value', value = f'{value}', inline = True)
        e.add_field(name = 'Mode', value = 'Set', inline = True)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = ChatButton(ctx, user, value, 'set', e))

    @chat.command(aliases = ('rs',))
    async def reset(self, ctx, members: commands.Greedy[discord.Member] = None):
        """ Used to reset the donation to 0 for specifies members. """
        if not members:
            return await ctx.send('Please provide the member(s).')

        user = [a.id for a in members]
        mentions = '\n'.join([f'<@{a}>' for a in user])

        e = embed.data_update(ctx, 'Donation Update', discord.Color.red())
        e.description = 'Following things will be updated.'
        e.add_field(name = 'Users', value = f'{mentions}', inline = False)
        e.add_field(name = 'Mode', value = 'Reset', inline = False)
        e.add_field(name = 'Responsible Editor', value = f'<@{ctx.author.id}>', inline = False)

        await ctx.send(embed = e, view = ChatButton(ctx, user, 0, 'reset', e))

async def setup(bot):
    await bot.add_cog(Chat(bot))