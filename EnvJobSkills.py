
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 06:00:19 2015
@author: Mike
"""
from bs4 import BeautifulSoup # For HTML parsing
import urllib2 # Website connections
import re # Regular expressions
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
from nltk.stem.snowball import SnowballStemmer
import pandas as pd # For converting results to a dataframe and bar chart plots
# matplotlib inline

def text_cleaner(website):
    '''
    This function just cleans up the raw html so that I can look at it.
    Inputs: a URL to investigate
    Outputs: Cleaned text only
    '''
    try:
        site = urllib2.urlopen(website).read() # Connect to the job posting
    except: 
        return   # Need this in case the website isn't there anymore or some other weird connection problem 

    soup_obj = BeautifulSoup(site) # Get the html from the site

    for script in soup_obj(["script", "style"]):
        script.extract() # Remove these two elements from the BS4 object

    text = soup_obj.get_text() # Get the text from this
    lines = (line.strip() for line in text.splitlines()) # break into lines
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each

    def chunk_space(chunk):
        chunk_out = chunk + ' ' # Need to fix spacing issue
        return chunk_out  

    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') # Get rid of all blank lines and ends of line

    # Now clean out all of the unicode junk (this line works great!!!)

    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore') # Need this as some websites aren't formatted
    except:                                                            # in a way that this works, can occasionally throw
        return                                                         # an exception

    text = re.sub("[^a-zA-Z.+3]"," ", text)  # Now get rid of any terms that aren't words (include 3 for d3.js)
                                                # Also include + for C+
    text = text.lower().split()  # Go to lower case and split them apart
    stop_words = set(stopwords.words("english")) # Filter out any stop words
    text = [w for w in text if not w in stop_words]
    text = list(set(text)) # Last, just get the set of these. Ignore counts (we are just looking at whether a term existed
                            # or not on the website)
    return text
    
# sample = text_cleaner("http://uk.dice.com/?Mode=AdvertView&AdvertId=9670458&utm_source=Feed&utm_medium=Aggregator_RX&utm_campaign=Indeed_UK_jobs&rx_job=51720716&rx_source=Indeed&rx_campaign=Indeed15&rx_group=1191&rx_medium=cpc")

def skills_info(job="data+scientist",region = "UK"):
    '''
    This function will take a desired city/state and look for all new job postings
    on Indeed.com. It will crawl all of the job postings and keep track of how many
    use a preset list of typical data science skills. The final percentage for each skill
    is then displayed at the end of the collation. 
    Inputs: The location's city and state. These are optional. If no city/state is input, 
    the function will assume a national search (this can take a while!!!).
    Input the city/state as strings, such as skills_info('Chicago', 'IL').
    Use a two letter abbreviation for the state.
    Output: A bar chart showing the most commonly desired skills in the job market for 
    a data scientist. 
    '''
    # Make sure the city specified works properly if it has more than one word (such as San Francisco)
    if region is "UK":
        final_site_list = ['http://www.environmentjobs.co.uk/job_search/job_search_results.asp?o=0&lt=job&k=',job]#,
    else:
        final_site_list = ['http://www.environmentjobs.com/job_search/job_search_results.asp?o=0&lt=job&k=',job]

    final_site = ''.join(final_site_list) # Merge the html address together into one string
    #return final_site
    base_urls = ['http://www.environmentjobs.co.uk/','http://www.environmentjobs.com/']

    try:
        html = urllib2.urlopen(final_site).read() # Open up the front page of our search first
    except:
        'That region combination did not have any jobs. Exiting . . .' # In case the city is invalid
        return
    
    jobUrls=[]
    nJobs =0
    nPages=1

    while True:
        urlStem=re.findall('(http\S+?o=)',final_site)
        #print urlStem
        urlEnd=re.findall('&lt\S+',final_site)
        #print urlEnd
        urlNextpage=urlStem[0]+str(15*(nPages-1))+urlEnd[0]
        html = urllib2.urlopen(urlNextpage).read()
        soup = BeautifulSoup(html)
        jobs = soup.find_all("a","search-jobtitle")
        for jobUrl in jobs:
            nextUrl = str(re.findall('href="(\S+=[0-9]+)',str(jobUrl)))[2:-2]
            #print nextUrl
            jobUrls.append(nextUrl)
        text = soup.get_text()
        pages=re.findall("NEXT PAGE",text)
        if len(pages)>0:
            nPages+=1           
        else:
            break
     
    print "Found: "+ str(len(jobUrls)) +" jobs on "+str(nPages)+" pages"
    #print jobUrls    
    #return

    job_descriptions = [] # Store all our descriptions in this list

    for j in xrange(len(jobUrls)):
        print 'Getting job', j+1
        #print jobUrls[j]
        baseURLIncluded=False
        for url in base_urls:
            if url in jobUrls[j]:
                baseURLIncluded=True
        
        if baseURLIncluded == False:
            jobUrls[j] = base_urls[0]+str(jobUrls[j])
        #print jobUrls[j]
        final_description = text_cleaner(jobUrls[j])
        #print final_description
        if final_description: # So that we only append when the website was accessed correctly
            job_descriptions.append(final_description)
        sleep(1)
            

    print 'Done with collecting the job postings!'    
    print 'There were', len(job_descriptions), 'jobs successfully found.'
   #print job_descriptions[:]

    doc_frequency = Counter() # This will create a full counter of our terms. 
    [doc_frequency.update(item) for item in job_descriptions] # List comp

    # Now we can just look at our final dict list inside doc_frequency

    # Obtain our key terms and store them in a dict. These are the key data science skills we are looking for

    quals_dict=Counter({'PhD':doc_frequency['phd'] +doc_frequency['dphil']+doc_frequency['doctorate'],'Experience':doc_frequency['experience'],
                        'Degree':doc_frequency['degree']+doc_frequency['graduate']+doc_frequency['bsc']+doc_frequency['bachelors'],'Masters':doc_frequency['masters']+doc_frequency['msc']+doc_frequency['postgraduate'],'A levels':doc_frequency['a level'],
                         'HND':doc_frequency['hnd']+doc_frequency['foundation degree']})
    
    science_dict=Counter({'Biology':doc_frequency['biology']+doc_frequency['biologist']+doc_frequency['life sciences']+doc_frequency['biological'],
                          'Biochemistry':doc_frequency['biochemistry'],
                          'Chemistry':doc_frequency['chemistry']+doc_frequency['chemist']+doc_frequency['chemical'],
                          'Physics':doc_frequency['physics']+doc_frequency['physicist']+doc_frequency['physical'],
                          'Materials':doc_frequency['materials']+doc_frequency['composites']+doc_frequency['metal']+doc_frequency['metallurgical'],
                          'Nuclear':doc_frequency['nuclear']})
                          
    sciJob_dict =Counter({'Analyst':doc_frequency['analyst'],
                          'Laboratory':doc_frequency['laboratory'],
                          'Technician':doc_frequency['technician']})                    
    instrument_dict=Counter({'Microscope':doc_frequency['microscopes']+doc_frequency['microscopy'],
                             'Spectrometer':doc_frequency['spectrometers']+doc_frequency['spectroscopy']})

    env_dict=Counter({'Marine':doc_frequency['marine'],'Wildlife':doc_frequency['wildlife'],
                             'Ecology':doc_frequency['ecology']+doc_frequency['ecologist']})   
    
    
    prog_lang_dict = Counter({'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                    'Java':doc_frequency['java'], 'C++':doc_frequency['c++'],
                    'Ruby':doc_frequency['ruby'],
                    'Perl':doc_frequency['perl'], 'Matlab':doc_frequency['matlab'],
                    'JavaScript':doc_frequency['javascript'], 'Scala': doc_frequency['scala'], 'GIS': doc_frequency['gis']})

    analysis_tool_dict = Counter({'Excel':doc_frequency['excel'],  'Tableau':doc_frequency['tableau'],
                        'D3.js':doc_frequency['d3.js'], 'SAS':doc_frequency['sas'],
                        'SPSS':doc_frequency['spss'], 'D3':doc_frequency['d3'],'Minitab':doc_frequency['minitab']})  

    hadoop_dict = Counter({'Hadoop':doc_frequency['hadoop'], 'MapReduce':doc_frequency['mapreduce'],
                'Spark':doc_frequency['spark'], 'Pig':doc_frequency['pig'],
                'Hive':doc_frequency['hive'], 'Shark':doc_frequency['shark'],
                'Oozie':doc_frequency['oozie'], 'ZooKeeper':doc_frequency['zookeeper'],
                'Flume':doc_frequency['flume'], 'Mahout':doc_frequency['mahout']})

    database_dict = Counter({'SQL':doc_frequency['sql'], 'NoSQL':doc_frequency['nosql'],
                    'HBase':doc_frequency['hbase'], 'Cassandra':doc_frequency['cassandra'],
                    'MongoDB':doc_frequency['mongodb']})
                    
    ds_techniques_dict = Counter({'Machine learning':doc_frequency['machine learning']+doc_frequency['statistical learning'],'Inference':doc_frequency['inference'],
                        'Regression':doc_frequency['regression'],'Visualisation':doc_frequency['visualisation'],
                        'Exploratory data analysis':doc_frequency['exploratory data analysis'],'Classification':doc_frequency['classification']+doc_frequency['tree'],
                        'Clusters':doc_frequency['cluster'],'Optimisation':doc_frequency['optimisation']+doc_frequency['optimization'],
                         'Text':doc_frequency['text'],'Data Mining':doc_frequency['data mining'],'Spatial':doc_frequency['gis']})


   #overall_total_attributes = prog_lang_dict + analysis_tool_dict + hadoop_dict + database_dict # Combine our Counter objects
   #overall_total_attributes = quals_dict
    overall_total_attributes = env_dict
    #overall_total_attributes = science_dict+instrument_dict+sciJob_dict
    #overall_total_attributes = ds_techniques_dict

    final_frame = pd.DataFrame(overall_total_attributes.items(), columns = ['Term', 'NumPostings']) # Convert these terms to a 
                                                                                                # dataframe 

    # Change the values to reflect a percentage of the postings 

    final_frame.NumPostings = (final_frame.NumPostings)*100/len(job_descriptions) # Gives percentage of job postings 
                                                                                    #  having that term 

    # Sort the data for plotting purposes

    final_frame.sort(columns = 'NumPostings', ascending = False, inplace = True)

    # Get it ready for a bar plot

    final_plot = final_frame.plot(x = 'Term', kind = 'bar', legend = None, 
                            title = 'Percentage of Job Ads with a Key Skill')# + city_title)

    final_plot.set_ylabel('Percentage Appearing in Job Ads')
    fig = final_plot.get_figure() # Have to convert the pandas plot object to a matplotlib object


    return fig, final_frame # End of the function

a=skills_info("marine")