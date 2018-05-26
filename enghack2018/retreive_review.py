from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib

import pandas as pd

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


API_KEY= "u4Pj955LuiXx28W-Idr_Px8_l0kXOOMfjlNWAdQcXFp_yH7tRKy4346_ZymdjqM3R5AEI7xnatx18qd-AcwKtKB9CXi2xBMxUWtK7uymgMtUGXfflNxmP-ISmO8IW3Yx"


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = 'food'
DEFAULT_LOCATION = 'Toronto, ON'
SEARCH_LIMIT = 60

def set_term(category):
    DEFAULT_TERM = category
    return


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        #'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)



def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)



def queri_api_for_business_info(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']
    response = get_business(API_KEY, business_id)
    print(response)
    business_df = pd.DataFrame.from_dict(response, orient='index')
    business_df = business_df.transpose()
    
    for x in range(1, len(businesses)):
    	business_id = businesses[x]['id']
    	response = get_business(API_KEY, business_id)
    	business_df=business_df.append(response, ignore_index=True)

    print(business_df)

    id_list=business_df['id'].tolist()

    return id_list


    # for business in businesses:
    # 	id_business = business['id']
    # 	response = get_business(API_KEY, business_id)
    # 	df.append(response)


    # business_id = businesses[0]['id']

    # print(u'{0} businesses found, querying business info ' \
    #     'for the top result "{1}" ...'.format(
    #         len(businesses), business_id))
    # response = get_business(API_KEY, business_id)

    # print(u'Result for business "{0}" found:'.format(business_id))
    # pprint.pprint(response, indent=2)

def get_reviews(ids):
	"""
	Queries yelp API to pass in id for reviews
	considers rating for sentiment analysis

	build df with reviews and 

	"""
	columns=['id', 'review', 'rating']
	df_=pd.DataFrame(columns=columns)

	for busi_id in ids:
		response = get_business(API_KEY, busi_id +'/reviews')
		_reviews =response['reviews']
		#print(_reviews)

		for x in range(3):
			review_string = _reviews[x]['text']
			buss_rating = _reviews[x]['rating']
			df_entry={'id':busi_id, 'review':review_string, 'rating':buss_rating}
			df_=df_.append(df_entry, ignore_index=True)

	print(df_)
	df_.to_csv('reviews_and_ids.csv', sep=',')




def main():

    set_term("food")

    parser = argparse.ArgumentParser(description='Get location and catgory')

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')
    
    input_values = parser.parse_args()

    try:
        list_of_ids=queri_api_for_business_info(input_values.term, input_values.location)

    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )

    get_reviews(list_of_ids)



if __name__ == '__main__':
    main()
