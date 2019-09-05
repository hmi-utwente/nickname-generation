import nltk as n
from bs4 import BeautifulSoup as b
from bs4 import NavigableString
import urllib3 as url
import urllib
import random
import pronouncing as p
from metaphone import doublemetaphone as d
from nltk.corpus import wordnet as wn
import eel
import json
import threading
import time
import pdb
import re

#%% Functions and global variables

# movie = False
# musical = False
# sporty = False
# boring = False
qs = [False, False, False, False]
global smalltalk
smalltalk = False
smalltalkies = ["Where are you from?", "Where do you currently live?", "Do you have any pets?", "Which sports do you play or follow?"]
asked = [False, False, False]
global firstName
global lastName
global middleName
global message
global rhymingNames
rhymingNames = -1

qtexts = ["Lets start with the basics, what is your name?", "Which sports do you play or follow?", "Alright, do you follow or play any other sports?",
          "I see, and what about movies? Which genres do you like watching?",
          "Hmm could you maybe respell that, or try another one. Maybe make it singular instead of plural",
          "And finally, would you say that you like sports or movies more? You have to choose one!"]



def nounGetter(tags):
    nouns = []

    for j in tags:
        if j[1] == 'NN' or j[1] == "NNS" and j[0] not in nouns:
            nouns.append(j[0])

    return nouns


def verbGetter(tags):
    verbs = []

    for j in tags:
        if j[1] == 'VB' or j[1] == 'VBD' or j[1] == 'VBG' or j[1] == 'VBN' and j[0] not in verbs:
            verbs.append(j[0])

    return verbs


def getConceptTermsWithContext(word):
    searchTerm = word
    link = 'http://conceptnet.io/c/en/'
    link = link + searchTerm
    http_pool = url.connection_from_url(link)
    r = http_pool.urlopen('GET', link)
    http_pool.close()
    html = r.data.decode('utf-8')
    soup = b(html, features="html5lib")

    termsWithContext = []
    withContext = []
    fart = []
    candies = []
    # divs = []

    divs = soup.findAll("a")

    for d in divs:
        if d.contents[0] == 'Terms with this context':
            withContext = d.find_parent().find_parent()

    if len(withContext) > 0:
        links = withContext.findAll("span")
        for k in links:
            if 'en' in k.contents[0]:
                l = k.find_parent().find_all("a")
                for j in l:
                    termsWithContext.append(n.word_tokenize(j.contents[0]))

        if len(termsWithContext) > 1:
            del (termsWithContext[0])

        for k in termsWithContext:
            if len(k) == 1 and not '➜' == k[0] and not k[0] == 'v' and not k[0] == 'n':
                fart.append(k[0])

            elif len(k) > 1 and not k[0] == 'v' and not k[0] == 'n' and not k[0] == 'a' and not 'more' in k[0].lower():
                temp = ""
                for l in k:
                    if not l == ',':
                        temp = temp + " " + l
                fart.append(temp[1:])

        termsWithContext = fart

        for i in range(len(termsWithContext)):

            if " " in termsWithContext[i]:
                termsWithContext[i] = termsWithContext[i].replace(" ", "_")
            elif "-" in termsWithContext[i]:
                termsWithContext[i] = termsWithContext[i].replace("-", "_")
            try:
                termsWithContext[i] = termsWithContext[i].encode()
                termsWithContext[i] = termsWithContext[i].decode('UTF-8')
            except UnicodeDecodeError:
                continue
            link = 'http://conceptnet.io/c/en/' + termsWithContext[i]
            http_pool = url.connection_from_url(link)
            r = http_pool.urlopen('GET', link)
            htm = r.data.decode('UTF-8')
            http_pool.close()
            s = b(htm, features="html5lib")

            fibs = s.findAll("a")

            for j in fibs:
                if j.contents[0] == 'Context of this term':
                    lin = j.find_parent().find_parent()

                    if len(lin) > 0:

                        ls = lin.findAll("a")
                        pre = []
                        for k in range(len(ls)):
                            term = n.word_tokenize(ls[k].contents[0])

                            if len(term) == 1 and not '➜' == term[0] and not term[0] == 'v' and not term[0] == 'n':
                                pre.append(term[0])

                            elif len(term) > 1 and not term[0] == 'v' and not term[0] == 'n' and not term[0] == 'a' and not 'more' in \
                                term[0].lower():
                                # print("Second check:")
                                # print(term)
                                temp = ""
                                for l in term:
                                    if not l == ',':
                                        temp = temp + " " + l
                                pre.append(temp[1:])
                        del(pre[0])
                        pre = list(set(pre))

                        if searchTerm in pre and len(pre) < 3:
                            if "_" in termsWithContext[i]:
                                temp = termsWithContext[i]
                                temp = temp.replace("_", " ")
                                candies.append(temp)
                            else:
                                candies.append(termsWithContext[i])

    candies = list(set(candies))
    c = []
    for i in candies:
        if not searchTerm in i:
            c.append(i)
    candies = c

    return candies


