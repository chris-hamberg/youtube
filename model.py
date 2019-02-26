from api import *

class model:

    def __init__(self):
        self.api = API()

    def top_viewed_location_by_channel():
        # 1) for each regional code, search channels api, by view count
        # 2) store top result for each regional code in database
        # 3) sort data collection (in descending order) by view count
        # 4) get country name, and view count for each item in the list
        # 5) return list to the controller
        pass

    def top_viewed_channel_in_usa_of_month():
        # requires a definition for month..
        # ..is month 30 days from today, 31 days from today, or independent of
        # the current date, and based on calendar months??
        # api.search(publishedBefore=month_end, publishedAfter=month_start)
        # api.search defaults the regional code to USA, when one is not supplied
        # get the top channel names, and view counts

    def channel_view_summary():
        # get channel name from listbox in ui
        # call database for statistical data
        # daily, monthly, and yearly average view count
        # call api for current view count
        # substract current view count from yesterdays view count = todays views
        # return todays view, & average for daily, monthly, and yearly views

