import twitter_login.constants as constants
import oauth2
import urllib.parse as urlparse
import json
from twitter_login.user import User
from twitter_login.database import Database

Database.initialise(database="learning", host="localhost", user="postgres", password="1234")

user_email = input("Enter your email address: ")
user = User.load_from_db_by_email(user_email)
# Create a consumer, which uses the CONSUMER_KEY and CONSUMER_SECRET to identify our app.
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

if not user:
    client = oauth2.Client(consumer)
    # Use the client to perform a request for the request token
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print("An error occurred getting the request token from Twitter!")

    # Get the request token, parsing the string returned.
    request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

    # Ask the user to authorise the app by entering the pin from twitter.
    print("Please visit the following website on your Browser: ")
    print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

    oauth_verifier = input("What is the PIN? ")

    # Create aa token object containing the request token and verifier.
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    # Create a client with the consumer(our app) and newly created and verified token
    client = oauth2.Client(consumer, token)

    # Ask twitter fir the access token, and twitter will comply as we have verified the request token.
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
    print(access_token)
    print("Please provide the details below: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

# create an authorized token object, to do twitter calls on behalf of the user.
authorized_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)
authorized_client = oauth2.Client(consumer, authorized_token)

# Make twitter API Calls
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images', 'GET')
if response.status != 200:
    print('An error occured.')
tweets = json.loads(content.decode('utf-8'))

for tweet in tweets['statuses']:
    print(tweet['text'])
# Checkout dev.twitter.com/rest/public