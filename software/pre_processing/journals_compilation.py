#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import operator
import numpy as np
import pandas as pd
import unicodedata

import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

from IPython.core.debugger import set_trace


# In[ ]:


def by_line(N):
    byline = []
    for i in range(N):
        if(N == 1):
            byline.append( 0 )
        else:
            ret = byline.append( ( i/(N-1) ) )
    return byline

def prevalence(text, word):
    import re
    return sum(1 for _ in re.finditer(r'\b%s\S' % re.escape(word), text))

def countSurname(authors):
    r = max(dict([v, prevalence(authors, v)] 
         for v in authors.split("; ")).items(), key=operator.itemgetter(1))
    
    if r[1] > 1:
        return r

def contrib(author_name, authors_new, authors):
    ret = 0
    list = re.compile('|'.join(authors_new.split('; ')), re.UNICODE)
    try:
        for a in authors.split("; "):
            try:
                if re.findall(list, authors):
                    if(re.findall(a.strip(" "), author_name)):
                        if(len(authors.split("; ")) > 0):
                            ret = 1/len(authors.split("; "))
            except:
                ret = 0
    except:
        ret = 0
        
    return ret


# In[ ]:


df = pd.read_excel(file, encoding='utf-8')


# In[ ]:


authors_list = []
count = 0
columns = [
    'eid', 'doi', 'title', 'year', 'volume', 'issue', 'page_count', 'reader_count', 'export_saves_count', 'cited_by_count', 'clinical_cited_by_count',
    'all_blog_count', 'news_count', 'reference_count', 'comment_count', 'qa_site_mentions_count', 'facebook_count', 'tweet_count', 'abstract_views_count', 
    'full_text_views_count', 'link_click_count', 'link_outs_count', 'downloads_count',
    
    'author_in_article', 'authors', 'authors_new', 'authors_id', 'author_id', 'author_name', 'author_byline', 'byline', 'posicao',

    'contrib_conception_and_design', 
    'contrib_analysis_and_interpretation_of_the_data', 
    'contrib_drafting_of_the_article', 
    'contrib_critical_revision_for_important_intellectual_content', 
    'contrib_final_approval_of_the_article', 
    'contrib_statistical_expertise', 
    'contrib_obtaining_of_funding', 
    'contrib_administrative_technical_or_logistic_support', 
    'contrib_collection_and_assembly_of_data', 
    'contrib_provision_of_study_materials_or_patients',
    'c1',
    'c2',
    'c3',
    'c4',
    'c5',
    'c6',
    'c7',
    'c8',
    'c9',
    'c10',
    
    'ac1', 'ac2', 'ac3', 'ac4', 'ac5', 'ac6', 'ac7', 'ac8', 'ac9', 'ac10', 'flag'
]

for index, row in df.iterrows():
    ids = row['authors_id'].split('; ')
    authors = row['authors'].split('; ')

    try:
        for linha in range(len(ids)):
            authors_list.append([
                row['eid'],
                row['doi'],
                row['title'],
                row['year'],
                row['volume'],
                row['issue'],
                row['page_count'],
                row['reader_count'],
                row['export_saves_count'],
                row['cited_by_count'],
                row['clinical_cited_by_count'],
                row['all_blog_count'],
                row['news_count'],
                row['reference_count'],
                row['comment_count'],
                row['qa_site_mentions_count'],
                row['facebook_count'],
                row['tweet_count'],
                row['abstract_views_count'],
                row['full_text_views_count'],
                row['link_click_count'],
                row['link_outs_count'],
                row['downloads_count'],
                row['authors_in_article'],
                row['authors'],
                row['authors_new'],
                row['authors_id'],

                str(''.join(ids[count].split(' '))), # author_id            

                ' '.join(autores[count].split(' ')), # author_name

                str((by_line(len(ids))[count])).replace(',', '.'), # author_byline

                str((by_line(len(ids)))).replace('.', '.').strip('[]'), #byline

                count+1, # author_position

                row['contrib_conception_and_design'],
                row['contrib_analysis_and_interpretation_of_the_data'], 
                row['contrib_drafting_of_the_article'], 
                row['contrib_critical_revision_for_important_intellectual_content'], 
                row['contrib_final_approval_of_the_article'], 
                row['contrib_statistical_expertise'], 
                row['contrib_obtaining_of_funding'], 
                row['contrib_administrative_technical_or_logistic_support'], 
                row['contrib_collection_and_assembly_of_data'], 
                row['contrib_provision_of_study_materials_or_patients'],

                row['c1'],
                row['c2'],
                row['c3'],
                row['c4'],
                row['c5'],
                row['c6'],
                row['c7'],
                row['c8'],
                row['c9'],
                row['c10'],

                # To other journal, input contributions matrix
                contrib(' '.join(authors[count].split(';')), row['authors_new'], row['c1']),  # contrib_study_concept_and_design
                contrib(' '.join(authors[count].split(';')), row['authors_new'], row['c2']),  # contrib_critical_revision
                contrib(' '.join(authors[count].split(';')), row['authors_new'], row['c3']),  # contrib_drafting_manuscript
                contrib(' '.join(authors[count].split(';')), row['authors_new'], row['c4']),  # contrib_statistical_analysis
                contrib(' '.join(authors[count].split(';')), row['authors_new'], row['c5']),  # contrib_study_supervision
                contrib(' '.join(authors[count].split(';')), row['authors_new'], row['c6']),  # contrib_administrative_support
                contrib(' '.join(authors[count].split(';')), row['authors_new'], row['c7']),  # contrib_obtained_funding
                contrib(' '.join(authors[count].split(';')), row['authors_new'], row['c8']),  # contrib_acquisition_analysis_interpretation_data
                contrib(' '.join(authors[count].split(';')), row['authors_new'], row['c9']),  # contrib_analysis_interpretation_data
                contrib(' '.join(authors[count].split(';')), row['authors_new'], row['c10']), # contrib_acquisition_data
                
                countSurname(row['authors_new'])
            ])
            count += 1                         
        count = 0
    except:
        print('Err', ' '.join(authors[count].split(' ')), row['authors_new'])
        
df1 = pd.DataFrame(data=authors_list, columns=columns)


# In[ ]:


df1.to_excel(file_out, header=True, index=False, encoding='utf-8')
df_byline = pd.read_excel(file', encoding='utf-8')
df_autores = pd.read_excel(file_authors, encoding='utf-8')
result = pd.merge(df_byline, df_autores, on='author_id', how='inner')
result.to_excel(file_final, header=True, index=False, encoding='utf-8')

