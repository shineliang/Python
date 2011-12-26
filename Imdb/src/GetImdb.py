#!/usr/bin/python
# -*- coding: utf-8 -*-

from ImdbInfo import ImdbInfo
from MovieNameParser import MovieNameParser

def processLine(line):
    movie = MovieNameParser(line) 
    movie.parse()
    imdb = ImdbInfo(movie.name, movie.year)
    imdb.getInfo()
    print '%s|%s|%s' % (line.strip(), imdb.rate, imdb.vote)

if __name__ == '__main__':
    fh = open('2.txt')
    for line in fh.readlines():
        try:
            processLine(line)
        except Exception, data:
            None
            #print Exception, ":", data
        
