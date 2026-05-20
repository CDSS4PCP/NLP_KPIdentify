from classes.trigger_pubmed_efetch import trigger_pubmed_efetch

trigger_pubmed_efetch_obj = trigger_pubmed_efetch(output_file='output/test_out.xml')
trigger_pubmed_efetch_obj.run_edirect()
