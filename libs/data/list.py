# Dealing with the search list

import pandas as pd
import datetime
import time


class search_list:
    def __init__(self, dir, project_name, search_date) -> None:
        self.list = pd.read_csv(dir + project_name)
        self.search_date = search_date
        self.project_name = project_name

    def filename_latest(self):
        """
        return: filename (ex) project name_20211023), date
        """
        now = datetime.datetime.now()  # current time
        datetime_now = now.strftime("%Y-%m-%d %H:%M:%S")
        date = now.strftime("%Y%m%d")
        filename_latest = self.project_name + "_" + datetime_now
        return filename_latest, datetime_now
