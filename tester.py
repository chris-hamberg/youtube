from api import *
import sys, os

class View:

    def __init__(self):
        self.clear = 'cls' if 'win' in sys.platform else 'clear'
        self.controller = Controller()
        self.methods = {1: self.controller.view_count,
                        2: self.controller.channel_views,
                        3: self.controller.subscriber_count,
                        4: self.controller.channel_earnings,
                        5: self.controller.video_earnings,
                        6: self.controller.growth,
                        7: self.controller.video_growth,
                        8: self.controller.earning_growth,
                        0: self.controller.quit}

    def view(self):
        print('''#{0}# api tester 1.0v #{0}#

SELECT AN OPTION TO TEST:
1. view count
2. channel views
3. subscriber count
4. channel earnings
5. video earnings
6. growth
7. video growth
8. earning growth
0. quit
'''.format('-'*3))

    def run(self):
        while True:
            os.system(self.clear)
            self.view()
            selection = input('>>> ')
            os.system(self.clear)
            try:
                selection = int(selection)
                self.methods[selection]()
            except (KeyError, ValueError):
                print('{} is not a valid selection'.format(selection))
                print('Please select a number from the list.')
            finally:
                if selection:
                    print('\nPress Enter to continue.')
                    input('>>> ')
                else:
                    os.system(self.clear)

class Controller:

    def __init__(self):
        self.api = API()

    # views (by video)      **redaction: videos (by view count)
    def view_count(self):
        pprint(self.api.search())
        print('''
[DESCRIPTION]

requirements: views (by video)\t**redaction: videos (by view count)
method name: view_count

This is a listing of the most viewed videos on YouTube

From this list, we can retreive a video id, and get the statistics for that
particular video. Calling the api for statistics on a specific video 
will return the number of views for that video, among other stats. 

It is not possible to search youtube directly, for views, according to the
youtube api specification.''')

    # view (per channel)
    def channel_views(self, requirements='view (per channel)', 
            method_name='channel_views'):
        # formal parameters are temporary, only for current display logic
        json_ = self.api.guide_categories(regionCode='us')
        id_ = json_['items'][5]['id']
        pprint(self.api.channels(part='snippet, statistics', categoryId=id_))
        print('''
[DESCRIPTION]

requirements: {0}
method name: {1}

This is two calls wrapped in one. The first api request is on the 
"guideCategories" specification. In order to get the desired data, calling guide
categories first, is required. 

The call to Guide Categories, requires a regional code as a parameter (the 
regional code is correspondent to the country, and its categories.) Guide 
cateogries then responds with the list of YouTube categories, for the region,
and in that listing are included categorical ids. An id from this list is 
required in order to call the youtube api channels specification. Channels is
what provides channel statistics, including view counts for a particular 
channel.

It is recommended that you inspect the data resulting from the guide_categories 
method, included in the "specifications.py" file. The method is accessible by 
running: 
 
 ~$ python3 -i api.py 
 
and then running the command: api.guide_categories()

This method is currently hard coded to act on the id in the 6th entry returned 
by guideCategories. A random choice on my part; I think the category name for 
the 6th entry might be 'gaming'. The channel method calls the youtube channels 
specification, with the parameters: part='snippet, statistics', and the required 
categoryId (the categoryId value is supplied to us by selecting a valid category
from the list returned by the first api call to guideCategories).

If the region were to remain constant: calls could be amortized, by storing the
resulting list (respondent from guide categories) into memory, or in a database, 
using the regional code as an identifer, for each categorical list.'''.format(
    requirements, method_name))

    # subscribers (requires a target (a channel, or video))
    def subscriber_count(self):
        pprint(self.channel_views('subscribers', 'subscriber_count'))
        print('''
[IMPORTANT]

From the perspective of the API: this query is completely identical to 
"view (per channel)"

The statistics parameter given to the api (in the method handling 
"view (per channel)") returns subscriber count data, already.''')

    # earnings (per channel)
    def channel_earnings(self, requirements='earnings (per channel)',
            method_name='channel_earnings'):
        print('''
[DESCRIPTION]

requirements: {0}
method name: {1}

Not Implemented. This method will inevitably act on our final data product.
Therefore, its implementation should not be constructed until all of its
dependencies are statistifed.'''.format(requirements, method_name))

    # earnings (per video)
    def video_earnings(self):
        self.channel_earnings('earnings (per video)', 'video_earnings')
        print('''
[IMPORTANT]

The internal mechanics of this method should be identical, or near identical to 
the method that is responsible for handling the "earnings (per channel)" 
requirement.''')

    # growth (channel subscribers)
    def growth(self):
        print('''
[DESCRIPTION]

requirements: growth (channel subscribers)
method name: growth

This requires a proprietary, and already populated database. The YouTube api 
does not support subscriber growth for channels.

You can measure change in growth since the beginning of a database, and after
performing a data collection step. It is not possible to get change in 
subscriber count data, before the data record exists. It would be possible to 
measure growth between two like points in a data collection. 

For instance: if you were to take a snap shot of the current number of 
subscribers for a channel, store the data in a database, and then a week later, 
collect the like data for the same channel, you could then measure change in 
growth between the first date and the second date. Solving the problem requires 
metaphorical points in cartesian "data" space. Where each data point would be 
a representation for a specific snap shot (channel name, date, and current 
subscriber count (for that particular date.)) With that data being established, 
it is then possible, by calculating the absolute value for the difference 
between two points from the complete data set (the data set being the complete 
record of all dates on a channel, referent to subscriber count.)

The YouTube api does not supply data for change in terms of growth.''')

    # growth (by video, views)
    # TODO: add videos to the api
    def video_growth(self, requirements='growth (by video, views)', 
            method_name='video_growth'):
        print('''
[DESCRIPTION]

requirements: {0}
method name: {1}

This Python program does not currently support this specification. I will extend 
the specifications module to include the youtube api videos specification.

Forewarning: The api may or may not support the logic required to handle this 
option. I will have to investigate its capabilities.'''.format(requirements,
    method_name))

        # growth (earnings)
    def earning_growth(self):
        self.video_growth('growth (earnings)', 'earning_growth')
        print('''
[IMPORTANT]

The "growth (by video, views)" method must be implemented to support this 
method. "growth (by video, views) acts as a dependency for this method.''')

    def quit(self):
        sys.exit(0)

def test_controller():
    controller = Controller()
    clear = 'cls' if 'win' in sys.platform else 'clear'
    for method in dir(controller):
        os.system(clear)
        if not method.startswith('_') and method != 'quit':
            try:
                name = controller.__getattribute__(method).__name__
                print('\n[TEST]: {}'.format(name))
                input(' - press Enter to execute test.\n')
                controller.__getattribute__(method)()
                input('\nPress Enter to continue.')
            except Exception:
                pass
    else:
        print('\n[Testing Completed.]\n')

def interactive():
    global c
    c = Controller()

if __name__ == '__main__':
    try: 
        command = sys.argv[1]
        test_controller() if command == 'test' else interactive()
        # ~$ python3 -i tester.py interactive will by-pass the view, and
        # instantiate a controller instance; for interactive testing.
    except IndexError:
        # no args were given in the terminal; run as model view controller
        View().run()
