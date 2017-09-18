
"""
"""
import os
import requests


def lookup_venue(query):
    """Uses Google Places API to lookup a query
    and map it to a lat / lon coordinates

    @input query:string
    @returns {lat:float, lng:float }
    """
    payload = {
        'key': os.environ.get('GOOGLE_KEY'),
        'query': query
    }

    res = requests.get(
        'https://maps.googleapis.com/maps/api/place/textsearch/json',
        params=payload
    )

    res = res.json()
    venues = res['results']

    if len(venues) < 1:
        return None

    top_hit = venues[0]
    return top_hit['geometry']['location']


def explore(lat, lng):
    """Uses the Google Places API to lookup
    popular venues around the provided coordinats
    """
    TYPES_TO_IGNORE = [
        'administrative_area_level_1',
        'administrative_area_level_2',
        'administrative_area_level_3',
        'administrative_area_level_4',
        'administrative_area_level_5',
        'colloquial_area',
        'country',
        'finance',
        'floor',
        'food',
        'general_contractor',
        'geocode',
        'intersection',
        'locality',
        'neighborhood',
        'place_of_worship',
        'political',
        'post_box',
        'postal_code',
        'postal_code_prefix',
        'postal_code_suffix',
        'postal_town',
        'premise',
        'room',
        'route',
        'street_address',
        'street_number',
        'sublocality',
        'sublocality_level_4',
        'sublocality_level_5',
        'sublocality_level_3',
        'sublocality_level_2',
        'sublocality_level_1',
        'subpremise',
    ]

    payload = {
        'key': os.environ.get('GOOGLE_KEY'),
        'location': '{0},{1}'.format(str(lat), str(lng)),
        'radius': 500
    }

    res = requests.get(
        'https://maps.googleapis.com/maps/api/place/nearbysearch/json',
        params=payload
    )

    res = res.json()
    venues = res['results']
    venues = [venue for venue in venues if len(set(TYPES_TO_IGNORE).intersection(venue['types'])) == 0 ]

    if len(venues) < 1:
        return []

    return venues


def details(placeid):
    """Uses Google Places API to lookup
    the details of a place
    """
    payload = {
        'key': os.environ.get('GOOGLE_KEY'),
        'placeid': placeid
    }
    res = requests.get(
        'https://maps.googleapis.com/maps/api/place/details/json',
        params=payload
    )

    res = res.json()
    
    return res['result']

def get_locality(place_details):
    """Parses the Google Places API Details response
    """
    LOCALITY_TYPE = 'sublocality'
    address_components = place_details['address_components']

    for component in address_components:
        if LOCALITY_TYPE in component['types']:
            return component['long_name']

    return None