def getConceptDerivedTerms(word):
    searchTerm = word
    link = 'http://conceptnet.io/c/en/'
    link = link + searchTerm
    http_pool = url.connection_from_url(link)
    r = http_pool.urlopen('GET', link)
    http_pool.close()
    html = r.data.decode('utf-8')
    soup = b(html, features="html5lib")

    divs = soup.findAll("a")
    div = []
    candies = []

    for d in divs:
        if d.contents[0] == 'Derived terms':
            div = d.find_parent().find_parent()

        # elif d.contents[0] == 'Terms with this context':
        #     withContext = d.find_parent().find_parent()

    if len(div) > 0:
        links = div.findAll("a")
        for k in links:
            candies.append(n.word_tokenize(k.contents[0]))

        del (candies[0])

        c = []

        for k in candies:
            if len(k) > 1:
                counter = 0
                s = ''
                for j in k:
                    if len(j) > 2:
                        counter += 1
                        s = s + ' ' + j
                if counter == len(k):
                    c.append(s)

            elif len(k[0]) > 2:
                c.append(k[0])

        candies = c
        # for i in candidates: print(i)
        c = []

        for k in candies:
            if not k == searchTerm:
                c.append(k)
        candies = c

        for k in range(len(candies)):
            temp = n.word_tokenize(candies[k])
            if len(temp) > 1:
                s = ''
                for j in temp:
                    s = s + j + ' '
                candies[k] = s
            else:
                candies[k] = temp[0]

    return candies


def getConceptSports(word):
    searchTerm = word
    link = 'http://conceptnet.io/c/en/'
    link = link+searchTerm
    http_pool = url.connection_from_url(link)
    r = http_pool.urlopen('GET', link)
    http_pool.close()
    html = r.data.decode('utf-8')
    soup = b(html, features="html5lib")

    divs = soup.findAll("a")
    termsWithContext = []
    derivedTerms = []
    tWC = []
    dT = []
    contextCandies = []
    derivedCandies = []

    for d in divs:
        if d.contents[0] == 'Derived terms':
            div = d.find_parent().find_parent()

            if len(div) > 0:
                dinks = div.findAll("a")

                for k in dinks:
                    derivedTerms.append(n.word_tokenize(k.contents[0]))

                del (derivedTerms[0])

                for k in derivedTerms:
                    if len(k) == 1 and not '➜' == k[0] and not k[0] == 'v' and not k[0] == 'n':
                        dT.append(k[0])

                    elif len(k) > 1 and not k[0] == 'v' and not k[0] == 'n' and not k[0] == 'a' and not 'more' in k[
                            0].lower():
                        temp = ""
                        for l in k:
                            if not l == ',':
                                temp = temp + " " + l
                        dT.append(temp[1:])

                derivedCandies = dT

                # for i in range(len(derivedTerms)):
                #
                #     if " " in derivedTerms[i]:
                #         derivedTerms[i] = derivedTerms[i].replace(" ", "_")
                #     elif "-" in derivedTerms[i]:
                #         derivedTerms[i] = derivedTerms[i].replace("-", "_")
                #
                #     link = 'http://conceptnet.io/c/en/' + derivedTerms[i]
                #     http_pool = url.connection_from_url(link)
                #     r = http_pool.urlopen('GET', link)
                #     htm = r.data.decode('utf-8')
                #     http_pool.close()
                #     s = b(htm, features="html5lib")
                #
                #     libs = s.findAll("a")
                #
                #     for j in libs:
                #         if j.contents[0] == 'Context of this term':
                #             shin = j.find_parent().find_parent()
                #
                #             if len(shin) > 0:
                #
                #                 ls = shin.findAll("a")
                #                 pre = []
                #                 for k in range(len(ls)):
                #                     term = n.word_tokenize(ls[k].contents[0])
                #
                #                     if len(term) == 1 and not '➜' == term[0] and not term[0] == 'v' and not term[
                #                                                                                                 0] == 'n':
                #                         # print("First check:")
                #                         # print(term)
                #                         pre.append(term[0])
                #
                #                     elif len(term) > 1 and not term[0] == 'v' and not term[0] == 'n' and not term[
                #                                                                                                  0] == 'a' and not 'more' in \
                #                                                                                                                    term[
                #                                                                                                                        0].lower():
                #                         temp = ""
                #                         for l in term:
                #                             if not l == ',':
                #                                 temp = temp + " " + l
                #                         pre.append(temp[1:])
                #                 del (pre[0])
                #                 pre = list(set(pre))
                #
                #                 if searchTerm in pre and len(pre) < 3:
                #                     if "_" in derivedTerms[i]:
                #                         temp = derivedTerms[i]
                #                         temp = temp.replace("_", " ")
                #                         derivedCandies.append(temp)
                #                     else:
                #                         derivedCandies.append(termsWithContext[i])

        elif d.contents[0] == 'Terms with this context':
            withContext = d.find_parent().find_parent()

    # if len(div) > 0:
    #     links = div.findAll("a")
    #     for k in links:
    #         candies.append(n.word_tokenize(k.contents[0]))
    #
    #     del (candies[0])
    #
    #     c = []
    #
    #     for k in candies:
    #         if len(k) > 1:
    #             counter = 0
    #             s = ''
    #             for j in k:
    #                 if len(j) > 2:
    #                     counter += 1
    #                     s = s + ' ' + j
    #             if counter == len(k):
    #                 c.append(s)
    #
    #         elif len(k[0]) > 2:
    #             c.append(k[0])
    #
    #     candies = c
    #     # for i in candidates: print(i)
    #     c = []
    #
    #     for k in candies:
    #         if not k == searchTerm:
    #             c.append(k)
    #     candies = c
    #
    #     for k in range(len(candies)):
    #         temp = n.word_tokenize(candies[k])
    #         if len(temp) > 1:
    #             s = ''
    #             for j in temp:
    #                 s = s + j + ' '
    #             candies[k] = s
    #         else:
    #             candies[k] = temp[0]
    #
    # print("after derived terms")
    # print(cand
            if len(withContext) > 0:
                links = withContext.findAll("a")
                for k in links:
                    termsWithContext.append(n.word_tokenize(k.contents[0]))

                del (termsWithContext[0])

                for k in termsWithContext:
                    if len(k) == 1 and not '➜' == k[0] and not k[0] == 'v' and not k[0] == 'n':
                        tWC.append(k[0])

                    elif len(k) > 1 and not k[0] == 'v' and not k[0] == 'n' and not k[0] == 'a' and not 'more' in k[0].lower():
                        temp = ""
                        for l in k:
                            if not l == ',':
                                temp = temp + " " + l
                        tWC.append(temp[1:])

                termsWithContext = tWC

                for i in range(len(termsWithContext)):

                    if " " in termsWithContext[i]:
                        termsWithContext[i] = termsWithContext[i].replace(" ", "_")
                    elif "-" in termsWithContext[i]:
                        termsWithContext[i] = termsWithContext[i].replace("-", "_")

                    link = 'http://conceptnet.io/c/en/' + termsWithContext[i]
                    http_pool = url.connection_from_url(link)
                    r = http_pool.urlopen('GET', link)
                    htm = r.data.decode('utf-8')
                    http_pool.close()
                    s = b(htm, features="html5lib")

                    fibs = s.findAll("a")

                    for j in fibs:
                        if j.contents[0] == 'Context of this term':
                            lin = j.find_parent().find_parent()

                            if len(lin) > 0:

                                ls = lin.findAll("a")
                                pre = []
                                for k in range(len(ls)):
                                    term = n.word_tokenize(ls[k].contents[0])

                                    if len(term) == 1 and not '➜' == term[0] and not term[0] == 'v' and not term[0] == 'n':
                                        # print("First check:")
                                        # print(term)
                                        pre.append(term[0])

                                    elif len(term) > 1 and not term[0] == 'v' and not term[0] == 'n' and not term[0] == 'a' and not 'more' in \
                                        term[0].lower():
                                        # print("Second check:")
                                        # print(term)
                                        temp = ""
                                        for l in term:
                                            if not l == ',':
                                                temp = temp + " " + l
                                        pre.append(temp[1:])
                                del(pre[0])
                                pre = list(set(pre))

                                if searchTerm in pre and len(pre) < 3:
                                    if "_" in termsWithContext[i]:
                                        temp = termsWithContext[i]
                                        temp = temp.replace("_", " ")
                                        contextCandies.append(temp)
                                    else:
                                        contextCandies.append(termsWithContext[i])

            # print("after context terms")
            # print(candies)
            contextCandies = list(set(contextCandies))
            c = []
            for i in contextCandies:
                if not searchTerm in i:
                    c.append(i)
            contextCandies = c

    if len(contextCandies) > 1:
        return contextCandies
    else:
        return derivedCandies


