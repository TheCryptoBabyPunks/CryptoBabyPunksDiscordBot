FROM python:3.8-buster

COPY bots/guild.py /bots/
COPY bots/opensea.py /bots/
COPY bots/config.py /bots/
COPY data/cryptobabypunks.pkl data/
COPY templates/retrieve_assets.txt templates/
COPY requirements.txt /tmp
RUN pip install --upgrade cython && \
    pip3 install -r /tmp/requirements.txt


WORKDIR /bots
CMD ["python3", "guild.py"]