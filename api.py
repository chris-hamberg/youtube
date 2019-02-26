from specifications import Search, Channels, Videos
from specifications import VideoCategories, GuideCategories
from decimal import Decimal
from pprint import pprint
from api_key import api_key as key
import sys

class API:

    def __init__(self):
        self.url = 'https://www.googleapis.com/youtube/v3/'
        self.key = '&key={}'.format(key)
        self.category_names = dict()
        
        # youtube api specifications
        self.search           = Search(self, self.url)
        self.video_categories = VideoCategories(self, self.url)
        self.guide_categories = GuideCategories(self, self.url)
        self.channels         = Channels(self, self.url)
        self.videos           = Videos(self, self.url)

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

if __name__ == '__main__':

    # this is for testing purposes
    api = API()
    #pprint(api.search(videoCategoryId=1, regionCode='japan'))
    api.video_categories.show_names('japan')
