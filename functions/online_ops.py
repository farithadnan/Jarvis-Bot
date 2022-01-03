import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

NEWS_API_KEY = config("NEWS_API_KEY")
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
TMDB_API_KEY = config("TMDB_API_KEY")
EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")


# ipify provides a simple public IP address API. We just need to make a GET request on this URL: https://api64.ipify.org/?format=json. 
def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

# For searching on Wikipedia, we'll be using the wikipedia module that we had installed
def search_on_wikipedia(query):
    #  summary() method that accepts a query as an argument. Additionally, we can also pass the number of sentences required. Then we simply return the result.
    results = wikipedia.summary(query, sentences=2)
    return results

# For playing videos on YouTube, we are using PyWhatKit. We have already imported it as kit
def play_on_youtube(video):
    # PyWhatKit has a playonyt() method that accepts a topic as an argument. It then searches the topic on YouTube and plays the most appropriate video. It uses PyAutoGUI under the hood
    kit.playonyt(video)

# using PyWhatKit to search thru google search
def search_on_google(query):
    kit.search(query)

# pyWhatKit once again for sending WhatsApp messages
def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+6{number}", message)

# For sending emails, we will be using the built-in smtplib module from Python
def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


# Function on getting latest news
# we're first creating an empty list called news_headlines. We are then making a GET request on the API URL specified in the NewsAPI Documentation.
def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]

# Since the news is contained in a list called articles, we are creating a variable articles with the value res['articles']. Now we are iterating over this articles list and appending the article["title"] to the news_headlines list. We are then returning the first five news headlines from this list.


# Function to fetch latest weather
def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"


# Fetch trending movies
def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]

# Fetch random joke
def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

# Random advice
def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']