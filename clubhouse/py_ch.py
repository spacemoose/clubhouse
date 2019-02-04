# Goal 1 is to import open import from github, without importing
# duplicates, and subject to certain filters.
#
# I have no idea what I'm doing, so I'm going step by step trying
# stuff out.  Some of that might be useful to someone, so I'm storing
# it here.
#
# I started with this https://github.com/mahmoudimus/clubhouse, which
# seemed to be a nice start, but seems abandoned now.  This is my
# attempt to build something usable starting with that.
#
# At the moment I'm just writing some super simple stuff working
# directly with dictionaries.

import requests
import importlib
import parser
from lxml import html
from io import StringIO
import os
import sys
import json
import curlify

from pprint import pprint

#from clubhouse_resources import Story

class py_ch:

    api_url = "https://api.clubhouse.io/api/v2"
    token = os.environ['CLUBHOUSE_TOKEN']

    def __init__(self):
        self.unarchived_stories = self.search_stories("!is:archived")
        self.user_ids = self.get_username_map()

    def get_username_map(self):
        "Get the map of login names to UUID.  """
        r = requests.get(self.api_url + "/members?token=" + self.token)
        members = dict()
        for m in r.json():
            members[m["profile"]["name"]] = m["id"]
        return members


    def search(self, params):
        """ Return the response json if it was succsful, print diagnostics and return None if it failed"""
        ss_url = self.api_url+"/search/stories"
        r = requests.get(ss_url,  params = params)
        r.encoding='utf-8'
        if (r.status_code != 200):
            print ("\n", r.status_code , " was returned when trying to execute the query: ")
            print (r.url)
            return None
        return r.json()


    def search_stories(self, query):
        """Return a list of clubhouse stories that satisfies the passed query.
                    Any string passed as a search term in the web interface should produce
                    identicl results here.  The returned stories are simple dictionaries
                    consisting with field names as keys."""
        print ("gathering clubhouse stories", end='', flush=True)
        params = {'query':query, 'token':self.token}
        data = self.search(params)
        if data is None:
            print("\nNo data returned.  Something went wrong with the request.")
            return None;
        if 'next' in data:
            nxt = data['next']
        retval = data['data']
        while nxt is not None:
            nxt = nxt[nxt.rfind("=")+1:]
            params = {'query':query, 'next':nxt,'token':self.token }
            data = self.search(params)
            nxt = data['next']
            retval += data
            print(".", end='', flush=True)


        print(f"\ncollected {len(retval)} stories")
        return retval



def main():
    pc = py_ch()
    pprint (pc.user_ids)

#    stories=search_stories("has:comment")
#   for s in stories:
#        pprint (s)

if __name__ == '__main__':
                main()
