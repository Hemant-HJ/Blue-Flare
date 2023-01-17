from discord.ext import commands

class NotEditor(commands.CheckFailure):
    pass

def is_editor():
    def predicate(ctx):
        data = ctx.bot.mongo.setting.find_one({'_id': 1})
        if ctx.author.id not in data['editors']:
            raise NotEditor('You are not a editor.')
            return False
        return True
    return commands.check(predicate)