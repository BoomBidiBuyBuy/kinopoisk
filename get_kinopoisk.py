# coding=utf-8
from collections import defaultdict
from data_worker import *
from math import log

update_data()
"""
V = build_vocabulary()
texts, test_texts = partiate_texts(build_texts(), 20)
doc_counts = len(texts['good']) + len(texts['bad']) + len(texts['neutral'])

p_word_class = {}

for word in V:
	for category in ['good', 'bad', 'neutral']:
		numerator = 1.0
		denominator = 2.0
		for cat, value in texts.items():
			for T in value:
				if word in T.text:
					numerator += len(texts[category]) / doc_counts

				denominator += len(texts[category]) / doc_counts

		p_word_class[word, category] = numerator / denominator

p_class = defaultdict(lambda: 0.0)

for category in ['good', 'bad', 'neutral']:
	p_class[category] = len(texts[category]) + 0.1
	p_class[category] /= doc_counts


def classify(T):
	max_val = 0
	max_cat = 'good'
	for category in ['good', 'bad', 'neutral']:
		value = log(p_class[category])

		for word in V:
			if word in T.text:
				value += log(p_word_class[word, category])
			else:
				value += log(1.0 - p_word_class[word, category])

		if value > max_val:
			max_val = value
			max_cat = category

	return max_cat


cat_right = defaultdict(lambda: 0)
cat_wrong = defaultdict(lambda: 0)

for category, texts in test_texts.items():
	for T in texts:
		if classify(T) == category:
			cat_right[category] += 1
		else:
			cat_wrong[category] += 1

for category, value in cat_right.items():
	print "Right " + category + " : " + str(value)

for category, value in cat_right.items():
	print "Wrong " + category + " : " + str(value)
"""
