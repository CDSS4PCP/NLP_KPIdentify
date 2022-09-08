from utils.get_date import get_date
# from data_extraction.pubmed.classes.trigger_pubmed_efetch import trigger_pubmed_efetch
from metamap.run_metamap_code.classes.run_metamap import run_metamap

#generate medline extract for processing in metamap
# get_date_obj = get_date()
# trigger_pubmed_efetch_obj = trigger_pubmed_efetch(get_date_obj, output_directory='/home/rgoli/MetaMap-src/data/pubmed_data/pubmed_extracts_medline_format/',output_file='test_out_medline.txt', output_format='medline')
# trigger_pubmed_efetch_obj.run_edirect()

#run metamap
run_metamap_obj=run_metamap()
run_metamap_obj.run()

