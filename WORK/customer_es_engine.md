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

* Query for search result (within multimatch)

    **fuzziness:** would help for fuzzy text.

    **multi_match type** [(doc)](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/query-dsl-multi-match-query.html), 

    * best_fields:  Finds documents which match any field (good case for product searching, 
    index can be tool key, tool name, tool type etc...)
    * most_fields: Finds documents which match any field and combines the _score from each field. 
    (this case is using most_fields)

    **fields:** this we can pass the fields we want to search on
```python
def _process_results(selfquery, max_results):
    result_df = pd.DataFrame()
    res = self.getContact(query)
    for item in range(min(max_resultslen(res['hits']['hits']))):
        each = res['hits']['hits'][item]
        current_df = pd.DataFrame([each['_source']])
        current_df['score'] = each['_score']
        result_df = pd.concat([result_df, current_df], sort=False)
    if result_df.shape[0] > 0:
        result_df = result_df.reset_index(drop=True)
        for col in result_df.columns:
            if isinstance(result_df[col][0]str):
                result_df[col] = result_df[col].str.replace('notfound')
    else:
        result_df = pd.DataFrame()
    return result_df.reset_index(drop=True)


def getContact(self, userQuery):
    index_name = self.es_index
    res = Elasticsearch(hosts=self.es_hosts).search(
            index=index_name,
            size=50,
            body={
                "query":
                    {
                        "multi_match":
                            {
                                "fields": self.search_fields,
                                "query": userQuery,
                                "type": "most_fields",
                                "fuzziness": 1.0
                                # "tie_breaker": 0.3
                                # "operator": "or"
                            }
                    },

                "highlight":
                    {
                        "type": "unified",
                        "order": "score",
                        "fields":
                            {
                                "cust_num": {},
                                "contact_num": {},
                                "person_num": {},
                                "first_name": {},
                                "last_name": {},
                                "cust_name": {},
                                "tax_number_1": {},
                                "mobile_num": {},
                                "tel_num": {},
                                "email": {}
                            }
                    }
                })
    return res

```
# 3. Calling the process:

``` python
def _process_results(selfquery, max_results):
    result_df = pd.DataFrame()
    res = self.getContact(query)
    for item in range(min(max_resultslen(res['hits']['hits']))):
        each = res['hits']['hits'][item]
        current_df = pd.DataFrame([each['_source']])
        current_df['score'] = each['_score']
        result_df = pd.concat([result_df, current_df], sort=False)
    if result_df.shape[0] > 0:
        result_df = result_df.reset_index(drop=True)
        for col in result_df.columns:
            if isinstance(result_df[col][0]str):
                result_df[col] = result_df[col].str.replace('notfound')
    else:
        result_df = pd.DataFrame()
    return result_df.reset_index(drop=True)


def getContact(self, userQuery):
    index_name = self.es_index
    res = Elasticsearch(hosts=self.es_hosts).search(
            index=index_name,
            size=50,
            body={
                "query":
                    {
                        "multi_match":
                            {
                                "fields": self.search_fields,
                                "query": userQuery,
                                "type": "most_fields",
                                "fuzziness": 1.0
                                # "tie_breaker": 0.3
                                # "operator": "or"
                            }
                    },

                "highlight":
                    {
                        "type": "unified",
                        "order": "score",
                        "fields":
                            {
                                "cust_num": {},
                                "contact_num": {},
                                "person_num": {},
                                "first_name": {},
                                "last_name": {},
                                "cust_name": {},
                                "tax_number_1": {},
                                "mobile_num": {},
                                "tel_num": {},
                                "email": {}
                            }
                    }
                })
    return res

```

**Step 3: Automated process search**

Daily run on the search when there's new identified leads