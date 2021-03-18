
*below info are the extract from multiple 
references sources, mainly serve as my own knowledge note*

[(my related projects)](https://github.com/Yuhsuant1994/DataScienKnowledge/blob/master/projects/customer_es_engine.md)
_______________________________
# Elasticsearch [(wikipedia)](https://en.wikipedia.org/wiki/Elasticsearch#:~:text=Elasticsearch%20is%20a%20search%20engine,and%20schema%2Dfree%20JSON%20documents.)


Flexible and powerful open source, distributed real-time search and analytics engine.
It is developed in **Java** based on **Lucene library** one of the most popular 
enterprise search engine followed by Apache Solr, also based on Lucene. (Lucene does not contain crawling and HTML parsing functionality.)

**Remarkable features:**

* Elasticsearch can be used to search all kinds of documents. It provides scalable search,
 has near real-time search, and supports [multitenancy](https://en.wikipedia.org/wiki/Multitenancy).
So we can use multiple different application on top. (setup multiple indices, it can be 
query independently or in combination)
* Elasticsearch uses Lucene and tries to make all its features available through the 
**JSON and Java API**.(supports real-time GET requests, which makes it suitable as a NoSQL 
datastore)
* Elasticsearch is scalable up to petabytes of structured and unstructured data.
* Support [Faceted search](https://en.wikipedia.org/wiki/Faceted_search) ans percolate search (Elasticsearch usually queries a set of documents, looking for relevance of each one to a specific search request. Percolate works in the opposite way, running your documents up against registered queries (percolators) for matches.)

**some functionalities:**

* Query: we can query, and multi match query on selected columns with implementation of fuzzyness as well
* Filter: We can set filters to make it match fater

# why is it fast?

The core of high speed is derived from parallel computing and inverted index.

## Four Nouns of elastic search
* **Cluster**: A single cluster consists of multiple nodes.
* **Node**: Simply put, Node means the number of Elasticsearch process. You could activate more than one Elasticsearch process, in this way, you created multiple nodes. However, we usually deploy different nodes on different machine. It will make our service more available.
* **Shard**s: An unbreakable entity in Elasticsearch. The actual data unit in disk.
* **Replicas**: data copied from shards. Setting replicas with multiple node could avoid data lost when machine malfunction and allow higher availability.

Shards are the containers of **inverted indices**, and we call the process from input 
text to [inverted index](https://en.wikipedia.org/wiki/Inverted_index#:~:text=The%20purpose%20of%20an%20inverted,itself%2C%20rather%20than%20its%20index.)
 (can be seen as transpose document matric-> a term document table, per token / term 
what is the id of the documents that contains it) as indexing. 
After indexing, elasticsearch will create several 
inverted indices tables which is the reason of searching so fast in elasticsearch.

# Reference

* [How Elasticsearch Search So Fast?](https://medium.com/analytics-vidhya/how-elasticsearch-search-so-fast-248630b70ba4#:~:text=The%20essence%20of%20Shard%3A%20the%20set%20of%20inverted%20indices,-To%20an%20elasticsearch&text=To%20elasticsearch%2C%20yet%2C%20index%20is,is%20the%20actual%20data%20entity.&text=After%20indexing%2C%20elasticsearch%20will%20create,searching%20so%20fast%20in%20elasticsearch.)
* [inverted index](https://www.youtube.com/watch?v=bFrO8piASKg)

## Open source Elasticsearch with Python
* [How to Use Elasticsearch Data Using Pandas in Python](https://kb.objectrocket.com/elasticsearch/how-to-use-elasticsearch-data-using-pandas-in-python-349)
* [How to Index Elasticsearch Documents Using the Python Client Library](https://kb.objectrocket.com/elasticsearch/how-to-index-elasticsearch-documents-using-the-python-client-library)
* [Elasticsearch tutorial for beginners using Python](https://medium.com/naukri-engineering/elasticsearch-tutorial-for-beginners-using-python-b9cb48edcedc)

## Open source Elasticsearch setup
* [Setup documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html), 
* [Viedo setup Elasticsearch Engine on linux](https://www.youtube.com/watch?v=63nS1Z-pIfI), 
* [Blog setup Elasticsearch Engine on linux](https://linuxize.com/post/how-to-install-elasticsearch-on-centos-7/)

## search engine basic knowlege
* [SEO For Beginners: Crawling, Indexing and Ranking](https://www.youtube.com/watch?v=xqvnBxu7960)
* [HOW SEARCH ENGINES WORK: CRAWLING, INDEXING, AND RANKING](https://moz.com/beginners-guide-to-seo/how-search-engines-operate)
    * Crawling: (discovering of the pages) Scour the Internet for content, looking over the code/content for each URL they find (can configure some pages be disable from google crawl)
    * Indexing: (storing of the discovered pages) Store and organize the content found during the crawling process. Once a page is in the index, it’s in the running to be displayed as a result to relevant queries.
    * Ranking: (rank the result) Provide the pieces of content that will best answer a searcher's query, which means that results are ordered by most relevant to least relevant.

## AWS elastic search

[documentation](https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/what-is-amazon-elasticsearch-service.html)

using the same open source, but faster easoer to deploy and fit into AWS environment. 
It also automatically detects and replaces failed Elasticsearch nodes, reducing the 
overhead associated with self-managed infrastructures.