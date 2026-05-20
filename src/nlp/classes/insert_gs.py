import glob
import psycopg2
import psycopg2.extras as extras
from datetime import datetime
import subprocess


class insert_gs:
    def __init__(self, conn, abs_base_dir='/home/rgoli/MetaMap-src/data/gold_standard/AnnotationResults_Abstracts/', 
                 ft_base_dir='/home/rgoli/MetaMap-src/data/gold_standard/AnnotationResults_full_text/', page_size=200,
                done_dir='/home/rgoli/MetaMap-src/data/gold_standard/AnnotationResults_Abstracts/done/'):
        
        self.conn = conn
        self.abs_base_dir=abs_base_dir
        self.ft_base_dir=ft_base_dir
        self.page_size= page_size
        self.done_dir = done_dir
        
    
    def get_files_to_process(self):
        abs_files = glob.glob(self.abs_base_dir+'**/*.txt', recursive = True)
        ft_files = glob.glob(self.ft_base_dir+'**/*.txt', recursive = True)
        
        return abs_files, ft_files
    
    def insert_data(self):
        abs_files, ft_files = self.get_files_to_process()
        values_list=[]
        
        sql = """
        INSERT INTO gold_standard_terms (gs_id, gs_term, sys_creation_date, sys_update_date, app_id, active, expiration_date, term_text_type, primary_paper_id, other_id)
        VALUES %s
        """
        
        for file in abs_files:
            my_file = open(file, "r")
            content = my_file.read()
            gs_list = content.split('\n')
            my_file.close()
            
            pmid = gs_list[0]
            gs_list = gs_list[1:]
            
    
            for term in gs_list:
                if term.strip() == '':
                    continue
                value_tuple = (term.strip().lower(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'cdssadmin', 'Y', 
                               None, 'abs', pmid, None)
                values_list.append(value_tuple)
        
        sequence_required = len(values_list)
        cursor = self.conn.cursor()
        get_sequences='''select nextval('gs_term_id') from generate_series(1,'''+str(sequence_required)+''')'''
        cursor.execute(get_sequences)
        sequences = cursor.fetchall()
        new_values_list=[]
        for value_tuple in values_list:
            value_tuple = sequences.pop(0) + value_tuple
            new_values_list.append(value_tuple)
        
        #return new_values_list
        
        try:
            extras.execute_values(cursor, sql, new_values_list, page_size = self.page_size)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            cursor.close()
            return 1
        print("execute_values() done")
        cursor.close()
        
        #move all files to done
        for file in abs_files:
            move_command='mv '+ file + ' '+self.done_dir+file.split('/')[-1]+'.done'
            p = subprocess.Popen([move_command], shell=True)
            out, err = p.communicate()
