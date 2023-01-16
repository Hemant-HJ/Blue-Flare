import discord
import pymongo
from discord.ext import commands

import config

class DataStructure:
    mainstr = {
        'username': 'Not Set',
        'win': 0,
        'lose': 0,
        'draw': 0,
        'chat': 0,
        'donation': 0
    }
    settingstr = {
        '_id': 1,
        'editors': [724447396066754643]
    }
    def __init__(self):
        self.client = pymongo.MongoClient(config.MONGO_URI)
        self.db = self.client['BlueFlare']
        self.main = self.db['Main']
        self.setting = self.db['setting']

class Mongo(commands.Cog, DataStructure):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    async def insert(self, data: dict):
        data = self.main.insert_one(data)
        return data

    async def fetch(self, _id):
        data = self.main.find_one({'_id': _id})
        return data

    async def update(self, _id, data: dict):
        data = self.main.update_one({'_id': _id}, {'$set': data}, upsert = True)
        return True

    async def delete(self, _id):
        data = self.main.delete_one({'_id': _id})
        return 

async def setup(bot):
    await bot.add_cog(Mongo(bot))