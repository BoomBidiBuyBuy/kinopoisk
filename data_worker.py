# coding=utf-8
from collections import defaultdict
from word_processing import *
import pymorphy2
import requests
import hashlib
import codecs
from bs4 import BeautifulSoup as soup

def download(category, limit):
	url = 'http://www.kinopoisk.ru/reviews/type/comment/status/{0}/period/month/page/{1}/'

	texts = []
	page = 1

	while True:
		request = requests.get(url.format(category, page))
		s = soup(request.text, "html5lib")
		for div in s.find_all('div', {'class': 'userReview'}):
			div_text = div.find('div', {'class': 'brand_words'})

			texts.append((div_text.text,))

		print('Processed page {0}, {1} texts {2}'.format(page, len(texts), category))
		if len(texts) >= limit:
			break

		page += 1

	return texts[:limit]

def update_data():
    morph = pymorphy2.MorphAnalyzer()

    hashes_file = open("hashes", mode="r")
    text_hashes = set()
    added_hashes = set()

    for line in hashes_file:
        text_hashes.add(line[:-1])

    hashes_file.close()

    #---------------------#

    def download_category(category, number):
        texts_file = codecs.open(category + "_texts", mode="a", encoding="utf-8")
        pnt_count = 0
        word_count = 0
        added = 0
        collision = 0

        for text in download(category, number):
            text = text[0].split()
            result_text = ""

            for raw_word in text:
                raw_word, pnt_cnt = word_remove_symbols(raw_word)
                pnt_count += pnt_cnt
                word_count += 1
                result_text += list(norm(raw_word, morph))[0] + " "

            current_hash = hashlib.sha512(result_text.encode(encoding='utf-8')).hexdigest()
            if not current_hash in text_hashes:
                texts_file.write(result_text + '\n')
                text_hashes.add(current_hash)
                added_hashes.add(current_hash)
                added += 1
            else:
                collision += 1

        texts_file.close()

        print category + " added :", added
        print category + " pnt count :", pnt_count
        print category + " word count :", word_count
        print category + " collision :", collision

    download_category("good", 300)
    download_category("bad", 300)
    download_category("neutral", 300)

    hashes_file = open("hashes", mode="a")
    for hash in added_hashes:
        hashes_file.write(hash + '\n')
    hashes_file.close()

def build_vocabulary():
    def get_for_category(category):
        file = codecs.open(category + "_texts", mode="r", encoding="utf-8")

        words = set()

        for line in file:
            for word in line.split():
                words.add(word)

        return words

    words = set()

    words.update(get_for_category("good"))
    words.update(get_for_category("bad"))
    words.update(get_for_category("neutral"))

    return words

def build_texts():
    def read_category(category):
        class Text:
            def __init__(self, text):
                self.text = set(text.split())

        result = []
        file = codecs.open(category + "_texts", mode="r", encoding="utf-8")
        for line in file:
            result.append(Text(line))

        return result

    texts = {}
    texts['good'] = read_category('good')
    texts['bad'] = read_category('bad')
    texts['neutral'] = read_category('neutral')

    return texts

def partiate_texts(texts, count=10):
    test_text = defaultdict(lambda: [])

    for category, texts_cat in texts.items():
        for inx in xrange(count):
            test_text[category].append(texts_cat[inx])

        for inx in xrange(count):
            texts_cat.pop(inx)

    return texts, test_text
