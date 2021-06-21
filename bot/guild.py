import discord
import pandas as pd
import emoji
from bs4 import BeautifulSoup
import requests
import logging
import nest_asyncio
from opensea import OpenSeaAPI
from config import Config
from punksfamily import PunksFamilyAPI

nest_asyncio.apply()
client = discord.Client()
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

class DiscordBotResponse:

    def read_template(self, name):
        with open(Config.TEMPLATES_PATH + f'/{name}.txt', 'r') as file:
            return file.read()
            
    def attributes(self, q):
        attributes = []
        for trait in q["traits"]:
            if trait['trait_type']=='Attribute':
                attributes.append(f"{str(trait['value'])} ({trait['trait_count']/10}%)")
        return ', '.join(attributes)
                
    def get_price(self, q):
        coeff = 1000000000000000000
        try:
            if q["sell_orders"]==None:
                price = round(float(q['last_sale']['total_price'])/(coeff), 2)
                symbol = q["last_sale"]["payment_token"]["symbol"]
                tag = 'Last sale price: '
            else: 
                price = round(float(q["sell_orders"][0]["current_price"])/(coeff), 2)
                symbol = q["sell_orders"][0]["payment_token_contract"]['symbol']
                tag = 'Current Price: '
            return tag + str(price) + symbol
        except:
            return 'Undisclosed'
    
    def trait_type(self, q, key):
        try:
            for trait in q["traits"]:
                if trait['trait_type']==key:
                    value = trait['value']
                    trait_count = trait['trait_count']/10
                    attributes = f"{value} ({trait_count}%)"
            return attributes
        except:
            return ':shrug:'

    def get_owner(self, q):
        try:
            owner = q["last_sale"]["transaction"]["from_account"]["user"]["username"]
            if owner!=None:
                return owner
            return ':ghost:'
        except:
            return ':ghost:'

    def get_owner_from_web(self, q):
        url = q["permalink"]
        with requests.get(url) as response:
           html_page = response.content
        soup = BeautifulSoup(html_page, "html.parser")
        owner = soup.find(
            'div', 
            {'class': "AccountLinkreact__DivContainer-sc-4gdciy-0 hJExCK"}
        ).find('a')['href'].split('/')[-1]
        return owner

    def get_family(self, fam, key):
        response = ''
        if key == 'fatherSiblings' or key == 'motherSiblings':
            for punk in fam[key]['children']:
                response += punk['code']+' '
        elif key == 'brothers':
            if len(fam[key]) > 0:
                for punk in fam[key]:
                    response += punk['code']+' '
            else:
                response = 'none'
        return response

    def catalogue(self, q, fam):
        template = self.read_template('retrieve_assets')
        embed = discord.Embed(
            title=f':link: {q["name"]}',
            colour=discord.Colour(0xE5E242),
            url=q["permalink"],
            description=emoji.emojize(
                template.format(
                    name=q["name"],
                    baby_type=self.trait_type(q, 'Baby Type'),
                    attr=self.attributes(q),
                    mother=self.trait_type(q, 'Mother'),
                    father=self.trait_type(q, 'Father'),
                    price=self.get_price(q),
                    brothers=self.get_family(fam, 'brothers'),
                    father_children=self.get_family(fam, 'fatherSiblings'),
                    father_count=fam['fatherSiblings']['count'],
                    mother_children=self.get_family(fam, 'motherSiblings'),
                    mother_count=fam['motherSiblings']['count'],
                    link=fam['link']
                    # owner=self.get_owner(q)
                ))
        )
        embed.set_thumbnail(url=q["image_url"])
        return embed
            
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content in list(df['keys']):
        num = message.content.split('!')[-1]
        token_id = df.loc[df['num'] == num]['token_id'].values[0]
        q = app.assets(token_id)['assets'][0]
        fam = family.get(num)['data']
        embed = bot.catalogue(q, fam) # get info from catalogue!
        await message.channel.send(embed=embed)

if __name__ == "__main__":
    
    df = pd.read_pickle('../data/cryptobabypunks.pkl')
    app = OpenSeaAPI()
    family = PunksFamilyAPI()
    bot = DiscordBotResponse()
    client.run(Config.DISCORD_TOKEN)

