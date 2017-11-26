#!/usr/bin/env python

import twitter

def authorize_twitter():
  """
  Initiates authorizing via twitter apps site.
  Outputs authorization credentials to file 'credentials.txt':
    - app_name
    - consumer_key
    - consumer_secret
    - access_key
    - access-secret
  """
  app_name = "PennCryptoTrader"
  consumer_key = "QCBsCvQCaGnaLcs3l0WbmZpmE"
  consumer_secret = "OaBuumdCkfheLC2PfffpLtXZiRnMWYW3nAZ68p4dijDMao1HLK"

  print("[*] Authorizing application...")
  access_key, access_secret = twitter.oauth_dance(app_name, consumer_key, consumer_secret)
  print("[+]\tAuthorized")
  print("[+]\tApplication name: %s" % app_name)
  print("[+]\tconsumer_key: %s" % consumer_key)
  print("[+]\tconsumer_secret: %s" % consumer_secret)
  print("[+]\taccess_key: %s" % access_key)
  print("[+]\taccess_secret: %s" % access_secret)

  f = open('credentials.txt', 'w')
  f.write('app_name:%s\n' % app_name)
  f.write('consumer_key:%s\n' % consumer_key)
  f.write('consumer_secret:%s\n' % consumer_secret)
  f.write('access_key:%s\n' % access_key)
  f.write('access_secret:%s\n' % access_secret)
  f.close()

if __name__=='__main__':
  authorize_twitter()