def getSentiWordNetRating(word):
    f = open("SentiWordNet_3.0.0.txt", "r")
    for x in f:
        if word + '#' in x:
            x = x.split("\t")
            # print(x)
            negRating = float(x[3])
            if negRating < 0.25:
                return True
            else:
                return False


def getSentiWordNetWords(word, candidates):
    f = open("SentiWordNet_3.0.0.txt", "r")
    c = []
    for x in f:
        if ' ' + word + ' ' in x:
            x = x.split("\t")
            x[len(x) - 2] = x[len(x) - 2].split("#")[0]

            if word in x[len(x) - 1]:

                if len(x[len(x) - 2].split(" ")) > 1:

                    for j in x[len(x) - 2].split(" "):

                        if "_" in j:
                            j = j.replace("_", " ")
                        if j not in candidates:
                            c.append(j)
                else:
                    if "_" in x[len(x) - 2]:
                        temp = x[len(x) - 2].replace("_", " ")
                        if temp not in candidates:
                            c.append(temp)
                    elif not x[len(x) - 2] == word and x[len(x) - 2] not in candidates:
                        c.append(x[len(x) - 2])

    return c


def wordInSentiNet(word):
    f = open("SentiWordNet_3.0.0.txt", "r")
    for x in f:
        if ' ' + word + ' ' in x:
            x = x.split("\t")
            # if x[0].lower() == 'n':
            split = x[len(x) - 2].split("#")
            for i in split:
                if word in i:
                    return True
            compare = x[len(x) - 2].split("#")[0]
            if word == compare or word in compare:
                return True
    return False


def getSentiNetPronunciations():
    f = open("SentiWordNet_3.0.0.txt", "r")
    for x in f:

        x = x.split("\t")
            # if x[0].lower() == 'n':
        split = x[len(x) - 2].split("#")


def filter(list):
    c = []
    for k in list:
        if not n.pos_tag(n.word_tokenize(k))[0][1] == 'JJ' \
                and not n.pos_tag(n.word_tokenize(k))[0][1] == 'RB' \
                and not k[0:4] == 'anti' \
                and not k[0:3] == 'non':
            c.append(k)

    return c


def capitalize(word):
    nick = ""

    sp = (word.split(" "))
    if len(sp) > 1:
        for k in range(len(sp)):
            if not sp[k] == '':
                f = sp[k][0]
                rest = sp[k][1:]
                if k == len(sp)-1:
                    nick = nick + (f.upper() + rest)
                elif k < len(sp):
                    nick = nick + (f.upper() + rest) + " "

    else:
        f = word[0]
        rest = word[1:]
        nick = f.upper() + rest

    return nick


def normalize(list):
    tagged = []
    for i in range(len(list)):
        first = list[i][0].lower()
        second = list[i][1]
        tagged.append((first, second))
    return tagged


def getRhymes(word):
    r = []
    for i in range(len(word)):
        if len(word[i:]) > 1:
            t = p.rhymes(word[i:].lower())
            temp = []
            # for j in t:
            #     if wordInSentiNet(j):
            #         temp.append(j)
            if len(temp) > 0:
                r.append(temp)

    u = []
    for k in range(len(r) - 1):
        u = set(u).union(set(r[k]).union(set(r[k + 1])))
    return list(u)


