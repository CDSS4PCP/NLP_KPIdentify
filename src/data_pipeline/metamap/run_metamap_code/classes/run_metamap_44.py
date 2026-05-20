import glob
import subprocess

class run_metamap_44:
    def __init__(self, metamap_path='/home/rgoli/MetaMap-src/metamap/public_mm/bin/metamap', 
                 output_directory='/home/rgoli/MetaMap-src/data/metamap_data/metamap_results/44_abstract/', 
                 input_search_directory='/home/rgoli/MetaMap-src/data/pubmed_data/raw_data/', 
                 metamap_default_options = '--JSONf 2', 
                 behavioral_options = ['--conj', '-Q', '--prune 10', '--no prune', '-t', '-d', '-D', '-a', '-u', '-l', '-r 700', '-i', '-y']):
        self.metamap_path=metamap_path
        self.output_directory=output_directory
        self.input_search_directory=input_search_directory
        self.metamap_default_options=metamap_default_options
        self.behavioral_options = behavioral_options
        
        
    def run(self):
        file=self.input_search_directory+'44_abstracts_test.medline'
        
        for option in self.behavioral_options:
            option_name=option.lower().replace('-','').replace(' ','_')
            outfile = self.output_directory+'metamap_processed_'+file.split('/')[-1].split('.')[0]+'_'+ option_name+'.json'
            run_command = self.metamap_path+''' '''+self.metamap_default_options+''' '''+option+''' '''+file+''' '''+outfile
            print(run_command) 

            p = subprocess.Popen([run_command], shell=True)
            out, err = p.communicate()

            #move_command='mv '+file+' '+'/'.join(file.split('/')[:-1])+'/done/'+file.split('/')[-1]+'.done'
            #print(move_command)

            #p = subprocess.Popen([move_command], shell=True)
            #out, err = p.communicate()
