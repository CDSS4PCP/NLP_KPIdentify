import glob
import subprocess

class run_metamap:
    def __init__(self, metamap_path='/home/rgoli/MetaMap-src/metamap/public_mm/bin/metamap', output_directory='/home/rgoli/MetaMap-src/datametamap_data/metamap_results/', input_search_directory='/home/rgoli/MetaMap-src/datapubmed_data/raw_data/', metamap_options=['--JSONf 2', '-D', '-y']):
        self.metamap_path=metamap_path
        self.output_directory=output_directory
        self.input_search_directory=input_search_directory
        self.metamap_options=metamap_options
        
        
    def run(self):
        files=glob.glob(self.input_search_directory+'*.medline')
        for file in files:
            outfile = self.output_directory+'metamap_processed_'+file.split('/')[-1].split('.')[0]+'.json'
            run_command = self.metamap_path+''' '''+' '.join(self.metamap_options)+''' '''+file+''' '''+outfile
            print(run_command) 
            
            p = subprocess.Popen([run_command], shell=True)
            out, err = p.communicate()
            
            move_command='mv '+file+' '+'/'.join(file.split('/')[:-1])+'/done/'+file.split('/')[-1]+'.done'
            print(move_command)
            
            p = subprocess.Popen([move_command], shell=True)
            out, err = p.communicate()
