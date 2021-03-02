# 1. Global purpose of the project

Build a unittest for QA the data base tables quality and status to know if I can 
correctly run our projects based on those data. As Ill as the QA for projects result.

Then provide Dashboard for results and main table's KPI tracking. For internal tracking 
and external cross team communications.

PAIN POINT: Spent many times in debuging and finding the issue for the daily automation 
process. Many times the problem was reported from other team about the concern for our 
team data. 

IMPACT: **Reduce 80%** of the debug / communication and duplicated work.

TECHNOLOGY USED: Python, Unittest, Azure MSSQL, Redshift, AWS SNS, PoIrBI

# 2. Process and tech note

## 2.1 Main tables KPI log

Define some KPI to check the data quality, in order to compare the data with different 
sources daily extract the KPI data and store it. In order to create a tracking table,
as Ill as visualizing it in PoIrBI.

## 2.2 Data base data update status QA

Start performing after I have the log of the ETL scheduler is done. (else directly 
consider not updated yet and don't perform the test)

**Step 1: Extract table's daily log**

Latest data reference date, size per country. Potential problems:

* Some tables didn't have country separated: use 'GLOBAL' to count all
* Some tables didn't have date separated: empty not to extract
* As all table is using different column names

Solutions: define a table of metadata, then build a dynamic SQL for running the loop. Therefore, 
in the future if I add more table to do the QA I don't need to rewrite the code, I just need 
to add one row of metadata in the table. The code would extract the information directly.

Sample code:
```python
def meta_data_query(simple=True):
    # query join is the table who have other country format in the column
    query_simple = """
    SELECT  '{table_name}' as table_name,
            {country_col} as country_key,
            count(*) as count_size,
            {date_col} as latest_data_date,
            '{today}' as sys_update_date
    FROM {table_name}
    WHERE {country_col} not in {country_key}
          @sql_filter
    GROUP BY sales_org
    """
    query_join = """
    SELECT  '{table_name}' as table_name ,
            LPAD(country.country_key, 4, '0') as country_key,
            count_size,
            latest_data_date,
            '{today}' as sys_update_date
    FROM(
            SELECT {country_col},
                        count(*) as count_size,
                        {date_col} as latest_data_date
            FROM {table_name}
            GROUP BY {country_col}
        ) as base_table
    JOIN table_country_map as country
    {join_country_on}
    WHERE LPAD(country.country_key, 4, '0') not in {country_key}
          @sql_filter
    """
    if simple:
        return query_simple
    else:
        return query_join
```

**Step 2: unittest update status**

Double check if the the size and date has changed per country according to the update 
frequency. Then I check the quality of the ETL, compare the size today with the mean 
of last month and keep tracking the deviation to know what is the general threshold that 
I should raise a warning. 

Eventually store the unittest result. Use AWS SNS to notify the team if there's some potential 
issue. As Ill as build a dashboard in PoIr BI for the tracking and visualization.

unittest python sample code:
```python
class TestUpdateMethod(unittest.TestCase):
    def __init__(self, methodName, today_size, compare_size,
                 today_date, compare_date, table_name, country,
                 dev_mean):
        super(TestUpdateMethod,  self).__init__(methodName)
        self.table_name = table_name
        self.country = country
        self.today_size = today_size
        self.compare_size = compare_size
        self.today_date = today_date
        self.compare_date = compare_date
        self.dev_mean = dev_mean

    def test_size_change(self):
        self.assertTrue(self.today_size != 0)
        self.assertTrue(self.compare_size != 0)
        if ((self.today_size != 0) & (self.compare_size != 0)):
            self.assertTrue(self.today_size != self.compare_size,
                            f"data size for table: {self.table_name} country: {self.country} does not change")

    def test_size_change_range(self):
        self.assertTrue(abs(self.dev_mean) <= HEALTHY_THRESHOLD,
                        f"""abnormal data size change for table: {self.table_name} country: {self.country},
                        dev in means is {self.dev_mean},  bigger than our healthy threshold {HEALTHY_THRESHOLD}""")

    def test_date_change(self):
        self.assertTrue(self.today_date != self.compare_date,
                        'latest date for table: {self.table_name} country: {self.country} does not change')

```

## 2.3 Project result unittest

**Step 1: define metadata / rule engine table**

Define a table for metadata and rule engine then I just have to maintain the table, reduce 
efforts for modifying code and testing the code.

Define test case with different stakeholders what kind of test I need to perform, 
per request I can add the unique test per project. There are some general test such as 
require columns, if there's extra columns, mandatory columns cannot be empty, 
columns formats, check result size etc...

Then I store the result into a tables to track it and create a dashboard for the result. 