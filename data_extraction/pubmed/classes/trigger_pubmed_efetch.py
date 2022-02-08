#from classes.get_date import get_date
import subprocess,os
from datetime import datetime

class trigger_pubmed_efetch:
    def __init__(self, get_date_obj, output_directory='/home/rgoli/MetaMap-src/data/pubmed_data/raw_data/', output_file='test_out.xml', output_format='xml', db='pubmed'):   
        #get batch date
        #get_date_obj= get_date()
        date_pd = get_date_obj.run_query()
        self.mindate = date_pd['cur_execution_date'][0].strftime("%Y/%m/%d")

        #other parameters
        self.db=db
        self.output_file=output_file
        self.output_directory = output_directory
        self.output_format=output_format
        self.query="Decision Support Systems, Clinical[MeSH Terms] AND (manage*[Title/Abstract] OR rule*[Title/Abstract] OR monitor*[Title/Abstract] OR operat*[Title/Abstract])"
    
    def run_edirect(self):
        #e-direct command
        edirect_command_str = '''data_extraction/pubmed/installation/edirect/esearch -db '''+self.db+''' -query "'''+self.query+'''" -mindate '''+self.mindate+''' | data_extraction/pubmed/installation/edirect/efetch -format '''+self.output_format+''' > ''' + self.output_directory + self.output_file
        print(edirect_command_str)

        # p = subprocess.Popen([edirect_command_str], shell=True)
        # out, err = p.communicate()
