# Author: Suraj T Paramasivam
# Company: Informatica
# Purpose: Extraction of Metadata from API Yaml definition(OpenAPI 3.0 or above) to be ingested into EDC

import csv
import json
from zipfile import ZipFile

import yaml

configfile = "config.yaml"
with open(configfile, 'r') as conf:
    files = yaml.load_all(conf, Loader=yaml.FullLoader)
    for k in files:
        filelist = k

url = filelist['url']

ipfile = filelist['yamlfile_input']
jsonfile = filelist['jsonfile_output']
jsonfile1 = filelist['jsonfile_output']
opzipfile = filelist['zipfile_output']

with open(
        ipfile,
        "r") as yamlfile, open(jsonfile, 'w+') as jsonfile:
    yamlobj = yaml.safe_load(yamlfile)
    json.dump(yamlobj, jsonfile)

with open(jsonfile1, "r") as jsonbase:
    data = json.load(jsonbase)

parsed_data = data['components']['schemas']

t4 = list(parsed_data.keys())
# print(t4)
with open('objects.csv', 'w+', newline='') as objectsfile, open('links.csv', 'w+', newline='') as linksfile:
    writer = csv.writer(objectsfile)
    writer_links = csv.writer(linksfile)
    writer.writerow(
        ['class', 'identity', 'core.name', 'core.description', 'com.slb.custom.api.URL', 'com.slb.custom.api.datatype'])
    writer_links.writerow(['association', 'fromObjectIdentity', 'toObjectIdentity'])

    writer.writerow(['com.slb.custom.api.System', 'value', 'FDP', 'FDP API', url])
    for i in t4:
        writer.writerow(['com.slb.custom.api.Object', i, i, 'API Table', ''])
        writer_links.writerow(['com.slb.custom.api.SystemObject', 'value', i])
        fields1 = data['components']['schemas'][i]['properties'].keys()
        dt1 = data['components']['schemas'][i]['properties'].values()
        for d in dt1:
            t5 = d['type']

        for f in fields1:
            writer.writerow(['com.slb.custom.api.Field', i + '.' + f, f, 'API Field', '', t5])
            writer_links.writerow(['com.slb.custom.api.ObjectField', i, i + '.' + f])

zipf = ZipFile(opzipfile, 'w')
zipf.write('objects.csv')
zipf.write('links.csv')
zipf.close()
