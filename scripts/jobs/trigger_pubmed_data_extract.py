from src.utils.get_date import get_date
from src.data_pipeline.pubmed.classes.trigger_pubmed_efetch import trigger_pubmed_efetch

get_date_obj = get_date()
trigger_pubmed_efetch_obj = trigger_pubmed_efetch(get_date_obj, output_file='full_data.xml', output_format='xml')
trigger_pubmed_efetch_obj.run_edirect()
