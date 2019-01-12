import codecs
import bs4
import os
import mine_pdf
from pathlib import Path
import json

years = [2010, 2012, 2014, 2016, 2018]
years = [2018]
datalist = []
for year in years:
    LRECdir = 'data/LREC/LREC' + str(year) + '_Proceedings/'
    print('searching ' + str(LRECdir))
    #for html in os.listdir(LRECdir + 'summaries/')[:10]:
    for html in ['157.html']:
        
        data = {}
        
        # open file
        f=codecs.open(Path(str(LRECdir + 'summaries/') + str(html)), 'r')
        try:
            soup = bs4.BeautifulSoup(f, 'html.parser')
        except:
            print(html + ' not included')
        
        # get year
        data['year'] = year
        
        # get number
        data['number'] = html.strip('.html')
        
        # extract title
        title = soup.find('th', class_="second_summaries").string
        data['title'] = title

        # extract topics
        topics = []
        for a in bs4.BeautifulSoup(str(soup.find_all(class_='topics_summaries')), 'html.parser').find_all('a'):
            topics.append(a.string)
        data['topics'] = topics
        
        # extract authors
        authors = []
        for a in soup.find('td', text = 'Authors').nextSibling.nextSibling.find_all('a'):
            authors.append(a.string)
        data['authors'] = authors
        
        # extract abstracts
        data['abstract'] = soup.find('td', text = 'Abstract').nextSibling.nextSibling.string
        datalist.append(data)
        
        if year == 2018:
            pdfdir = LRECdir + 'pdf/' + str(data['number']) + '.pdf'
        else:
            pdfdir = LRECdir + 'pdf/' + str(data['number']) + '_Paper.pdf'
        
        text, keywords = mine_pdf.mine_pdf(pdfdir)


        if text is not None and keywords is not None:
            if keywords != '':
                keywords = keywords.lowercase().replace(':', ' ').strip('keywords').split(',')
            data['keywords'] = keywords
            data['fulltext'] = text

            print(text)

            with open(Path('data/LRECjson/' + str(year) + '_' + str(data['number']) + '.json'), 'w') as fp:
                json.dump(data, fp)
        



        
    

#alltopics = []
#for topiclist in topicsdict:
#    for topic in topiclist.split(' '):
#        alltopics.append(topic)
#alltopics = list(set(alltopics))