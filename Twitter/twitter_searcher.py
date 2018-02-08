#!/usr/bin/env python

import twitter

class Twitter_Searcher:

  def __init__(self):
    self.get_credentials()

  def get_credentials(self):
    """
    Gets authorization credentials from 'credentials.txt'
    Should be run upon construction in order to use credentials
     when authorizing use of twitter api.
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

  def get_tweet(self, search_term='bitcoin', count=1):
    """
    Conducts key-word search of twitter for 'search_term'
    Number of returned tweets must be <= 100. Searchs for 1 by default.
    If exceeding max number of queries (15 queries per 15 minute period) or if
      tweet fails to load, use default tweet as placeholder.
    """
    try:
      t = twitter.Twitter(auth = twitter.OAuth(
        self.access_key, 
        self.access_secret, 
        self.consumer_key, 
        self.consumer_secret))

      query = t.search.tweets(q="bitcoin", count=count)	# conduct twitter seach
      hit = query['statuses'][0]				# Take top result
      return (hit['id'], hit['user']['screen_name'])		# Return (tweet_id, user_name)

    except IndexError:
      return (941913288186642432, "FoxBusiness")

    except:
      print('[-] Unknown error when accessing tweet')
      return (941913288186642432, "FoxBusiness")







if __name__=='__main__':
  ts = Twitter_Searcher()
  ts.handle_getter()
  ts.id_getter()

