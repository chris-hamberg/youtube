import requests, inspect, json

class AbstractSpecification:

    def __init__(self, api, url, specification):
        self.api = api
        self.url = url+specification
        self.q_string = ''

    def __call__(self):
        frame = inspect.currentframe().f_back
        self.parameters = inspect.getargvalues(frame).locals
        del self.parameters['__class__'], self.parameters['self']
        self.parameters = {
                key.replace('_', ''): str(value)
                for key, value in self.parameters.items()}
        self.build_query_string()
        try:
            response = requests.get(self.q_string)
            self.q_string = ''
            return json.loads(response.text)
        except Exception as e:
            print(str(e))

    def build_query_string(self):
        for param in self.parameters:
            if self.parameters[param]:
                if param == 'regionCode':
                    self.parameters[
                            param] = AbstractCategories._get_region_code(
                                    self, self.parameters[param])
                if param == 'publishedBefore' or param == 'publishedAfter':
                    for i in self.parameters[param]:
                        if not i.isnumeric():
                            self.parameters[param
                                    ] = self.parameters[param].replace(i, '/')
                            break
                    month, day, year = self.parameters[param].split('/')
                    if param == 'publishedBefore':
                        self.month_end = month
                        self.day_end = day
                        self.year_end = year
                    else:
                        self.month_start = month
                        self.day_start = day
                        self.year_start = year
                    continue
                self.q_string += '&' + param + '=' + self.parameters[param]
        self.q_string = self.q_string.lstrip('&')
        self.q_string = self.url + self.q_string
        try:
            self.set_date()
        except AttributeError:
            pass
        self.q_string += self.api.key

class AbstractCategories(AbstractSpecification):

    def __init__(self, api, url, specification):
        self.region_code = 'us'
        super().__init__(api, url, specification)

    def __call__(self, part='snippet', regionCode='us', *args):
        if args: # TODO it seems that we don't need *args
            print('got *args in Categories.__call__')
        return super().__call__()
        
    def show_names(self, region_code=None):
        self._set_region_and_get_ids(region_code)
        for category in self.api.category_names:
            print('id: {}\t: {}'.format(
                category, self.api.category_names[category]))

    def _set_category_ids(self, region_code, retry=True):
        self.api.category_names = dict()
        data = self(regionCode=region_code)
        try:
            assert data['items']
            for category in data['items']:
                id_ = category['id']
                snippet = category['snippet']['title']
                self.api.category_names[id_] = snippet
        except AssertionError:
            if retry:
                print('Categories do not exist for {}'.format(region_code))
                self._set_category_ids('us', retry=False)

    def _set_region_and_get_ids(self, region_code=None):
        # convert region_code to the region code
        region_code = self._get_region_code(region_code or self.region_code)
        # do we know the categories; are we searching for a different region?
        if region_code != self.region_code or not self.api.category_names:
            self._set_category_ids(region_code)

    def _get_region_code(self, country):
        base_url  = 'https://maps.googleapis.com/maps/api/geocode/json?'
        api_call  = base_url + 'address={}'.format(
                country) + self.api.key
        try:
            gmap_data = json.loads(requests.get(api_call).text)
        except Exception as e:
            print(str(e))
        else:
            iso_3166  = gmap_data[
                    'results'][0]['address_components'][0]['short_name']
            return iso_3166
