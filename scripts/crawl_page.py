# -*- coding: utf-8 -*-

import argparse
import os
import sys
import time
import json
import random

from urllib.parse import urljoin
from urllib.error import HTTPError
from slacker import Slacker

sys.path.append(os.pardir)
from GCrawler.g_crawler.crawler import GCrawler

BASE_URL = "https://gunosy.com/categories/"

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

HOME_DIR = os.path.expanduser("~")


def safe_post_message(slacker, crawler, start_id, post_message, max_retries=3):

    retries = 0

    while True:
        try:
            slacker.chat.post_message("#crawler", "[{}] [ID: {}] {}".format(crawler.__class__.__name__, start_id, post_message))
        except HTTPError as http_err:
            retries += 1
            if retries >= max_retries:
                raise Exception("Too many retries.")

            wait = 2 ** (retries)
            print("[ RETRY ] Waiting {} seconds...".format(wait))
            time.sleep(wait)
        else:
            break


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='run crawler')
    parser.add_argument('category', choices=CATEGORIES.keys(), help="category to crawl")
    args = parser.parse_args()

    # define target category url
    target_category_url = urljoin(BASE_URL, CATEGORIES[args.category])

    # load status.json if exists
    status_file_dir = os.path.join(os.path.dirname(os.path.realpath("__file__")), "crawler-status")
    status_file = "GCrawler-status-{}.json".format(args.category)
    if os.path.isfile(os.path.join(status_file_dir, status_file)):
        print("[ LOAD ] Load status file.")
        with open(os.path.join(status_file_dir, status_file), "r") as rf:
            status_dict = json.load(rf)

        target_url = status_dict["target_url"]
        page_count = status_dict["page_count"]

    else:
        target_url = target_category_url
        page_count = 1

    save_dir = os.path.join(os.path.dirname(os.path.realpath("__file__")), "data", args.category)
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    crawler = GCrawler(target_url, args.category, save_dir, page_count)
    slacker_config_path = os.path.join(HOME_DIR, ".slacker.config")
    with open(slacker_config_path, "r") as rf:
        slacker_config = json.load(rf)

    slacker = Slacker(slacker_config["token"])

    start_id = random.randint(0, 1000)
    slacker.chat.post_message("#crawler", "[{}] [ID: {}] START {}.".format(crawler.__class__.__name__, start_id, args.category))
    finish_crawl = crawler.crawl()

    safe_post_message(slacker, crawler, start_id, finish_crawl)
