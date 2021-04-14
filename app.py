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
    gChromeOptions = webdriver.ChromeOptions()
    gChromeOptions.add_argument("window-size=1920x1480")
    gChromeOptions.add_argument("disable-dev-shm-usage")
    gDriver = webdriver.Chrome(
        chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install()
    )
    gDriver.get("https://www.python.org/")
    print(gDriver.page_source)
    gDriver.close()
            
    return render_template('home.html')
    

if __name__ == '__main__':
    app.run(host="0.0.0.0")
