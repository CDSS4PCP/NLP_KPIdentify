import psycopg2
import psycopg2.extras as extras
import pubmed_parser as pp
from datetime import datetime

class parse_pubmed_and_insert:
    def __init__(self, conn):
        self.conn = conn
    
    def parse_xml_csv(self, file):
        dicts_out = pp.parse_medline_xml(file,
                                         year_info_only=False,
                                         nlm_category=False,
                                         author_list=False,
                                         reference_list=False)
        values_list=[]
        for item in dicts_out:
            temp_dict={}
            for k,v in item.items():
                if k=='title':
                    temp_dict['title']=v
                if k=='abstract':
                    temp_dict['abstract']=v
                if k=='pmid':
                    temp_dict['pmid']=v
                if k=='pmc':
                    temp_dict['pmc']=v
                if k=='authors':
                    temp_dict['authors']=v
                if k=='pubdate':
                    temp_dict['pubdate']=v
                if k=='journal':
                    temp_dict['journal']=v
                if k=='country':
                    temp_dict['country']=v
                if k=='mesh_terms':
                    temp_dict['mesh_terms']=v

            dt = datetime.now()
            current_time= dt.strftime("%Y-%m-%d %H:%M:%S")

            temp_tuple=(temp_dict['pmid'], current_time, current_time, 'cdssadmin', temp_dict['pmc'],
                       temp_dict['title'], temp_dict['authors'], temp_dict['pubdate'], temp_dict['journal'],
                       temp_dict['country'], temp_dict['abstract'], temp_dict['mesh_terms'], 1)
            values_list.append(temp_tuple)
           
        
        return values_list
    
    def insert_data(self, file):
        
        values_list = self.parse_xml_csv(file)
        
        cursor = self.conn.cursor()
    
        sql = """
        INSERT INTO raw_data (id, sys_creation_date, sys_update_date, app_id, other_id, title, authors, pubdate, journal, 
        country, abstract, keywords, source)
        VALUES %s
        """
        
        try:
            extras.execute_values(cursor, sql, values_list, page_size=200)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            cursor.close()
            return 1
        print("execute_values() done")
        cursor.close()
