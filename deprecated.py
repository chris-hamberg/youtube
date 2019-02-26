'''
import youtube

type help(youtube) in the interactive shell for help and usage
'''
from decimal import Decimal
from pprint import pprint
import requests, json, sys

# --- YOUR API KEY GOES IN THE QUOTES HERE --- #
API_KEY = ''
# -------------------------------------------- #

class SearchAPI:
    '''
    This class lets the user build an api query string, and sends the 
    authenticated request to the youtube api. The response is a JSON
    containing the requested data.

    The api request generated is specific for returning the videos by top view 
    counts.
        
        Methods:
        
        - get_request: 
            sends the api call (url request) to the youtube server.
        
        - set_country: 
            add the url parameter to filter by region.

        - set_keyword: 
            add the url parameter to filter by search term, ex. 'taco'

        - set_date: 
            add the url parameter to filter by a  specific day.

        - clear_params:
            clears out all parameters, resetting the url string to its default 
            state.

        ex. syntax:

            ex. 1
            caller = Request(API_KEY)
            caller.set_country('japan')
            caller.set_date(4, 28, 2011)
            caller.get_request(10)

            will return a json with the top 10 videos by view count
            in Japan on the date 4/28/2011
             - the name "caller" can be any name you want.

            ex. 2
            caller.set_keyword('taco bell')
            caller.get_request()

            returns a json with the top 5 videos relevant to the phrase
            'taco bell'. 5 is the default value for get_request

            ex. 3
            caller.set_keyword('dogs')
            caller.clear_params()
            caller.set_keyword('cats')
            caller.get_request(17)

            returns the top 17 videos for cats

        note:

            the api request is not actually sent to the server until get_request 
            is called on the caller object (named 'caller' in the example).

            every get_request call resets the url parameters to their 
            default state after it returns the data from youtube.
    '''
    def __init__(self, key):
        '''
        initialization requires a google API key.

        the API key is a python string data type.
        '''
        self.base   = 'https://www.googleapis.com/youtube/v3/'
        self.key    = '&key={}'.format(key)
        self.spec   = 'search?part=snippet&order=viewCount&type=video'
        self.params = ''
        self.categories = dict()
        self.region_code = 'us'
        self.json = None
        self.data = dict()

    def show_data(self):
        pprint(self.data)

    def get_data(self, num_results=5):
        self.json = self.get_request(num_results)['items']
        self._get_statistics()
        self.clear_params()

    def get_request(self, num_results=5):
        '''
        send the request to youtube. the default request will return
        a response containing the top num_results for all of youtube.
        
        num_results is an integer or string python data type.
        the num_results max value is 50 as specified by the youtube
        api documentation.

        the response is returned as a JSON (python dict.)
        '''
        try:
            response  = requests.get('%s%s%s%s%s'%(
                    self.base, 
                    self.spec,
                    self.params,
                    '&maxResults={}'.format(num_results),
                    self.key))
        except Exception as e:
            print(str(e))
        else:
            return json.loads(response.text)

    def set_country(self, country):
        '''
        Add a country name to the url parameters. 
        
        country is a python string.
        '''
        iso_3166 = self._get_region_code(country)
        self.region_code = iso_3166
        self.params += '&regionCode={}'.format(iso_3166)
        
    def set_keyword(self, keyword):
        '''
        Add a keyword (search term) to the url parameters. 
        
        region is a python string.
        '''
        self.params += '&q={}'.format(keyword)

    def set_date(self, month, day, year, 
                month_end=None, day_end=None, year_end=None):
        '''
        Add a filter by specific day, to the url parameters.

        day, month, and year can be python ints or strings.
        single digit values do not begin with zero for int.
        '''
        if month_end == None: month_end = month
        if day_end == None: day_end = day
        if year_end == None: year_end = year
        date   = '{}-{}-{}'
        before = date.format(year_end, month_end, day_end)+'T23%3A59%3A59Z'
        after  = date.format(year, month, day)+'T00%3A00%3A00Z'
        self.params += '&publishedBefore={}&publishedAfter={}'.format(
                before, after)

    def set_category(self, id_, region_code=None):
        id_ = str(id_)
        self._set_region_and_get_ids(region_code)
        try:
            # validation step
            self.categories[id_]
        except KeyError:
            self._bad_category(id_, region_code)
        else:
            self.spec += '&videoCategoryId={}'.format(id_)

    def show_category_names(self, region_code=None):
        self._set_region_and_get_ids(region_code)
        for category in self.categories:
            print('id: {}\t: {}'.format(
                category, self.categories[category]))

    def clear_params(self):
        '''
        Reset the url parameters to the default state. This is useful
        for clearing mistakes.
        '''
        self.params = ''
        self.region_code = 'us'

    def _get_statistics(self):
        temp = self.spec
        for index in range(len(self.json)):
            
            self.spec = 'videos?part=statistics'

            id_ = self.json[index]['id']['videoId']
            channel_id = self.json[index]['snippet']['channelId']
            
            self.params = '&id={}'.format(id_)
            statistics = self.get_request()
            view_count = statistics['items'][0]['statistics']['viewCount']
            estimation = self._estimate_revenue(view_count)

            self.spec = 'channels?part=statistics'
            self.params = '&id={}'.format(channel_id)
            channel_statistics = self.get_request()

            self.data[index] = {
                    'snippet': self.json[index],
                    'video_statistics': statistics,
                    'estimated_earnings': estimation,
                    'channel_statistics': channel_statistics}
        self.spec = temp

    def _estimate_revenue(self, view_count):

        low = Decimal('0.2') * Decimal(view_count)
        high = Decimal('5') * Decimal(view_count)
        mean = (low + high) / Decimal('2')
        return {'low': low, 'high': high, 'mean': mean}

    def _set_region_and_get_ids(self, region_code=None):
        # convert region_code to the region code
        region_code = self._get_region_code(region_code or self.region_code)
        # do we know the categories; are we searching for a different region?
        if region_code != self.region_code or not self.categories:
            self._set_category_ids(region_code)

    def _bad_category(self, id_, region_code=None):
        print('Error: id {} does not exist for regional code {}'.format(
                id_, region_code))
        print('Existing ids for regional code {} are:'.format(region_code))
        self.show_category_names()
        print('Please use an id that exists')

    def _set_category_ids(self, region_code, retry=True):
        self.categories = dict()
        temp = self.spec
        self.spec = 'videoCategories?part=snippet&regionCode={}'.format(
                region_code)
        data = self.get_request(num_results=50)
        self.spec = temp
        try:
            assert data['items']
            for category in data['items']:
                id_ = category['id']
                snippet = category['snippet']['title']
                self.categories[id_] = snippet
        except AssertionError:
            if retry:
                print('Categories do not exist for {}'.format(region_code))
                self._set_category_ids('us', retry=False)

    def _get_region_code(self, country):
        base_url  = 'https://maps.googleapis.com/maps/api/geocode/json?'
        api_call  = base_url + 'address={}'.format(country) + self.key
        try:
            gmap_data = json.loads(requests.get(api_call).text)
        except Exception as e:
            print(str(e))
        else:
            iso_3166  = gmap_data[
                    'results'][0]['address_components'][0]['short_name']
            return iso_3166

