#!/usr/bin/env python3

import urllib.request
import io

def get_robots_txt(url):
  if url.endswith('/'):
    path = url
  else:
    path = url + '/'
  req = urllib.request.urlopen(path + "robots.txt", data=None)
  data = io.TextIOWrapper(req, encoding='utf-8')
  return data.read()


url = "https://coinmarketcap.com/"
print(get_robots_txt(url))
