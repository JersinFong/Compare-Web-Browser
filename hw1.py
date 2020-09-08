import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from html.parser import HTMLParser
import json
import csv
from urllib.parse import unquote

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def search(query, will_sleep=True):
  if will_sleep: # Prevents loading too many pages too soon
    sleep(randint(1, 10))
  temp_url = '+'.join(query.split()) #for adding + between words for the query
  url = 'http://search.yahoo.com/search?p=' + temp_url + '&n=10'
  print("run")
  soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
  new_results = scrape_search_result(soup)
  return new_results

def scrape_search_result(soup):
  raw_results = soup.find_all("a",  attrs = {"class" : "ac-algo fz-l ac-21th lh-24"})
  results = []
  #implement a check to get only 10 results and also check that URLs must not be duplicated
  for result in raw_results:
    link = result.get('href')
    results.append(unquote(link[link.find("RU=") + 3:link.find("/RK")]))  
  return results


def readfile(file_name):
  with open(file_name) as f:
    lines = [line.rstrip() for line in f]
  return lines


def readJson(file_name):
  f = open(file_name)
  data = json.load(f)
  return data


def writeJson(file_name, data):
  json_object = json.dumps(data, indent = 2)
  with open(file_name, 'w') as outfile:
    outfile.write(json_object)



def scrapping_results(inputFile, outPutFile):
  queries = readfile(inputFile)
  results_json = {}
  for query in queries:
    links = search(query, True)
    print(links)
    results_json[query] = links
  writeJson(outPutFile, results_json)


def is_same_link(link1, link2):
  return True


def calc_correlation(ranks):
  di_sum = 0
  n = len(ranks)
  if n == 1 :
    if(ranks[0][0] == ranks[0][1]): return 1
    return 0
  for rank in ranks:
    di_sum += (rank[0] - rank[1]) * (rank[0] - rank[1])
  return 1 - 6 * di_sum / n * (n * n - 1)



def compute_statistics(json_file_search, json_file_reference):
  data_search = readJson(json_file_search)
  data_reference = readJson(json_file_reference)
  query_num = 1
  res = []
  for key in data_search:
    links_search = data_search[key]
    links_reference = data_reference[key]
    ranks = []
    for i in range(0, len(links_search)):
      for j in range(0, len(links_reference)):
        if is_same_link(links_search[i], links_reference[j]):
          ranks.append([i + 1, j + 1])
    rs = calc_correlation(ranks)
    res.append["Query " + query_num, len(ranks), len(ranks) / 10, rs]
  with open('hw1.csv', 'w', newline='') as csvfile:
    res_writer = csv.writer(csvfile, delimiter=', ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    res_writer.writerows(res)
    




#############Driver code############
scrapping_results('100QueriesSet2.txt', 'hw1.json')
# SearchEngine.compute_statistics('hw1.json', 'Google_Result2.json')     

####################################
#############Driver code############
# print(SearchEngine.readJson('Google_Result2.json')["Some important facts on the respiratory system"])
# print(SearchEngine.readfile('100QueriesSet2.txt'))
# print(SearchEngine.search("Some important facts on the respiratory system"))
####################################