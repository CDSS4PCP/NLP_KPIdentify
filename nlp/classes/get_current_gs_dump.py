import psycopg2

class get_current_gs_dump:
    def __init__(self, conn):
        self.conn = conn
    
    def get_dump(self):
        sql = 'select gs_term,gs_id from gold_standard_terms_agg_view'
        cursor = self.conn.cursor()
        
        try:
            cursor.execute(sql)
            gs_terms = cursor.fetchall()
        
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
        
        finally:
            cursor.close()
        
        return gs_terms
