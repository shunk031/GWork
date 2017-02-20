# -*- coding: utf-8 -*-

import time

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


class GBase:

    def _make_soup(self, url):
        """
        Return BeautifulSoup instance from URL
        :param str url:
        :rtype: bs4.BeautifulSoup
        """
        html = self._safe_url_open(url)
        return BeautifulSoup(html, "lxml")

    def _safe_url_open(self, url, max_retries=3):
        """
        open max_retries times url and get the html
        :param str url:
        :param int max_retries=3:
        :rtype: bytes
        """

        retries = 0

        while True:
            try:
                with urlopen(url) as res:
                    html = res.read()

            except HTTPError as err:
                print("[ EXCEPTION ] in {}#make_soup: {}".format(self.__class__.__name__, err))

                retries += 1
                if retries >= max_retries:
                    print("[ EXCEPTION ] Too many retries.")
                    raise err

                wait = 2 ** retries
                print("[ RETRY ] Waiting {} seconds...".format(wait))
                time.sleep(wait)
            else:
                break

        return html
