# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 04:05:57 2015

@author: Mike
"""

quals_dict={'PhD':doc_frequency['phd'] +doc_frequency['dphil']+doc_frequency['doctorate'],'Experience':doc_frequency['experience'],
                    'Degree':doc_frequency['degree']+doc_frequency['bsc']+doc_frequency['bachelors'],'Masters':doc_frequency['masters']+doc_frequency['msc'],'A levels':doc_frequency['a level'],
                     'HND':doc_frequency['hnd']+doc_frequency['foundation degree']}

science_dict={'Biology':doc_frequency['biology']+doc_frequency['biologist']+doc_frequency['life sciences']+doc_frequency['biological'],
                      'Biochemistry':doc_frequency['biochemistry'],
                      'Chemistry':doc_frequency['chemistry']+doc_frequency['chemist']+doc_frequency['chemical'],
                      'Physics':doc_frequency['physics']+doc_frequency['physicist']+doc_frequency['physical'],
                      'Materials':doc_frequency['materials']+doc_frequency['composites']+doc_frequency['metal']+doc_frequency['metallurgical'],
                      'Nuclear':doc_frequency['nuclear']}
                      
sciJob_dict ={'Analyst':doc_frequency['analyst'],
                      'Laboratory':doc_frequency['laboratory'],
                      'Technician':doc_frequency['technician']})                    
instrument_dict={'Microscope':doc_frequency['microscopes']+doc_frequency['microscopy'],
                         'Spectrometer':doc_frequency['spectrometers']+doc_frequency['spectroscopy']}

prog_lang_dict = {'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                'Java':doc_frequency['java'], 'C++':doc_frequency['c++'],
                'Ruby':doc_frequency['ruby'],
                'Perl':doc_frequency['perl'], 'Matlab':doc_frequency['matlab'],
                'JavaScript':doc_frequency['javascript'], 'Scala': doc_frequency['scala'], 'GIS': doc_frequency['gis']}

analysis_tool_dict = {'Excel':doc_frequency['excel'],  'Tableau':doc_frequency['tableau'],
                    'D3.js':doc_frequency['d3.js'], 'SAS':doc_frequency['sas'],
                    'SPSS':doc_frequency['spss'], 'D3':doc_frequency['d3'],'Minitab':doc_frequency['minitab']}

hadoop_dict = {'Hadoop':doc_frequency['hadoop'], 'MapReduce':doc_frequency['mapreduce'],
            'Spark':doc_frequency['spark'], 'Pig':doc_frequency['pig'],
            'Hive':doc_frequency['hive'], 'Shark':doc_frequency['shark'],
            'Oozie':doc_frequency['oozie'], 'ZooKeeper':doc_frequency['zookeeper'],
            'Flume':doc_frequency['flume'], 'Mahout':doc_frequency['mahout']}

database_dict = {'SQL':doc_frequency['sql'], 'NoSQL':doc_frequency['nosql'],
                'HBase':doc_frequency['hbase'], 'Cassandra':doc_frequency['cassandra'],
                'MongoDB':doc_frequency['mongodb']}
                
ds_techniques_dict = {'Machine learning':doc_frequency['machine learning']+doc_frequency['statistical learning'],'Inference':doc_frequency['inference'],
                    'Regression':doc_frequency['regression'],'Visualisation':doc_frequency['visualisation'],
                    'Exploratory data analysis':doc_frequency['exploratory data analysis'],'Classification':doc_frequency['classification']+doc_frequency['tree'],
                    'Clusters':doc_frequency['cluster'],'Optimisation':doc_frequency['optimisation']+doc_frequency['optimization'],
                     'Text':doc_frequency['text'],'Data Mining':doc_frequency['data mining'],'Spatial':doc_frequency['gis']}

