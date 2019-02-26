from abstract import AbstractSpecification, AbstractCategories

class Search(AbstractSpecification):

    def __init__(self, api, url):
        super().__init__(api, url, 'search?')

    def __call__(self, part='snippet', relatedToVideoId='', channelId='', 
            location='', maxResults='5', order='viewCount', publishedAfter='', 
            publishedBefore='', q='', regionCode='', type_='video', 
            videoCategoryId=''):

        # TODO parameter documentation

        return super().__call__()
        
    def set_date(self):
        if self.parameters['publishedBefore'] or self.parameters['publishedAfter']:
            if self.month_end == None: self.month_end = self.month_start
            if self.day_end == None: self.day_end = self.day_start
            if self.year_end == None: self.year_end = self.year_start
            date   = '{}-{}-{}'
            before = date.format(
                    self.year_end, self.month_end, self.day_end
                    )+'T23%3A59%3A59Z'
            after  = date.format(
                    self.year_start, self.month_start, self.day_start
                    )+'T00%3A00%3A00Z'
            self.q_string += '&publishedBefore={}&publishedAfter={}'.format(
                before, after)

class VideoCategories(AbstractCategories):
    '''
    Returns a list of categories that can be associated with YouTube videos
    '''
    # TODO parameter documentation

    def __init__(self, api, url):
        super().__init__(api, url, 'videoCategories?')

class GuideCategories(AbstractCategories):
    '''
    Returns a list of categories that can be associated with YouTube channels
    '''
    # TODO parameter documentation

    def __init__(self, api, url):
        super().__init__(api, url, 'guideCategories?')

class Channels(AbstractSpecification):

    def __init__(self, api, url):
        super().__init__(api, url, 'channels?')

    def __call__(self, part='snippet', categoryId='', maxResults=5, id_=''):
        # TODO process *args
        '''
        - *id_ is a "comma seperated list" of channel ids

        - The id parameter specifies a comma-separated list of the YouTube 
        channel ID(s) for the resource(s) that are being retrieved. In a 
        channel resource, the id property specifies the channel's YouTube 
        channel ID.

        - maxResults is limited to 50 results.

        - Valid part entries (and quota costs):

            auditDetails: 4
            brandingSettings: 2
            contentDetails: 2
            contentOwnerDetails: 2
            id: 0
            invideoPromotion: 2
            localizations: 2
            snippet: 2
            statistics: 2
            status: 2
            topicDetails: 2
        '''
        return super().__call__()

class Videos(AbstractSpecification):

    def __init__(self, api, url):
        super().__init__(api, url, 'videos?')

    def __call__(self, part='snippet,statistics', chart='mostPopular', id_='',
            maxResults=5, regionCode='us', videoCategoryId='0'):
        return super().__call__()
