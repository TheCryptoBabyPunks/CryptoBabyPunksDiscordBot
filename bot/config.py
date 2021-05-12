import os
import os.path as op


class Config:  
    # Discord
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DISCORD_GUILD = os.getenv('DISCORD_GUILD')
        
    # local
    TEMPLATES_PATH = op.join(op.dirname(__file__), '../templates')

    # Punks Family

    PF_TOKEN = os.getenv('PF_TOKEN')
