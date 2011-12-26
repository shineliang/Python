#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class MovieNameParser:
    name = ''
    year = ''
    years = []
    for i in range(1980, 2013):
        years.append(str(i))
    regSpliter = re.compile(r'\s|\.')
    regFilterName = re.compile(r'^[0-9]{8}-')
    
    def __init__(self, fullName):
        self.fullName = fullName.strip()
        
    def parse(self):
        self.getNameAndYear()
        
    def getNameAndYear(self):
        array = MovieNameParser.regSpliter.split(self.fullName)
        movieName = ""
        for item in array:
            if item in MovieNameParser.years:
                self.year = item
                self.name = self.parseName(movieName.strip())
            movieName += item + ' '

    def parseName(self, name):
        if MovieNameParser.regFilterName.match(name):
            return name[9:]
        else:
            return name
        

