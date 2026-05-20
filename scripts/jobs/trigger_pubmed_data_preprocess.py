from src.data_pipeline.pubmed.classes.process_pubmed_raw_xml import process_pubmed_raw_xml
import glob
import subprocess

process_pubmed_raw_xml_obj=process_pubmed_raw_xml()

files_list=glob.glob('/home/rgoli/MetaMap-src/data/pubmed_data/raw_data/*.xml')
print(files_list)
processed_files=[]
for file in files_list:
    try:
        output_file = process_pubmed_raw_xml_obj.convert_pubmed_out_to_xml(file)
        processed_files.append(output_file)
        if output_file:
            print("Output file wrote in: "+str(output_file))
            file_name_done=file.split('/')[-1]+'.done'
            file_path = '/'.join(file.split('/')[:-1])+'/done/'
            move_command='mv '+ file + ' '+file_path+file_name_done
            p = subprocess.Popen([move_command], shell=True)
            out, err = p.communicate()
    except Exception as e:
        print(str(e))



