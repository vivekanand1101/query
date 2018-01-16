# coding=utf-8
import csv
import os

import flask
from flask import Flask, jsonify, request
app = Flask(__name__)

FILE = os.environ.get("FILE", "data.csv")


with open(FILE) as f:
    reader = csv.reader(f)
    terms = [row[0] for row in reader if row[0]]

def fsort():
    sterms = sorted(terms, key=lambda x: (x.lower(), len(x)))
    return sterms

STERMS = fsort()
STERMS_LEN = len(STERMS)
SEARCH_LEN = 10

def binsearch(target):
    ''' Searching through the sorted list for the query
    and range it down to SEARCH_LEN elements '''
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


def distance(given_str, target_str):
    ''' Implement levenshtein distance, returns distance between the given
    string and target string '''

    if given_str == target_str:
        return 0
    elif len(given_str) == 0:
        return len(target_str)
    elif len(target_str) == 0:
        return len(given_str)
    elif given_str.lower().startswith(target_str.lower()):
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
    query = request.args.get("q", '')
    results = []  # must be list of dicts: [{"name": "foo"}, {"name": "bar"}]

    # your logic goes here!
    if len(query) < 3:
        results = []
    else:
        results = binsearch(query)
        results = sorted(results, key=lambda x: (distance(x, query), len(x)))
        results = [{'name': x} for x in results]

    resp = jsonify(results=results[:SEARCH_LEN])  # top 10 results
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/')
def index():
    ''' The index page of the flask app '''
    return flask.render_template('index.html')
