# -*- coding: utf-8 -*-

import math
import sys
from collections import defaultdict


class NaiveBayes:
    """Multinomial Naive Bayes"""

    def __init__(self):
        """

        """
        self.categories = set()     # Category collection
        self.vocabularies = set()   # Vocabulary collection
        self.word_count = {}        # Number of occurrences of word in category
        self.category_count = {}    # Number of occurrences of category
        self.denominator = {}       # The value of the denominator of P(word|category)

    def train(self, documents, categories):
        """
        Train naive bayes classifier.
        :param list documents:
        :param list categories:
        """
        # Initialize dictionary by extracting categories from document set
        for document, category in zip(documents, categories):
            self.categories.add(category)

        for category in self.categories:
            self.word_count[category] = defaultdict(int)
            self.category_count[category] = 0

        # Count category and word from document set
        for document, category in zip(documents, categories):
            self.category_count[category] += 1
            for word in document:
                self.vocabularies.add(word)
                self.word_count[category][word] += 1

        # The value of the denominator of the conditional probability
        # of a word is preliminarily calculated in advance (for speeding up)
        for category in self.categories:
            self.denominator[category] = sum(self.word_count[category].values()) + len(self.vocabularies)

    def classify(self, document):
        """
        The logarithm log (P (cat | doc)) of the a posteriori probability
        returns the largest category.
        :param list document:
        :rtype: int
        """
        best = None
        max = -sys.maxsize
        for category in self.category_count.keys():
            p = self.calc_score(document, category)
            if p > max:
                max = p
                best = category
        return best

    def classify_all(self, documents):
        """
        Classify all documents given by argument.
        :param list documents:
        :rtype: list
        """
        best_categories = [self.classify(document) for document in documents]
        return best_categories

    def calc_word_probability(self, word, category):
        """
        Calculate the conditional probability P (word | cat) of a word.
        :param str word:
        :param TYPE cat:
        :rtype: TYPE
        """
        # Apply Laplace Smoothing
        return (self.word_count[category][word] + 1) / self.denominator[category]

    def calc_score(self, document, category):
        """
        Calculate the logarithm log (P (cat | doc)) of the posterior probability of the category given the document
        :param list document:
        :param list category:
        :rtype: int
        """
        total = sum(self.category_count.values())  # total number of documents
        score = math.log(float(self.category_count[category]) / total)  # log P(cat)
        for word in document:
            score += math.log(self.calc_word_probability(word, category))  # log P(word|cat)
        return score

    def __str__(self):
        total = sum(self.category_count.values())  # total number of documents
        return "documents: %d, vocabularies: %d, categories: %d" % (total, len(self.vocabularies), len(self.categories))