def lastResort(word):
    r = []
    for i in range(len(word)):
        if len(word[i:]) > 1:
            # print(word[i:])
            t = findWordNetRhymes(word[i:].lower())
            temp = []
            for j in t:
                if wordInSentiNet(j) and len(j) > 2:
                    temp.append(j)
            if len(temp) > 0:
                r.append(temp)
    # print(r)
    u = []
    for k in range(len(r) - 1):
        u = set(u).union(set(r[k]).union(set(r[k + 1])))
    return list(u)


def findWordNetRhymes(word):
    w = d(word.lower())[0]

    res = []
    for ss in wn.words():
        if d(ss)[0] == w:
            res.append(ss)

    if len(res) < 1:
        word = word[1:]
        if len(word) > 1:
            print("Going one level further")
            return findWordNetRhymes(word)
    else:
        return res


def getWikiSports():
    links = ['https://en.wikipedia.org/wiki/list_of_sports', "https://www.topendsports.com/events/summer/sports/index.htm",
             "https://en.wikipedia.org/wiki/List_of_hobbies"]
    # link = 'https://en.wikipedia.org/wiki/list_of_sports'
    # link2 = "https://www.topendsports.com/events/summer/sports/index.htm"
    # link3 = "https://en.wikipedia.org/wiki/List_of_hobbies"
    answer = ""

    # http_pool = url.connection_from_url(link2)
    # r = http_pool.urlopen('GET', link2)
    # html1 = r.data.decode('utf-8')
    # http_pool.close()
    #
    #
    # soup = b(html, features="html.parser")
    # soup2 = b(html1, features="html.parser")
    # answer = str(soup).lower()
    # answer = answer + str(soup2).lower()
    # return answer

    for i in links:
        http_pool = url.connection_from_url(i)
        r = http_pool.urlopen('GET', i)
        html = r.data.decode('utf-8')
        http_pool.close()
        soup = b(html, features='html.parser')
        answer = answer + "\n" + str(soup).lower()

    return answer


def getMovieGenres():
    genres = {"action": "https://www.filmsite.org/actionfilms4.html",
              "adventure": "https://www.filmsite.org/adventurefilms4.html",
              "animated": "https://www.filmsite.org/animatedfilms7.html",
              "biopic": "https://www.filmsite.org/biopics2.html",
              "comedy": "https://www.filmsite.org/comedyfilms7.html",
              ("crime", "gangster"): "https://www.filmsite.org/crimefilms4.html",
              "cult": "https://www.filmsite.org/cultfilms4.html",
              "drama": "https://www.filmsite.org/dramafilms3.html",
              "melodrama": "https://www.filmsite.org/melodramafilms4.html",
              ("epic", "historical", "period"): "https://www.filmsite.org/epicsfilms3.html",
              "fantasy": "https://www.filmsite.org/fantasyfilms3.html",
              ("film-noir", "noir", "filmnoir"): "https://www.filmsite.org/filmnoir6.html",
              ("detective", "mystery"): "https://www.filmsite.org/mysteryfilms3.html",
              "horror": "https://www.filmsite.org/horrorfilms5.html",
              "supernatural": "https://www.filmsite.org/supernatfilms2.html",
              ("musicals", "musical", "dance", "dances"): "https://www.filmsite.org/musicalfilms7.html",
              "romance": "https://www.filmsite.org/romancefilms5.html",
              ("scifi", "sci-fi", "science-fiction"): "https://www.filmsite.org/sci-fifilms7.html",
              ("superhero", "superheroes", "heros", "heroes"): ["https://www.filmsite.org/superheroesonfilm12.html",
                                                                "https://www.filmsite.org/superheroesonfilm13.html",
                                                                "https://www.filmsite.org/superheroesonfilm14.html"],
              ("thriller", "suspense"): "https://www.filmsite.org/thrillerfilms4.html",
              "war": "https://www.filmsite.org/warfilms6.html",
              ("western", "westerns"): "https://www.filmsite.org/westernfilms6.html",
              "silent": "https://www.filmsite.org/silentfilms2.html"}
    answer = ""
    keys = genres.keys()
    # print(genres[("crime", "gangster")])
    for i in keys:
        if isinstance(i, tuple):
            for j in i:
                answer = answer + " " + j
        else:
            answer = answer + " " + i
    return answer


def rhyme(word):
    word = word.lower()
    r = p.rhymes(word)
    results = []


    if len(r) < 3:
        print('starting wordnet rhymes')
        t = findWordNetRhymes(word)
        print('finished wordnet rhymes')

        if len(t) > 0:
            for i in range(len(t)):
                if "-" in t[i]:
                    t[i] = t[i].replace("-", " ")
                elif "_" in t[i]:
                    t[i] = t[i].replace("_", " ")

            r = list(set(r + t))

    if len(r) < 3:
        print('starting get rhymes')
        r = list(set(r + getRhymes(word)))
        print('finished get rhymes')

    print(r)
    for i in r:
        if getSentiWordNetRating(i):
            results.append(i)

    global rhymingNames
    rhymingNames = results


