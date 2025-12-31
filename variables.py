from os import getenv
import discord
from discord.ext import commands
from dotenv import load_dotenv
from mistralai import Mistral
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = f"mongodb+srv://184706a:{getenv("MONGO")}@cluster0.8tydecd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi("1"))

agent = Mistral(api_key=getenv("MISTRAL_KEY"))

intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.members = True

bot = commands.Bot(command_prefix="?", intents=intents)
guild: discord.Guild = discord.Object(id=int(getenv("GUILD_ID")))

owner = int(getenv("OWNER"))