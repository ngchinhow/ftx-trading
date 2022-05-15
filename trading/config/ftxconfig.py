from ftx import Client
from FTX.settings import ENV_FTX_API_KEY, ENV_FTX_SECRET_KEY


client = Client(ENV_FTX_API_KEY, ENV_FTX_SECRET_KEY)