def getMovieNicknames(word, firstName):
    word = word.lower()
    # f = open("noc.txt", "r")
    # contents = f.readlines()
    movies = []
    results = []

    if word == "gangster" or word == "gang":
        word = "crime"
    elif word == "historical" or word == "period":
        word = "epic"
    elif word == "film-noir" or word == "filmnoir":
        word = "noir"
    elif word == "detective":
        word = "mystery"
    elif word == "musicals" or word == "dance" or word == "dance":
        word = "musical"
    elif word == "sci-fi" or word == "science-fiction" or word == "science_fiction":
        word = "scifi"
    elif word == "westerns":
        word = "western"
    elif word == "suspense":
        word = "thriller"
    elif word == "superhero" or word == "superheroes" or word == "heroes":
        word = "hero"
    elif word == "romantic":
        word = "romance"
    elif word == "funny":
        word = "comedy"
    elif word == "biopic":
        word = "documentary"

    genres = {"action": "https://www.filmsite.org/actionfilms4.html",
              "adventure": "https://www.filmsite.org/adventurefilms4.html",
              "animated": "https://www.filmsite.org/animatedfilms7.html",
              "documentary": "https://www.filmsite.org/biopics2.html",
              "comedy": "https://www.filmsite.org/comedyfilms7.html",
              "crime": "https://www.filmsite.org/crimefilms4.html",
              "cult": "https://www.filmsite.org/cultfilms4.html",
              "drama": "https://www.filmsite.org/dramafilms3.html",
              "melodrama": "https://www.filmsite.org/melodramafilms4.html",
              "epic": "https://www.filmsite.org/epicsfilms3.html",
              "fantasy": "https://www.filmsite.org/fantasyfilms3.html",
              "noir": "https://www.filmsite.org/filmnoir6.html",
              "mystery": "https://www.filmsite.org/mysteryfilms3.html",
              "horror": "https://www.filmsite.org/horrorfilms5.html",
              "supernatural": "https://www.filmsite.org/supernatfilms2.html",
              "musical": "https://www.filmsite.org/musicalfilms7.html",
              "romance": "https://www.filmsite.org/romancefilms5.html",
              "scifi": "https://www.filmsite.org/sci-fifilms7.html",
              "hero": "https://www.filmsite.org/fantasyfilms3.html",
              "thriller": "https://www.filmsite.org/thrillerfilms4.html",
              "war": "https://www.filmsite.org/warfilms6.html",
              "western": "https://www.filmsite.org/westernfilms6.html",
              "silent": "https://www.filmsite.org/silentfilms2.html"}

    http_pool = url.connection_from_url(genres[word])
    r = http_pool.urlopen('GET', genres[word])
    http_pool.close()
    html = r.data.decode('utf-8')
    soup = b(html, "html.parser")

    td = soup.findAll("td")
    td = td[-1]

    a = td.findAll("a")
    links = []
    for i in a:
        if not "=" in str(i.contents[0]):
            links.append(str(i.contents[0]))


    td = str(td)
    td = td.split("<br/>")

    for i in range(len(td)):
        td[i] = td[i].split("(")[0]
        if "\n" in td[i]:
            td[i] = td[i].split("\n")[1]
        if "<a" in td[i]:
            td[i] = td[i].split(">")[1]
        else:
            counter = 0
            for j in range(len(td[i])):
                if not td[i][j].isalpha():
                    counter += 1
                else:
                    break
            td[i] = td[i][counter:]
        # print(td[i])

    for i in td:
        if "<img align=\"bottom\" border=\"0\" height=\"10\" src=\"redstar.gif\" width=\"14\"/" not in i and \
        len(i) < 70:
            movies.append(i)

    del(movies[0])

    # Look through NOC list
    # people = []
    #
    # for i in contents:
    #     compare = i.split("\t")
    #     if len(compare) == 25:
    #         if word in compare[14]:
    #             people.append(compare[0])
    #
    # results = []
    # if len(people) > 2:
    #     for i in people:
    #         res = i.split(" ")
    #         if len(res) > 1:
    #             s = ""
    #             for j in range(len(res)):
    #                 if not j == 0:
    #                     s = s + res[j] + " "
    #             s = firstName + " " + s
    #             # print(s)
    #             results.append(s[:-1])
    #         else:
    #             results.append(str(i) + " " + firstName)
    #     return results
    # else:
    for i in movies:
        done = False
        if len(i) > 1:
            res = n.pos_tag(n.word_tokenize(i))
            if len(res) > 1:
                s = ""
                for j in res:
                    # print(j)
                    if j[1] == "NNP" and not done:
                        s = s + firstName + " "
                        done = True
                    else:
                        s = s + j[0] + " "
                if firstName in s:
                    results.append(s[:-1])
    return results

def getMovieNicknames2(word, firstName):
    word = word.lower()
    movies = []
    results = []

    if word == "gangster" or word == "gang":
        word = "crime"
    elif word == "historical" or word == "period":
        word = "epic"
    elif word == "film-noir" or word == "filmnoir":
        word = "noir"
    elif word == "detective":
        word = "mystery"
    elif word == "musicals" or word == "dance":
        word = "musical"
    elif word == "sci-fi" or word == "science-fiction":
        word = "scifi"
    elif word == "westerns":
        word = "western"
    elif word == "suspense":
        word = "thriller"
    elif word == "superhero" or word == "superheroes" or word == "heroes":
        word = "hero"
    elif word == "romantic":
        word = "romance"
    elif word == "funny":
        word = "comedy"
    elif word == "biopic":
        word = "documentary"

    link = "www.google.com/search?q=best+" + word + "+movies"
    http_pool = url.connection_from_url(link)
    r = http_pool.urlopen('GET', link)
    http_pool.close()
    html = r.data.decode('latin-1')
    soup = b(html, 'html.parser')
    
