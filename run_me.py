import sys
import tweepy
import re
import time
from selenium import webdriver
from importlib import reload
from getpass import getpass
import sqlite3
from flask import Flask,render_template,request
import sqlite3 as sql
app=Flask(__name__)

reload(sys)

usr = input("Enter your Twitter username or email id: ")
pwd = getpass("Enter password: ")

driver = webdriver.Chrome('/usr/local/share/chromedriver')
driver.get("https://twitter.com/login")

u_box = driver.find_element_by_class_name("js-username-field")
u_box.send_keys(usr)

pwd_box = driver.find_element_by_class_name("js-password-field")
pwd_box.send_keys(pwd)

login_button = driver.find_element_by_css_selector('button.submit.EdgeButton.EdgeButton--primary.EdgeButtom--medium')
login_button.submit()

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
  consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
  token = oauth2.Token(key=key, secret=secret)
  client = oauth2.Client(consumer, token)
  resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
  return content

home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', ACCESS_KEY, ACCESS_SECRET )

con = sqlite3.connect("tweetInfo.db",timeout=10)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS twinfo( createdAt datetime, tids VARCHAR(39) ,textContent VARCHAR(280) , link VARCHAR(280))")



def replace_url_to_link(value):
    urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)
    value = urls.sub(r'<a href="\1" target="_blank">\1</a>', value)
    return value

def open(): 
  con = sqlite3.connect("tweetInfo.db",timeout=10)
  cur = con.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS twinfo( createdAt datetime, tids VARCHAR(39) ,textContent VARCHAR(280) , link VARCHAR(280))")
 
  def extract_url(value):
    urls=re.findall("(?P<url>https?://[^\s]+)", value)
    urls = str(urls)
    return urls
     


  #______________________________________________________________________
  CONSUMER_KEY = 'oIVHi4gTLB84eTnP11FFmoIhN'                           #
  CONSUMER_SECRET= 'LUh6KoVqNqYovytM0DAMabJAM8a5lEllaCCNexBKT1HhgtinJI'#
  ACCESS_KEY = '1394335759-Zx6UwyAatSCrPru4N8UQQ5oIliv2B3OQDjdeh5E'    #
  ACCESS_SECRET = 'puKymVbX1UPKPvgXzvHgVeNhWhCzMQYnXqxrxXePJGDA5'      #
  #-----------------------------------------------------------------------



  tweetList = []

  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
  api = tweepy.API(auth)
  statuses = api.home_timeline()

  #statuses = api.user_timeline('RahulPrksh1',count=400)


  for status in statuses:
    dict={}
    dict['text'] = (status.text)
    dict['id_str'] = status.id_str
    dict['created_at'] = status.created_at
    dict['lins'] = extract_url(status.text)
    dict['user.screen_name'] = status.user.screen_name
    dict['user.name'] = status.user.name
    tweetList.append(dict)
       



  for item in tweetList:
    stam=(item["created_at"])
    fin= item["user.name"]+" (@"+item['user.screen_name']+")"
    findTx=item['text']
    lnks = item['lins']
    

    # lnks = replace_url_to_link(lnks)
    #print(stam,fin,findTx,lnks)
    cur.execute('''INSERT INTO twinfo VALUES(?,?,?,?)''',(stam,fin,findTx,lnks))
    con.commit()
  cur.close()
  con.close()

@app.route('/')
def home():
  open()
  con=sql.connect("tweetInfo.db")
  cur=con.cursor()
  cur.execute("select count(*) from twinfo")
  tot=cur.fetchall()
  tot=tot[0][0]
  cur.close()
  con.close()
  return render_template('home.html',tot=tot)







@app.route('/dash')
def dash():
  open()
  con=sql.connect("tweetInfo.db")
  con.row_factory=sql.Row
  cur=con.cursor()
  cur.execute("")
  cur.execute("select * from twinfo")
  rows=cur.fetchall()
  cur.execute("DELETE from twinfo")
  con.commit()
  con.close()
  return render_template("dash.html",rows=rows)

  cur.close()



if __name__=="__main__":
  app.run(debug=True)





















