import nltk as n
from bs4 import BeautifulSoup as b
import urllib3 as url
import random
import pronouncing as p
from metaphone import doublemetaphone as d
from nltk.corpus import wordnet as wn
import eel
import json
import threading
import time



# biopic,
# term = "silent"
# link = "www.google.com/search?q=best+" + term + "+movies"
# http_pool = url.connection_from_url(link)
# r = http_pool.urlopen('GET', link)
# http_pool.close()
# html = r.data.decode('latin-1')
# soup = b(html, 'html.parser')
# movies = []
# for a in soup.find_all("a"):
#     # if a.has_attr('class'): print(a['class'])
#     #     print(a['href'])
#     if a.has_attr('class') and a['class'] == ['Mlb36b']:
#         if "q=" in a['href']:
#             text = a['href']
#             text = text.split("q=")[1]
#             text = text.split("stick=")[0]
#             text = text.replace("+"," ")
#             text = text.replace("&"," ")
#             text = text.replace("%"," ")
#             text = text.replace("(film)"," ")
#             text = text.replace("(film)"," ")
#             if len(text.split(" ")) > 3:
#                 lent = len(text.split(" "))
#                 c = 0
#                 for i in text.split(" "):
#                     # print(i)
#                     if i == "":
#                         c += 1
#                 if c < 2:
#                     print(text)


test = "captain america: civil war"
test2 = "Captain America: Civil War"

print(n.pos_tag(n.word_tokenize(test)))
print(n.pos_tag(n.word_tokenize(test2)))












