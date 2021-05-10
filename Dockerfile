FROM python:3.8-buster

COPY bots/guild.py /bot/
COPY bots/opensea.py /bot/
COPY bots/config.py /bot/
COPY data/cryptobabypunks.pkl data/
COPY templates/retrieve_assets.txt templates/
COPY requirements.txt /tmp
RUN pip install --upgrade cython && \
    pip3 install -r /tmp/requirements.txt


WORKDIR /bot
CMD ["python3", "guild.py"]
