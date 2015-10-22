#!/usr/bin/env python
import urllib
import json


class ModelKeywordDict(object):
    def __init__(self, file_name):
        # TODO: Read model string from input text file, where the dict should like:
        self.model_dict = {'CAR_NAME': '9999'}

    def __getitem__(self, key):
        if self.model_dict.has_key(key):
            return self.model_dict[key]
        else:
            return None

    def get_models(self, title):
        return_list = []
        for i in self.model_dict.keys():
            if i in title:
                return_list.append(self.model_dict[i])
        return return_list

    def detect_car(self, article):
        # TODO: detect car in article by rules
        keywords = self.get_models(article.title)
        if len(keywords) > 0 and article.serial_id != '':
            article.has_car = True


class Article(object):
    # demo article class, with only serial_id and title properties.
    def __init__(self, title, serial_id):
        self.title = title
        self.serial_id = serial_id
        self.has_car = False


class ModelInfoDict(object):
    def __init__(self, url):
        # TODO: load model info dict from web api.
        json_str = urllib.urlopen(url).read()
        self.model_dict = json.loads(json_str)

    def new_tags(self, old_tags_str):
        # TODO: return new tags with given old_tags in format: 100001:1,200002:2,...
        old_tags = old_tags_str.split(',')
        new_tags = [('900009', 9), ] # new tags list in this style. 
        for tag_id, tag_pw in old_tags:
            tag_pw = int(tag_pw)
            if tag_pw[:2] == '30':  # model tags start with '30'.
                # TODO: add your rules here.
                pass
        return ','.join([ x+':'+str(y) for x, y in new_tags ])


if __name__ == '__main__':
    kw_dict = ModelKeywordDict('keywords.txt')
    info_dict = ModelInfoDict('http://someurl.com/model/info')
    
    a1 = Article('Not a car name', '1111,2222')
    a2 = Article('A4L', '2888')
    kw_dict.detect_car(a1)
    kw_dict.detect_car(a2)
    print a1.has_car
    print a2.has_car
