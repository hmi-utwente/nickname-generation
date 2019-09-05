## connect to conceptNet here
# searchTerm = "basketball"
# # link = "http://api.conceptnet.io/c/en/"
# link = "http://api.conceptnet.io/query?rel=/r/IsA&end=/c/en/"
#
# results = r.get(link+searchTerm).json()
#
# with open('personal.json', 'w') as file:
#     json.dump(results, file)
#
# c = []
#
# # Get relevant words from ConceptNet
#
# for e in results['edges']:
#     print(e)
#     if e['start']['language'] == 'en' and searchTerm not in e['start']['label'].lower():
#         c.append(e['start']['label'])

t = ['apple', 'banana', 'orange']
l = ['fruit', 'vegetable', 'apple']
# print(list(set(t) - set(l)))


test = "arnav"
print(len(test.split(" ")))



for i in range(4):
    print(i)