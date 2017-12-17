#!/usr/bin/env python

import twitter

class Twitter_Searcher:

  def __init__(self):
    self.get_credentials()

  def get_credentials(self):
    """
    Gets authorization credentials from 'credentials.txt'
    """
    cred_file = 'Twitter/credentials.txt'
    try:
      f = open(cred_file, 'r')
    except IOError:
      print("[-] File '%s' not found\n[-] Run 'authorize.py' to generate credentials" % cred_file)
      exit()
    except:
      print("[-] Unknown error while reading credentials from '%s'" % cred_file)
      exit()

    try:
      self.app_name = f.readline().split(':')[1].strip()
      self.consumer_key = f.readline().split(':')[1].strip()
      self.consumer_secret = f.readline().split(':')[1].strip()
      self.access_key = f.readline().split(':')[1].strip()
      self.access_secret = f.readline().split(':')[1].strip()
    except:
      print("[-] Issue while reading credentials\n[-] Run 'authorize.py to generate credentials")
      exit()

  def search_twitter(self, search_term='bitcoin', count=1):
    """
    Conducts key-word search of twitter for 'search_term'
    Number of returned tweets <= 100
    """
    t = twitter.Twitter(auth = twitter.OAuth(
      self.access_key, 
      self.access_secret, 
      self.consumer_key, 
      self.consumer_secret))
    query = t.search.tweets(q="bitcoin", count=count)

    for result in query['statuses']:
      print("(%s) @%s %s" % (result['created_at'], result['user']['screen_name'], result['text']))
      print('\n')

  def handle_getter(self, search_term='bitcoin', count=1):
    t = twitter.Twitter(auth = twitter.OAuth(
      self.access_key, 
      self.access_secret, 
      self.consumer_key, 
      self.consumer_secret))

    while True:
      query = t.search.tweets(q="bitcoin", count=count)

      try:
        #while (query['statuses'][0] == None) :
        query = t.search.tweets(q="bitcoin", count=count)

        output_query = query['statuses'][0]

        return output_query['user']['screen_name']

      except IndexError:
        pass


  def id_getter(self, search_term='bitcoin', count=1):
    t = twitter.Twitter(auth = twitter.OAuth(
      self.access_key, 
      self.access_secret, 
      self.consumer_key, 
      self.consumer_secret))
    while True:
      query = t.search.tweets(q="bitcoin", count=count)

      try:
        #while (query['statuses'][0] == None) :
        query = t.search.tweets(q="bitcoin", count=count)

        output_query = query['statuses'][0]

        return output_query['id']

      except IndexError:
        pass






if __name__=='__main__':
  ts = Twitter_Searcher()
  ts.handle_getter()
  ts.id_getter()

