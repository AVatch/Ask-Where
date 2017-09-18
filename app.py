import logging
import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask
from flask_ask import Ask, request, session, question, statement
from geo import lookup_venue, explore, details, get_locality


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Hey there, where do you want to go?'
    return question(speech_text).reprompt(speech_text).simple_card('Hello', speech_text)


@ask.intent('WhereIntent', mapping={'venue': 'VENUE'})
def where(venue):
    print '*'*50
    print venue
    if venue is None:
        speech_text = 'Sorry, I did not understand the venue name'
        return statement(speech_text).simple_card('HelloWorld', speech_text)

    coords = lookup_venue(venue)
    if coords is None:
        speech_text = 'Sorry, I could not find that'
        return statement(speech_text).simple_card('HelloWorld', speech_text)

    venues = explore(coords['lat'], coords['lng'])
    number_of_venues = len(venues)
    top_hit = venues[0] if number_of_venues > 0 else None

    if top_hit is None:
        speech_text = 'Sorry, I could not find that'
        return statement(speech_text).simple_card('HelloWorld', speech_text)
    
    venue_details = details(top_hit['place_id'])
    venue_locality = get_locality(venue_details)

    speech_text = '{0} is near {1}'.format(
        venue,
        top_hit['name']
    )
    if venue_locality is not None:
        speech_text += ' in {0}'.format(venue_locality)

    return statement(speech_text).simple_card('HelloWorld', speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    # load environment variables
    load_dotenv(join(dirname(__file__), '.env'))
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