# original code by Arnav, modified by Lorenzo. If something breaks, check how the google page was changed and cry
    for a in soup.find_all("a"):
      #the HTML page has a div that contains the year, and "above" it there is a 
      #div with the movie name. Everything is enclosed in a <a> tag.
      #However, the div is often truncated, so we find the movie name in the link that
      #the <a> tag points to
      if a.has_attr('class') and "q=" in a['href'] and a.find_all(string=re.compile("^(19|20)\d+$")):
       	searchparams = urllib.parse.parse_qs('http://www.google.com'+a['href'])
       	if 'q' in searchparams:
        	movies.append(searchparams['q'][0])
    
    for i in movies:
        done = False
        if len(i) > 1:
            res = n.pos_tag(n.word_tokenize(i))
            if len(res) > 1:
                s = ""
                for j in res:
                    # print(j)
                    if j[1] == "NNP" and not done:
                        s = s + firstName + " "
                        done = True
                    else:
                        s = s + j[0] + " "
                if firstName in s:
                    results.append(s[:-1])

    return results

#print(getMovieNicknames2("adventure", "Arnav"))

def question1(text):
    # question1 = input("\n What is your name?\n")
    if len(text) > 0:
        text = text.split(" ")
        t = []
        for i in text:
            if not i == "":
                t.append(i)
        text = t
        if len(text) > 0:
            length = len(text)
            global firstName
            global middleName
            global lastName

            if length == 3:
                cap1 = text[0][0].upper()
                cap2 = text[1][0].upper()
                cap3 = text[2][0].upper()
                firstName = cap1 + text[0][1:]
                middleName = cap2 + text[1][1:]
                lastName = cap3 + text[2][1:]
                thread = threading.Thread(target=rhyme, args=(firstName,))
                thread.start()

            elif length == 2:
                cap1 = text[0][0].upper()
                cap2 = text[1][0].upper()
                firstName = cap1 + text[0][1:]
                lastName = cap2 + text[1][1:]
                thread = threading.Thread(target=rhyme, args=(firstName,))
                thread.start()

            elif length == 1:
                cap1 = text[0][0].upper()
                firstName = cap1 + text[0][1:]
                thread = threading.Thread(target=rhyme, args=(firstName,))
                thread.start()
            return True
        else:
            return False
    else:
        return False


def question2(m):
    sportsCandidates = []
    sports = getWikiSports()
    tagged = []
    m = m.lower()
    print(m)

    if "no" in m or "none" in m or "not really" in m or "nope" in m:
        # print("yes")
        return -1

    m = n.word_tokenize(m)
    temp = normalize(n.pos_tag(m))
    sNouns = nounGetter(temp)
    sVerbs = verbGetter(temp)

    # print(sports)
    for i in sNouns:
        if i in sports:
            tagged.append(i)

    for i in sVerbs:
        if i in sports:
            tagged.append(i)

    if len(tagged) < 1:
        return []

    for i in tagged:
        c = getConceptTermsWithContext(i)
        for h in c:
            global firstName
            s = h + " " + firstName
            sportsCandidates.append(s)

    return sportsCandidates


def question3(m):
    terms = []

    m = m.lower()

    if "no " in m or "none " in m or "not really " in m or "nope " in m:
        return -1

    m = n.word_tokenize(m)
    for i in m:
        test = " " + i.lower() + " "
        if test in movieGenres:
            terms.append(i)
    results = []

    global firstName
    for i in terms:
        r = getMovieNicknames2(i, firstName)
        for j in r:
            temp = j.split(" ")
            if len(temp) > 2:
                if " & amp ; " in j:
                    j = j.replace(" & amp ; ", " & ")
                    results.append(j)
                else:
                    results.append(j)


    return results


def giveNickname(boolean, m):

    print("Generating Rhyming Nickname")
    m = m.lower()
    # rhymingNames = rhyme(firstName)

    # result = [rhymingNames]
    global rhymingNames
    global personal

    while isinstance(rhymingNames, int):
        time.sleep(2)

    if boolean or len(rhymingNames) < 1:
        personal = True
        if "sport" in m:
            nickname = random.choice(sportsNames)
            return "\"" + capitalize(nickname) + "\""
        elif "movie" in m:
            nickname = random.choice(movieNames)
            return"\"" + capitalize(nickname) + "\""
        # return result

    else:
        personal = False
        nickname = random.choice(rhymingNames)
        nickname = "\"" + capitalize(nickname) + " " + firstName + "\""
        return nickname


def writeToJSON(dict, file):
    try:
        with open(file) as f:
            data = json.load(f)
    except json.decoder.JSONDecodeError:
        data = {}

    data.update(dict)

    with open(file, 'w') as f:
        json.dump(data, f)


def getIndexFromJson(file):
    with open(file) as f:
        data = json.load(f)

    keys = list(data.keys())
    # print(keys)
    if len(keys) > 0:
        # print(int(keys[-1]))
        return int(keys[-1])
    else:
        return -1


def personalChoice(file):
    with open(file) as f:
        data = json.load(f)

    keys = list(data.keys())
    pers = 0
    nonpers = 0

    if len(keys) > 0:
        for i in keys:
            if data[i]["personal"]:
                pers += 1
            else:
                nonpers += 1

    if pers > nonpers:
        print("Personal count: " + str(pers))
        print("Non-personal count: " + str(nonpers))
        # print(False)
        return False
    elif pers < nonpers:
        print("Personal count: " + str(pers))
        print("Non-personal count: " + str(nonpers))
        # print(True)
        return True
    else:
        choice = random.choice([0, 1])
        if choice == 0:
            print("Personal count: " + str(pers))
            print("Non-personal count: " + str(nonpers))
            # print(True)
            return True
        else:
            print("Personal count: " + str(pers))
            print("Non-personal count: " + str(nonpers))
            # print(False)
            return False


