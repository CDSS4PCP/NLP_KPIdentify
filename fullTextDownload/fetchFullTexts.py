from Bio import Entrez
import lxml
import json
from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
import re
import urllib3
import time

Entrez.email = "rgoli@clemson.edu"

HEADERS = {
    'X-ELS-APIKEY': "d63ecea23ea6f1b9645368e2288b2172",
    'Accept': 'application/pdf'
}

pattern = re.compile('S\d+-\d+\(\d+\)\d+-\d+')
BASE_DIR = "data/gold_standard/AnnotationResults_full_text/"

## Download Full text using PMC ID in XML format
# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=5854965&tool=my_tool&email=rgoli@clemson.edu
# https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:5854965&metadataPrefix=pmc

class fetchFullTexts:
    def __init__(self):
        return

    def get_elseiver_pdf(doi, file_to_save_to):
        url = f'http://api.elsevier.com/content/article/doi/{doi}?httpAccept=application/pdf'
        request = requests.get(url, headers=HEADERS)
        file_to_save_to.write(request.content)

if __name__ == "__main__":
    with open('pmids_to_download.txt') as f:
        pmids = f.read()
    pmid_list= ','.join(pmids.split())
    # print(pmid_list.strip())

    fetchHandle = Entrez.esummary(db="pubmed", id=pmid_list, retmode="xml")

    records = Entrez.parse(fetchHandle)

    # create session
    session = requests.Session()
    for record in records:
        x_rec = record['ArticleIds']
        if 'pmc' in x_rec:
            print(x_rec['eid'], 'http://www.ncbi.nlm.nih.gov/pmc/articles/%s/pdf/' % (x_rec['pmc']))
            pmc = x_rec['pmc']
            url = f'http://www.ncbi.nlm.nih.gov/pmc/articles/{pmc}/pdf'
            # http = urllib3.PoolManager()
            # print(url)
            # response = http.request('GET', url)
            # soup = BeautifulSoup(response.data,features='lxml')
            # soup_extract = soup.find_all("div", class_="el-exception-url")
            # print(soup_extract)
            # pdf_to_download = re.findall('((http)s?://.*?\.pdf)', soup_extract)
            # print(pdf_to_download)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
            req = session.get(url,headers=headers, stream=True)
            # req.raise_for_status()
            # req = requests.get(soup_extract,allow_redirects=True)
            with open(BASE_DIR+x_rec['eid']+"_ncbiDirect.pdf",'wb') as pdf_file:
                pdf_file.write(req.content)
        # elif('pii' in x_rec):
        #     if pattern.match(x_rec['pii']):
        #         print(x_rec['doi'],x_rec['pii'])
        #         doi = x_rec['doi']
        #         req = requests.get(f'http://api.elsevier.com/content/article/doi/{doi}?httpAccept=application/pdf', headers=HEADERS)
        #         with open(BASE_DIR+x_rec['eid']+"_elseiver.pdf",'wb') as pdf_file:
        #             pdf_file.write(req.content)
        # else:
        #     print(x_rec)
    session.close()
    fetchHandle.close()
