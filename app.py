from flask import Flask, request, redirect, send_from_directory, render_template
from flask_cors import CORS
from array import *
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import os

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
        gChromeOptions = webdriver.ChromeOptions()
        gChromeOptions.add_argument("window-size=1920x1480")
        gChromeOptions.add_argument("disable-dev-shm-usage")
        gDriver = webdriver.Chrome(
            chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install()
        )
        gDriver.get(url)
        #print(gDriver.page_source)
        
        #GET_URL
        pSrc = gDriver.page_source
        gDriver.close()
        
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

    else:
        return 'error'
def getBestQuality(url):
    if url.find('cda.pl/') != -1: 
        gChromeOptions = webdriver.ChromeOptions()
        gChromeOptions.add_argument("window-size=1920x1480")
        gChromeOptions.add_argument("disable-dev-shm-usage")
        gDriver = webdriver.Chrome(
            chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install()
        )
        gDriver.get(url)
        #print(gDriver.page_source)
    
        pSrc = gDriver.page_source
        gDriver.close()

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

    else:
        return 'error'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