def printBalance(file):
    with open(file) as f:
        data = json.load(f)

    keys = list(data.keys())
    pers = 0
    nonpers = 0

    if len(keys) > 0:
        for i in keys:
            if data[i]["personal"]:
                pers += 1
            else:
                nonpers += 1

    print("Personal tests: " + str(pers))
    print("Non-personal tests: " + str(nonpers))

printBalance("data.json")

def smallTalk(index):
    time.sleep(random.randint(3,5))
    eel.changeHTML(smalltalkies[index])
    global smalltalk

    if index == len(smalltalkies)-1:
        smalltalk = True
    else:
        smalltalk = False
    return smalltalkies[index]


#%% Program
movieGenres = getMovieGenres()

eel.init('web')
message = "base"

# @eel.expose
# def py_random():
#     return random.random()

@eel.expose
def py_send(n):
    eel.send(n)(print_result)

@eel.expose
def print_result(n):
    global message
    message = n


eel.start('main2.html', size=(500, 800), block=False)


global personal
personal = personalChoice("data.json")
personal = False
print("Personal Nickname is: " + str(personal))

index = 0
currentQuestion = ""
running = True

sportsNames = []
movieNames = []
sportsAnswer = ""
movieAnswer = ""

while running:
    eel.sleep(1)
    if not message == "base" and len(message) > 1:
        if message == "ready" and not qs[0]:
            eel.changeHTML(qtexts[0])
            currentQuestion = qtexts[0]
            message = "base"
        elif not qs[0]:
            if question1(message):
                qs[0] = True
                eel.changeHTML(smalltalkies[index])
                currentQuestion = smalltalkies[index]
                index += 1
                message = "base"
            else:
                message = "base"
                eel.changeHTML("I am sorry, what was your name?")
                currentQuestion = "I am sorry, what was your name?"

        elif not smalltalk:
            smallTalk(index)
            currentQuestion = smallTalk(index)
            index += 1
            message = "base"
        elif not qs[1]:
            sportsNames = question2(message)
            print(sportsNames)
            if isinstance(sportsNames, list):
                if len(sportsNames) > 1:
                    qs[1] = True
                    sportsAnswer = message
                    message = "base"
                    eel.changeHTML(qtexts[3])
                    currentQuestion = qtexts[3]
                else:
                    eel.changeHTML(qtexts[2])
                    currentQuestion = qtexts[2]
                    message = "base"
            elif sportsNames == -1:
                eel.changeHTML("Alright but if you had to pick a sport, which would it be?")
                currentQuestion = "Alright but if you had to pick a sport, which would it be?"
                message = "base"

        elif not qs[2]:
            movieNames = question3(message)
            print(movieNames)
            if isinstance(movieNames, list):
                if len(movieNames) > 1:
                    qs[2] = True
                    movieAnswer = message
                    message = "base"
                    eel.changeHTML(qtexts[5])
                    currentQuestion = qtexts[5]
                else:
                    eel.changeHTML(qtexts[4])
                    currentQuestion = qtexts[4]
                    message = "base"
            elif movieNames == -1:
                eel.changeHTML("Alright but if you had to pick a genre, which would it be?")
                currentQuestion = "Alright but if you had to pick a genre, which would it be?"
                message = "base"

        elif not qs[3]:
            # print(personal)
            final = giveNickname(personal, message)
            print(final)
            eel.changeHTML("I like the nickname " + str(final) + ". I think I'm going to call you that from now on. \n \n"
                                                            "Well I've got some computer-related stuff to get to so I'll catch you later, "
                                                            + str(final) + "!")
            eel.removeHTML()
            qs[3] = True

            index = getIndexFromJson("data.json") + 1
            # print("Index from JSON; " + str(index - 1) + " Current index: " + str(index))
            data = {index: {"participantName": firstName,
                            "personal": personal,
                            "nickname": str(final),
                            "sportsAnswer:": sportsAnswer,
                            "movieAnswer:": movieAnswer,
                            "sports": sportsNames,
                            "movies": movieNames,
                            "rhymes": rhymingNames
                            }}
            writeToJSON(data, "data.json")
            message = "base"
            running = False
            printBalance('data.json')
    elif len(message) < 1:
        # print("here")
        eel.changeHTML("Sorry I didn't get that. " + currentQuestion)
        message = "base"


