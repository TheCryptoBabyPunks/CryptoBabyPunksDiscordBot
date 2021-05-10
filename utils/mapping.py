from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

url = "http://www.cryptobabypunks.com/allcryptobabypunks.html"

def main():
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "html.parser")
    images = soup.findAll('img')
    links = soup.findAll('a')[:-1]
    tb = []
    for image, link in zip(images, links):
        id = link.get('href').split('/')[-1]
        num = image['alt'].split('#')[-1]
        key = str('!' + num)
        tb.append(
            (id, image['alt'], num, key, link.get('href'))
        )
    
    return pd.DataFrame.from_records(tb, columns=[
        'token_id', 'name', 'num', 'keys', 'link'])

if __name__ == "__main__":

    df = main()
    df.to_pickle('../data/cryptobabypunks.pkl')
