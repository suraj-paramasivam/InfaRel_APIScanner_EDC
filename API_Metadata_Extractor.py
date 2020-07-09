# Author: Suraj T Paramasivam
# Company: Informatica
# Purpose: Extraction of Metadata from API response to be ingested into EDC

import csv
import json
from zipfile import ZipFile

import requests
from more_itertools import unique_everseen

# put the api in the yaml file please

##url = params['url']
##xfdpapikey=params['x-fdpapikey']

url = 'Your API Method URL'

payload = {}
headers = {
    'Accept': 'application/json',
    # You will need to change the apikey with the parameter based on the API. If using a different auth mechanism, change code accordingly
    'x-fdpapikey': 'Your API Key'
}

try:
    resp = requests.request("GET", url, headers=headers, data=payload, verify=False)
    data = json.loads(resp.text)
    parsed_data = data['value']
    t4 = []

    for d in parsed_data:
        t4 = list(d.keys())
except:
    print("Something went wrong with getting data from API")


def get_links(obj, indices):
    for k, v in obj.items() if isinstance(obj, dict) else enumerate(obj):
        if isinstance(v, (dict, list)):
            yield from get_links(v, indices + [k])
        else:
            yield indices + [k]


try:
    with open('links1.csv', 'w+', newline='') as linksfile:
        writer1 = csv.writer(linksfile)
        writer1.writerow(['association', 'fromObjectIdentity', 'toObjectIdentity'])

        for a in get_links(data, []):

            r = 0
            no_integers = [x for x in a if not isinstance(x, int)]

            l = len(no_integers)
            l1 = len(t4)
            # print(l)
            if no_integers[0] == 'paginationmetadata' or no_integers[0] == 'links':
                pass
            else:
                while (r < l - 1):
                    if no_integers[0] == 'value':
                        writer1.writerow(['com.slb.custom.api.fdp3.APITable2Field', no_integers[r], no_integers[r + 1]])
                    r += 1
except:
    print(
        "Couldn't open intermediate file(links1.csv) in write mode, please check if the file is already opened by you or someone else")

try:
    with open('links1.csv', 'r') as f1, open(
            'links2.csv', 'w+') as f2:
        f2.writelines(unique_everseen(f1))

except:
    print("Couldn't open the links or links1.csv file in write mode, please close the file and retry")

old_str = 'com.slb.custom.api.fdp3.APIField2Field'
new_str = 'com.slb.custom.api.fdp3.APITable2Field'

r = csv.reader(open('links2.csv'))
lines = list(r)

try:
    with open('links.csv', 'w+', newline='') as links:
        f = csv.writer(links)
        for i in range(len(lines)):
            if lines[i][1] == 'value':
                lines[i][0] = 'com.slb.custom.api.fdp3.APISystem2Table'
            f.writerow(lines[i])

except:
    print("Something is wrong with links.csv, please close the file if it is open")


def show_indices(obj, indices):
    for k, v in obj.items() if isinstance(obj, dict) else enumerate(obj):
        if isinstance(v, (dict, list)):
            yield from show_indices(v, indices + [k])
            if k == 0:
                break
        else:
            yield indices + [k]


t2 = []
t3 = []
for keys in show_indices(data, []):
    for k in keys:
        t2.append(k)
for i in t2:
    if i not in t3:
        t3.append(i)

# for j in t4:
#    if j not in t3:
#        t3.append(j)
# print(t3)

with open('objects.csv', 'w+', newline='') as objectsfile:
    writer = csv.writer(objectsfile)
    writer.writerow(['class', 'identity', 'core.name', 'core.description', 'com.slb.custom.api.fdp.URL'])
    writer.writerow(['com.slb.custom.api.fdp3.System', 'value', 'value', 'FDP API', url])
    for i in t4:
        writer.writerow(['com.slb.custom.api.fdp3.APITable', i, i, 'API Table', ''])
    for i in t3:
        if str(i) != '0' and str(i) != 'value' and str(i) not in t4:
            writer.writerow(['com.slb.custom.api.fdp3.Field', i, i, 'API Field', ''])

zipf = ZipFile('fdp.zip', 'w')
zipf.write('objects.csv')
zipf.write('links.csv')
zipf.close()
