from flask import Flask, request, redirect, send_from_directory, render_template
from flask_cors import CORS
from array import *
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os

driverPath = 'C:/php'

CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
GOOGLE_CHROME_BIN = os.environ.get('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome')


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    title = 'error'

    if 'textareaInput' in request.form :

        requestedURL = request.form['textareaInput']
        quality = getBestQuality(requestedURL)

        dataset = []

        if quality.find('p') == -1:
            quality = '1080p'
        
        requestedURL = requestedURL + '?wersja=' + quality
     
        dataset = getUrl(requestedURL)
        for i in dataset:
            print(i)

        generatedLink = dataset[0]
        
        if generatedLink.find('https://'):
            title = 'error, try again with proper link'
            dl = False

        else:
            title = dataset[1]
            dl = True
            
        return render_template('home.html', dlReady = dl, generatedLink = generatedLink, title = title )

    else:
        return render_template('home.html')
    

def getUrl(url):
    if url.find('cda.pl/') != -1: 

        try:
            chrome_options = Options()
            chrome_options.binary_location = GOOGLE_CHROME_BIN
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

            #GET_URL
            pSrc = driver.page_source
        
            x = pSrc.find('.mp4')
            a = x - 125                         #~~url
            b = x + 4                           #.mp4 => +4
            print(x)                            #.mp4 on charNo
        
            cutSrc = pSrc[a:b]                  #cut
            print(cutSrc)
        
            y = cutSrc.find('https://')         #obtaining charNo of https...mp4
            url = cutSrc[y:]        
        
            print(url)

            #GET_TITLE
            titleStart = pSrc.find('<h1>')
            titleEnd = pSrc.find('</h1>')
            titleStart=titleStart+4

            title = pSrc[titleStart:titleEnd]

            data = [0 for i in range(2)] 

            data[0] = url
            data[1] = title
            print(data)
            print(type(data))
            return data
        
        except WebDriverException:
            print("failed to start driver at path: " + driverPath)
            return 'error'
    
    else:
        return 'error'


def getBestQuality(url):
    if url.find('cda.pl/') != -1: 

        try:
            chrome_options = Options()
            chrome_options.binary_location = GOOGLE_CHROME_BIN
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        
            pSrc = driver.page_source
        
            ssP = pSrc.find('class="quality-txt"')
            ssK = ssP + 650                                               
            print(ssP)
            cutSrc = pSrc[ssP:ssK]    
    
            print(cutSrc)

            if cutSrc.find('1080') != -1:
                return '1080p'
            if cutSrc.find('720') != -1:
                return '720p'

            return '480p'
        
        except WebDriverException:
            print("failed to start driver at path: " + driverPath)
            return 'error'
    
    else:
        return 'error'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