def test():
    api = SearchAPI(API_KEY)
    methods = {
            api._get_region_code: ('china', 'CN'),
            api._set_category_ids: ('US', api.categories),
            }
    for method in methods:
        arg = methods[method][0]
        expected_result = methods[method][1]
        result = method(arg) or expected_result
        print('testing [{}]'.format(method.__name__), end='\t')
        print(' passed') if result == expected_result else print(' <<FAILED>>')
    
    # set_date

    dates = {'date1': ((10, 11, 2010), (11, 20, 2011)),
             'date2': ((7, 6, 2015), (8, 6, 2015)),
             'date3': ((7, 6, 2015), (None, None, None)),
             'date4': ((4, 14, 2016), (10, None, None)),
             'date5': ((1, 12, 2008), (None, 19, None))
             }
    for date in dates:
        start, end = dates[date][0], dates[date][1]
        start_month, start_day, start_year = start[0], start[1], start[2]
        end_month, end_day, end_year = end[0], end[1], end[2]
        api.set_date(start_month, start_day, start_year,
            end_month, end_day, end_year)
        print('{}\t'.format(date) + api.params)
        api.params = ''

if __name__ == '__main__':
    
    try:
        if sys.argv[1] == 'test':
            test()
    except IndexError:
        # this is for testing purposes
        r = SearchAPI(API_KEY)
        r.set_keyword('tacos')
        r.set_date(12, 30, 2010)
        r.set_country('france')
        r.get_data(2)
        r.show_data()
