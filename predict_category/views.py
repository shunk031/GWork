from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from predict_category.models import InputURLForm

import pickle
import os
import sys

sys.path.append(os.pardir)
from GCrawler.g_crawler.scraper import GScraper
from GClassifier.g_preprocess import PreprocessDataset
from GClassifier.g_classifier import NaiveBayes

SERIALIZE_MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath("__file__")), "GClassifier")

# Create your views here.


def index(request):

    url_form = InputURLForm()
    context = {
        "url_form": url_form
    }
    return render(request, 'predict_category/index.html', context)


def result(request):
    article_url = request.POST['article_url']

    title, article = scrap_article(article_url)
    predict_category = predict_article_category(article)

    context = {
        "article_url": article_url,
        "predict_category": predict_category,
        "title": title,
        "article": article,
    }

    return render(request, 'predict_category/result.html', context)


def scrap_article(article_url):

    scraper = GScraper(article_url, None, None)
    article_dict = scraper.get_article_detail_info_dict(article_url)

    return article_dict['title'], article_dict['article']


def predict_article_category(article):

    preprocess_dataset = PreprocessDataset("mecab-noun")
    wakati_list = preprocess_dataset.wakati(article)

    with open(os.path.join(SERIALIZE_MODEL_DIR, "naive_bayes_model.pkl"), "rb") as rf:
        naive_bayes = pickle.load(rf)

    return naive_bayes.classify(wakati_list)
