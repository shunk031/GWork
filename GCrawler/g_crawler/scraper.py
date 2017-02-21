# -*- coding: utf-8 -*-

import os
import csv
import traceback
import dateutil.parser

from GCrawler.g_crawler.g_base import GBase


class GScraper(GBase):

    def __init__(self, target_url, target_gategory, save_dir):
        """
        :param str target_url: crawl target url
        :param str target_gategory: target article category
        :param str save_dir: directory where data is saved
        """
        self.target_url = target_url
        self.target_gategory = target_gategory
        self.save_dir = save_dir

    def scrap(self):
        """
        scrap target url page
        """

        # get list of detail article url
        article_detail_url_list = self.get_article_detail_urls()

        article_detail_info = []
        for article_url in article_detail_url_list:
            try:
                article_dict = self.get_article_detail_info_dict(article_url)
                article_detail_info.append(article_dict)

            except AttributeError as err:
                print("[ Exception ] Exception occured in GScraper#scrap: {}".format(err))
                traceback.print_tb(err.__traceback__)

        self.save_article_detail_info_list_to_csv(article_detail_info)

    def get_article_detail_urls(self):
        """
        get url for each articles from article list page
        :rtype: list
        """
        soup = self._make_soup(self.target_url)

        # find article url tag
        div_article_list = soup.find("div", {"class": "article_list"})
        div_list_contents = div_article_list.find_all("div", {"class": "list_content"})

        # get url for each articles and append the url to list
        article_detail_url_list = []
        for div_list_content in div_list_contents:
            a_article_url = div_list_content.find("div", {"class": "list_title"}).find("a")
            article_url = a_article_url["href"]
            print("[ Get ] Get URL: {}".format(article_url))
            article_detail_url_list.append(article_url)

        return article_detail_url_list

    def get_article_detail_info_dict(self, article_url):
        """
        get article infomation(url, title, article content, category, update date)
        :param str article_url: article url
        :rtype: dict
        """
        article_soup = self._make_soup(article_url)

        article_dict = {}
        article_dict["url"] = article_url
        article_dict["title"] = self.get_article_title(article_soup)
        article_dict["article"] = self.get_article_content(article_soup)
        article_dict["category"] = self.target_gategory
        article_dict["update_date"] = self.get_update_date(article_soup)

        return article_dict

    def get_article_title(self, a_soup):
        """
        get the article title
        :param bs4.BeautifulSoup a_soup:
        :rtype: str
        """
        title = a_soup.find("h1", {"class": "article_header_title"}).get_text()
        print("[ GET ] Title: {}".format(title))
        return title

    def get_article_content(self, a_soup):
        """
        get the article content
        :param bs4.BeautifulSoup a_soup:
        :rtype: str
        """
        return a_soup.find("div", {"data-gtm": "article_article"}).get_text()

    def get_update_date(self, a_soup):
        """
        get the article update date
        :param  bs4.BeautifulSoup a_soup:
        :rtype: str
        """
        return a_soup.find("li", {"class": "article_header_lead_date"})["content"]

    def save_article_detail_info_list_to_csv(self, article_detail_dict_list):
        """
        save article information to csv file
        :param list article_detail_dict_list:
        """
        # make save_dir directory if not exists
        try:
            os.makedirs(self.save_dir)
        except FileExistsError:
            pass

        for article_dict in article_detail_dict_list:
            article_title = article_dict['title']
            update_date = self._convert_update_date(article_dict['update_date'])
            # define csv filename from title and update date
            csv_filename = "{}.csv".format(self._convert_filename(update_date + article_title))

            # save article dict to csv
            with open(os.path.join(self.save_dir, csv_filename), "w") as wf:
                writer = csv.DictWriter(wf, article_dict.keys())
                writer.writeheader()
                writer.writerow(article_dict)

    def _convert_filename(self, article_title):
        """
        convert filename (delete obstructive characters)
        :param str article_title:
        :rtype: str
        """
        filename = article_title.replace("/", "")
        filename = filename.replace("?", "")

        if len(filename) > 150:
            print("[ DEBUG ] File name is too long, so shorten.")
            filename = filename[:150]
        return filename

    def _convert_update_date(self, update_date):
        """
        convert datetime
        :param str update_date:
        :rtype: str
        """
        tdatetime = dateutil.parser.parse(update_date)
        return tdatetime.strftime("%Y-%m-%d")
