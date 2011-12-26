#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import json

class InvalidInfoException(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)  

class ImdbInfo:
    urlFormat = 'http://www.imdbapi.com/?r&t=%s&y=%s'
    name = ''
    year = 0
    rate = 0.0
    vote = 0
    
    def __init__(self, name, year):
        self.name = name
        self.year = year

    def getInfo(self):
        if self.name is None or self.name == '':
            raise InvalidInfoException, "Movie's name is empty"
        
        url = self.urlFormat % (self.name, self.year)
        page = urllib.urlopen(url)
        data = page.read()
        dat = json.loads(data)
        if 'Rating' in dat and 'Votes' in dat:
            self.rate = float(dat['Rating'])
            self.vote = int(dat['Votes'])
        else:
            raise InvalidInfoException, self.name

