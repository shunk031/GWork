# -*- coding: utf-8 -*-

import time
import json
import traceback

from GCrawler.g_crawler.g_base import GBase
from GCrawler.g_crawler.scraper import GScraper
from urllib.parse import urljoin

CATEGORIES = {
    "entertainment": "1",
    "sports": "2",
    "interesting": "3",
    "domestic": "4",
    "overseas": "5",
    "column": "6",
    "science": "7",
    "gourmet": "8"
}


class GCrawler(GBase):

    BASE_URL = "https://gunosy.com/categories/"
    FINISH_CRAWL = "Finish crawling."

    def __init__(self, target_url, target_category, save_dir, page_count=1):
        self.target_url = target_url
        self.target_category = target_category
        self.before_url = None
        self.save_dir = save_dir
        self.page_count = page_count
        self.category_url = urljoin(self.BASE_URL, CATEGORIES[target_category])

    def get_next_page_link(self, url):
        """
        get next article list page link
        :param str url:
        :rtype: str: next page url if exist else None
        """
        self.before_url = url
        soup = self._make_soup(self.target_url)
        a_next = soup.find("a", {"class": "btn-pager-plus"})

        if a_next is not None and "href" in a_next.attrs:
            next_page_url = self.category_url + a_next['href']

            if self.before_url != next_page_url:
                print("[ PROCESS ] Next article list page: {}".format(next_page_url))
                return next_page_url

        return None

    def crawl(self):
        """
        crawl target url page
        :rtype: str: finish message
        """
        try:
            while True:
                # start to measure the time
                start = time.time()
                print("[ PROCESS ] Now page {} PROCESSING".format(self.page_count))
                scraper = GScraper(self.target_url, self.target_category, self.save_dir)
                scraper.scrap()  # scraping!

                # get next page link url
                self.target_url = self.get_next_page_link(self.target_url)

                # if target_url is not found
                if self.target_url is None:
                    break

                self.page_count += 1
                time.sleep(2)
                end = time.time()  # end to measure the time

                # print processing time
                self._print_processing_time(start, end)

            # finish message
            finish_crawl = self.FINISH_CRAWL

        except (Exception, KeyboardInterrupt) as err:
            print("[ EXCEPTION ] Exception occured in crawl(): {}".format(err))
            traceback.print_tb(err.__traceback__)

            # save crawler status
            self.save_crawler_status()

            if len(str(err)) == 0:
                err = "Keyboard Interrupt"

            # finish message
            finish_crawl = "{} ({})".format(err, self.FINISH_CRAWL)

        return finish_crawl

    def _print_processing_time(self, start_time, end_time):
        """
        print processing time
        :param float start_time:
        :param float end_time:
        """

        elapsed_sec = end_time - start_time
        elapsed_min = elapsed_sec / 60

        if elapsed_min < 1:
            print("[ TIME ] Elapsed time: {:.2f} [sec]".format(elapsed_sec))
        else:
            print("[ TIME ] Elapsed time: {:.2f} [min]".format(elapsed_min))

    def save_crawler_status(self):
        """
        save crawler status when exception occured
        """

        status_dict = {}
        status_dict["target_url"] = self.target_url
        status_dict["page_count"] = self.page_count

        status_filename = "GCrawler-status-{}.json".format(self.target_category)
        with open(status_filename, "w") as wf:
            json.dump(status_dict, wf, indent=2)

        print("[ SAVE ] Save status.json")
