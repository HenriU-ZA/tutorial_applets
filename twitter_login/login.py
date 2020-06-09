from twitter_login.user import User
from twitter_login.database import Database
from twitter_login.twitter_utils import get_request_token, get_oauth_verifier, get_access_token

Database.initialise(database="learning", host="localhost", user="postgres", password="1234")

user_email = input("Enter your email address: ")
user = User.load_from_db_by_email(user_email)

if not user:
    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    print("Please provide the details below: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images')

for tweet in tweets['statuses']:
    print(tweet['text'])

# Checkout dev.twitter.com/rest/public
