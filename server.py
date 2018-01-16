# coding=utf-8
import csv
import math
import os

import flask
from flask import Flask, jsonify, request
app = Flask(__name__)

FILE = os.environ.get("FILE", "data.csv")
SEARCH_LEN = 10


def preprocess():
    ''' Preload the data from csv '''
    with open(FILE) as f:
        reader = csv.reader(f)
        terms = [row[0] for row in reader if row[0]]
    # Sort the terms (case-insensitive) based on dictionary order
    sterms = sorted(terms, key=lambda x: (x.lower(), len(x)))
    return sterms

STERMS = preprocess()
STERMS_LEN = len(STERMS)

def binsearch(target):
    ''' Implement binary search and range search down to SEARCH_LEN elements '''
    start = 0
    end = STERMS_LEN -1
    target = target.lower()
    while end - start > SEARCH_LEN:
        middle = (end + start) / 2
        midpoint = STERMS[middle].decode('utf-8').strip()
        midpoint = midpoint.lower()
        if midpoint.lower().startswith(target.lower()):
            return STERMS[middle:middle+SEARCH_LEN]
        elif midpoint < target:
            start = middle + 1
        elif midpoint > target:
            end = middle
    return STERMS[start:end]


def edit_distance(given_str, target_str):
    ''' Gives edit distance between two strings, in case the given string start
    with target string, returns negative infinity so that it gets at top when
    sorted based on distance
    :args given_str: a term from csv on which we are checking for distance
    :args target_str: the query term from request
    '''

    if given_str == target_str:
        return 0
    elif len(given_str) == 0:
        return len(target_str)
    elif len(target_str) == 0:
        return len(given_str)
    # If the given_str starts with target element, we want to put them first
    elif given_str.decode('utf-8').lower().startswith(target_str.lower()):
        return -float('Inf')
    v0 = [None] * (len(target_str) + 1)
    v1 = [None] * (len(target_str) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(given_str)):
        v1[0] = i + 1
        for j in range(len(target_str)):
            cost = 0 if given_str[i] == target_str[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j] 
    return v1[len(target_str)]


@app.route('/auto')
def hello_world():
    ''' Searches the data from csv for the query element and returns a dict '''
    query = request.args.get("q", '')
    results = []  # must be list of dicts: [{"name": "foo"}, {"name": "bar"}]

    # your logic goes here!
    if len(query) < 3:
        results = []
    else:
        # First narrow down the search to SEARCH_LEN relevant elements
        results = binsearch(query)
        # Get the distances between the target element and relevant elements
        distances = {}
        for result in results:
            distances[result] = edit_distance(result, query)
        results = sorted(results, key=lambda x: (distances[x], len(x)))
        results = [{'name': x, 'score': distances[x] \
            if not math.isinf(distances[x]) else "matching"} for x in results]

    resp = jsonify(results=results[:SEARCH_LEN])  # top 10 results
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/')
def index():
    ''' The index page of the flask app '''
    return flask.render_template('index.html')
