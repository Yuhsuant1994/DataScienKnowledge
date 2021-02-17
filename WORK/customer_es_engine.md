# 1. Global purpose of the project

To identify the unknown leads from different platform form, social media... 
crosscheck with the database existing data to identify part of the unknown 
leads to known leads. Therefore some automation process can be set up immidiately.

Then create a data model for project performance dashboard creation.

PAIN POINT: unknown leads is always hard to track and to contact, identifing 
them could take up to one full day or even more for one employee to do 
the manual search.

IMPACT: Reduce work hour of one salesperson from **one day to 8s**. 
A **start point** for the company to start treating the “unknown leads.”

TECHNOLOGY USED: Python, Elastic Search, Redshift

# 2. Process and tech note

**Step 1: etl process**

weekly Downloading data and merging /cleaning the data

**Step 2: set up elastic search**

* remove old index (if not it would just append, depend on the needs) 
```
es = Elasticsearch(hosts=self.es_hosts)
es.indices.delete(self.es_index)
```
* Setup index 
    
    mapping properties:
    * columns as key not for searching `"col": {'type': 'keyword', "ignore_malformed": True}`
    * columns for searching `"last_name": {"type":"text", "analyzer": "autocomplete", "ignore_malformed": True, "search_analyzer": "standard"}` 

* Post Data

```python
def postData(self, es_instance):
    df_cleaned = pd.read_csv(self.ref_df_path, dtype=str)
    df_cleaned = df_cleaned[df_cleaned.sales_org == self.current_sales_org]

    # make sure there's no empty (used not found instead)
    for col in df_cleaned.columns:
        df_cleaned.loc[(df_cleaned[col] == ''), col] = 'notfound'
        df_cleaned[col].fillna('notfound', inplace=True)
    df_cleaned = df_cleaned.drop_duplicates().drop(columns='sales_org')
    len_df_cleaned = df_cleaned.shape[0]
    log.info(f'need to post {len_df_cleaned} rows of data')

    # append only partially ate once
    subsize = 30000
    start = 0
    end = subsize
    while start < len_df_cleaned:
        if end > len_df_cleaned:
            clean_sub_df = df_cleaned.iloc[start:]
        else:
            clean_sub_df = df_cleaned.iloc[start:end]
        header_list = list(df_cleaned.columns)
        index_name = self.es_index
        k = 1
        for index, row in clean_sub_df.iterrows():
            k = k + 1
            doc = {}
            for i in range(0, len(header_list)):
                doc[header_list[i]] = row[i]
            res = es_instance.index(index=index_name, body=doc)
        log.info(f'finish posting until {min(end,len_df_cleaned)} rows...')
        end = end + subsize
        start = start + subsize

```

* Function for search result (within multimatch)

    **fuzziness:** would help for fuzzy text.

    **multi_match type** [(doc)](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/query-dsl-multi-match-query.html), 

    * best_fields:  Finds documents which match any field (good case for product searching, 
    index can be tool key, tool name, tool type etc...)
    * most_fields: Finds documents which match any field and combines the _score from each field. 
    (this case is using most_fields)

    **fields:** this we can pass the fields we want to search on

Note for calling the process:
```python
from datetime import datetime
from config.log import *
from src import etl, es_cont
import argparse
from project_settings import *
import os
from elasticsearch import Elasticsearch, helpers
from elasticsearch import RequestsHttpConnection, helpers
import shutil


def execute(process, connection, country, data_download_path, ref_file_name,
            es_hosts, es_index, remove_billing, remove_hilti):
    if process == 'etl':
        data_object = etl.Data(connection, country, data_download_path,
                               ref_file_name, remove_billing, remove_hilti)
        data_object._download_data()
        data_object._get_merged_df()

    if process == 'es_setup':
        for current_country in list(country):
            log.info(f'starte setting up elastic search for contsct in {current_country}')
            es_cont.ContactElasticsearch(
                        current_country, es_hosts, es_index,
                        data_download_path, ref_file_name
                        )._setup_es()
            log.info(f'elastic search for {current_country} contact has been updated...')

    elif process == 'all':
        log.info('all process will be performed: etl, set_es')
        log.info('start etl process')
        data_object = etl.Data(connection, country, data_download_path,
                               ref_file_name, remove_billing, remove_hilti)
        data_object._download_data()
        data_object._get_merged_df()
        for current_country in list(country):
            log.info(f'starte setting up elastic search for contsct in {current_country}')
            es_cont.ContactElasticsearch(
                        current_country, es_hosts, es_index,
                        data_download_path, ref_file_name
                        )._setup_es()
            log.info(f'elastic search for {current_country} contact has been updated...')
        # remove files
        for folder in [output_path, data_download_path]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Elastic Search: contact info')
    parser.add_argument('--process', type=str, help='options: etl, set_es, all')
    args = vars(parser.parse_args())
    execute(args['process'], CONNECTION, COUNTRY, DOWNLOAD_PATH, FILE_NAME,
            ES_HOST, ES_INDEX, REMOVE_BILLING, REMOVE_HILTI)

```

**Step 3: Automated process search**

Daily run on the search when there's new identified leads