#
# # print("\n Hey there, I am your new personal assistant. "
# #       "In order to get to know you better, I'm going to ask you a few questions.\n")
#
#
# # %% Question 1
#
# # def question1():
# #     question1 = input("\n What is your name?\n")
# #     question1 = question1.split(" ")
# #     length = len(question1)
# #
# #     if length == 3:
# #         firstName = question1[0]
# #         middleName = question1[1]
# #         lastName = question1[2]
# #         return [firstName, middleName, lastName]
# #     elif length == 2:
# #         firstName = question1[0]
# #         lastName = question1[1]
# #         return [firstName, lastName]
# #     elif length == 1:
# #         firstName = question1[0]
# #         return [firstName]
#
#
#
#
#
# # %% Question 2
#
# q2Sufficient = False
# count = 0
# sportsCandidates = []
# # firstName = "Arnav"
#
# # def question2(asked):
# #     sportsCandidates = []
# #     tagged = []
# #     names = []
# #
# #     if asked:
# #         question2 = input("\n I am sorry, I don't know the sports you mentioned :( Check if you spelled it"
# #                           " right or try some others \n")
# #         question2 = n.word_tokenize(question2)
# #         temp = normalize(n.pos_tag(question2))
# #         sNouns = nounGetter(temp)
# #         sVerbs = verbGetter(temp)
# #
# #     else:
# #         question2 = input("\n Alright, do you play or follow any sports? \n")
# #         question2 = n.word_tokenize(question2)
# #         temp = normalize(n.pos_tag(question2))
# #         sNouns = nounGetter(temp)
# #         sVerbs = verbGetter(temp)
# #
# #     # question2 = input("\n Alright " + question1[0] + ", do you play or follow any sports? \n")
# #
# #
# #
# #     for i in sNouns:
# #         if i in sports:
# #             tagged.append(i)
# #
# #     for i in sVerbs:
# #         if i in sports:
# #             tagged.append(i)
# #
# #     for i in tagged:
# #         # c = getConceptSports(i)
# #         c = getConceptTermsWithContext(i)
# #         # if len(c) < 3:
# #         #     c = c + getConceptDerivedTerms(i)
# #         for h in c:
# #             sportsCandidates.append(h)
# #
# #     for i in sportsCandidates:
# #         names.append(i + " " + firstName)
# #
# #     return names
#
#
#
# while not q2Sufficient:
#
#     if count == 0:
#         sportsCandidates = question2(False)
#     else:
#         sportsCandidates = question2(True)
#
#     if len(sportsCandidates) < 1:
#         q2Sufficient = False
#     else:
#         q2Sufficient = True
#
#     count += 1
#
# # print(sportsCandidates)
#
#
# # %% Question 3
#
# movieCandidates = []
# sufficient = False
# count = 0
# terms = []
# firstName = "Arnav"
#
# movieGenres = getMovieGenres()
#
#
# def question3(m):
#     mNouns = []
#     terms = []
#
#     m = n.word_tokenize(m)
#     tagged = normalize(n.pos_tag(m))
#     mNouns = nounGetter(tagged)
#
#     for i in mNouns:
#         if i in movieGenres:
#             terms.append(i)
#     results = []
#
#     for i in terms:
#         r = getMovieNicknames(i, firstName)
#         for j in r:
#             results.append(j)
#
#     return results
#
#
#
# # def question3(asked):
# #     mNouns = []
# #     terms = []
# #
# #     if not asked:
# #         question3 = input("\n I see, and what about movies? Do you have a favourite genre? \n")
# #         question3 = n.word_tokenize(question3)
# #
# #         tagged = normalize(n.pos_tag(question3))
# #
# #         mNouns = nounGetter(tagged)
# #
# #     else:
# #         question3 = input("\n I am sorry, I don't know those genres, can you name some others? \n")
# #         question3 = n.word_tokenize(question3)
# #
# #         tagged = normalize(n.pos_tag(question3))
# #
# #         mNouns = nounGetter(tagged)
# #
# #     print(mNouns)
# #     for i in mNouns:
# #         if i in movieGenres:
# #             terms.append(i)
# #     # print(terms)
# #     results = []
# #
# #     for i in terms:
# #         r = getMovieNicknames(i, firstName)
# #         for j in r:
# #             results.append(j)
# #
# #     return results
#
#
# while not sufficient:
#
#     if count == 0:
#         movieCandidates = question3(False)
#     else:
#         movieCandidates = question3(True)
#
#     if len(movieCandidates) < 1:
#         sufficient = False
#     else:
#         sufficient = True
#
#     count += 1
#
#
#
#
# # %% Question 4
#
# # bookCandidates = []
# #
# # question4 = input("\n Hmm, alright and what about books? What kinds of books do you like to read? \n")
# # question4 = n.word_tokenize(question4)
# # tagged = normalize(n.pos_tag(question4))
# #
# # musicNouns = nounGetter(tagged)
# # musicVerbs = verbGetter(tagged)
# #
# # temp = []
# #
# # for i in musicNouns:
# #     if i in bookGenres:
# #         temp.append(i)
# #
# # for i in temp:
# #     c = getConceptNetWords(i)
# #     for j in c:
# #         bookCandidates.append(j)
# # for i in bNouns:
# #     # temp = getCandidates(i)
# #     temp = getConceptNetWords(i)
# #     temp = filter(temp)
# #     for j in temp:
# #         bookCandidates.append(j)
# #
# # for i in bVerbs:
# #     temp = getConceptNetWords(i)
# #     temp = filter(temp)
# #     for j in temp:
# #         bookCandidates.append(j)
#
# # for i in bookCandidates: print(i)
#
# # %% Question 5
#
# # question5 = input("\n And finally, would you say that you are more \"sporty\", a \"movie-buff\",a \"bookworm\" or \"none\"? "
# #                   "(You can only choose one, and please use the word I used; I can't read very well)\n \n")
#
# question5 = input("\n And finally, would you say that you like sports or movies more? "
#                   "You can only choose one!\n \n")
#
# question5 = n.word_tokenize(question5)
#
# def question4(m):
#     m = n.word_tokenize(m)
#     if "sport" in m:
#         sporty = True
#     elif "movie" in m:
#         movie = True
#     else:
#         boring = True
#
# # %% Generate personalized nickname
# nickname = ''
#
# # for i in sportsCandidates: print(i)
#
# if sporty:
#     nickname = random.choice(sportsCandidates)
# elif movie:
#     nickname = random.choice(movieCandidates)
# else:
#     nickname = random.choice(['boring', 'lame', 'get a hobby', 'do nothing', 'couch-potato'])
#
#
# print('Great, I gotta go do some computer-related stuff now, catch you later ' + capitalize(nickname))
#
#
# # %% Generate rhyming nickname
#
# names = []
# firstName = "Aart"
# rhymingNames = rhyme(firstName)
#
# nickname = random.choice(rhymingNames)
# print(nickname + " " + firstName)














