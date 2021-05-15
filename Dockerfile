FROM python:3.8-buster

COPY bot/guild.py /bot/
COPY bot/opensea.py /bot/
COPY bot/punksfamily.py /bot/
COPY bot/config.py /bot/
COPY data/cryptobabypunks.pkl data/
COPY templates/retrieve_assets.txt templates/
COPY requirements.txt /tmp
RUN pip install --upgrade cython && \
    pip3 install -r /tmp/requirements.txt


WORKDIR /bot
CMD ["python3", "guild.py"]
