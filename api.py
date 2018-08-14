# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 22:12:21 2018

@author: Christopher Gardner
"""

import random
from flask import Flask
from  flask_restful import Api, Resource, reqparse, abort
from collections import defaultdict
import unittest2
import flaskapi
import string
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('word')
parser.add_argument('wordlist', action='append')

#build useful dicts/lists
alphabet = list(string.ascii_lowercase())

#import CMU dictionary idea for method from:
# https://github.com/aparrish/gen-text-workshop/blob/master/cmu_pronouncing_dictionary_notes.md
rhymedict = defaultdict(list)
worddict = {}
with open('cmudict-0.7b.txt') as f:
    for line in f:
        #skip comments
        if(line[:3]==';;;'):
            continue
        #split elements on the double space
        word, sounds = line[:-1].split('  ')
        sounds = sounds.split(' ')
        if(len(sounds)==1):
            rhyme = sounds[0]
        else:
            rhyme = sounds[-2] + sounds[-1]
        rhymedict[rhyme].append(word)
        worddict[word] = sounds
        

        
#random function
class pick_random(Resource):
    '''Returns a random word from a list of inputs.
    
    Does not check for incorrect user inputs.'''
    
    def post(self):
        args = parser.parse_args()
        wordlist = args['wordlist']
        #we will check for non string inputs. This method likely causes problems with a large user base.
        for word in wordlist:
            if(type(word)!=str):
                abort(404, message="Non-string input is not accepted")
                
        return wordlist[random.randrange(len(wordlist))], 201
    
#rhyming function
class rhymes(Resource):
    '''returns a list of words that rhyme with the input
    
    we'll use a simple definition of rhyming words as words that share the last phonetic sounds'''
    
    def post(self):
        args = parser.parse_args()
        word = args['word']
        rhyme = worddict[word]
        if(len(rhyme)==1):
            rhymelist = rhymedict[rhyme]
        else:
            rhymelist = rhymedict[rhyme[-2]+rhyme[-1]]
        return rhymelist, 201
    
class encode(Resource):
    '''Input a string and get an encoded string back
    
    Uses the simple caesar cipher transformation'''
    def post(self):
        args = parser.parse_args()
        word = args['word']
        code = ''
        for letter in word.lower():
            if(letter not in alphabet):
                code+=letter
            else:
                loc = (alphabet.index(letter) + 3) % len(alphabet)
                code += alphabet[loc]
        return code, 201
    
class decode(Resource):
    '''Input an encrypted string and get a decoded string back
    
    Assumes input is using the simple caesar cipher transformation with shift 3'''
    def post(self):
        args = parser.parse_args()
        code = args['word']
        decode = ''
        for letter in code.lower():
            if(letter not in alphabet):
                decode+=letter
            else:
                loc = (alphabet.index(letter) - 3) % len(alphabet)
                decode += alphabet[loc]
        return decode, 201

#finish building api
api.add_resource(pick_random, '/pickrnd')
api.add_resource(rhymes, '/rhyme')
api.add_resource(encode, '/encode')
api.add_resource(decode, '/decode')


if __name__ == '__main__':
    app.run(debug=True)
