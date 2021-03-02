# 1. Global purpose of the project

To build a model for both email sources, Salesforce generate flat files and Hubspot API.
 In order to have a data model for email related project and performance tracking etc... 

PAIN POINT: Before this project we can only use Hubspot platform to download email event 
info per email, we don't have the data stored in our database. While we added another system 
"Salesforce" it become more problematique.

IMPACT: **Avoid 100% manual data load work**. Allow to start email related projects.

TECHNOLOGY USED: Python, RESTful API, Redshift

# 2. Process and tech note

**Step 1: get event from hotspot**

Hubspot we are extracting data with RESTful API

<details>
  <summary>Click to see the exemple code...</summary>

```python
from src.credentials import APIKEY
from src.connection import open_cnxn_dl, open_cnxn_mdp
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pandas.io.json import json_normalize
import requests

def get_new_emails():
    cnxn = open_cnxn_mdp()
    START_TIME = str(int(pd.read_sql("""
        SELECT max(event_time)
        FROM emails
        WHERE source='Hubspot'
        """, cnxn)['max'][0]) + 1)
    cnxn.close()
    df_events = pd.DataFrame()
    failed = pd.DataFrame(columns=['Failed index', 'cid', 'first'])
    URL = f'https://api.hubapi.com/email/public/v1/events?APIKEY={APIKEY}'\
        + f'&startTimestamp={START_TIME}&limit=1000'
    nb_try = 1
    NEED_COL_FULL = ['appName', 'emailCampaignId', 'recipient',
                     'type', 'sentBy.created', 'created']
    try:
        response = requests.get(URL, timeout=None).json()
        current_campaign = json_normalize(response['events'])
        col_list = list(current_campaign.columns)
        need_columns = list((set(NEED_COL_FULL)).intersection(set(col_list)))
        current_campaign = current_campaign[need_columns]
        df_events = pd.concat([df_events, current_campaign],
                              sort=False, ignore_index=True)
        hasMore = response['hasMore']
        nb_try = nb_try + 1
        current_rows = current_campaign.shape[0]
        try:
            while hasMore:
                offset = response['offset']
                offset_URL = URL + '&offset=' + str(offset)
                response = requests.get(offset_URL, timeout=None).json()
                current_campaign = json_normalize(response['events'])
                col_list = list(current_campaign.columns)
                need_columns = list((set(NEED_COL_FULL))
                                    .intersection(set(col_list)))
                current_campaign = current_campaign[need_columns]
                df_events = pd.concat([df_events, current_campaign],
                                      sort=False, ignore_index=True)
                hasMore = response['hasMore']
                nb_try = nb_try + 1
                current_rows = current_campaign.shape[0]
        except:
            failed = failed.append({
                'Failed index': nb_try,
                'cid': campaign_id,
                'first': 'loop'
                }, ignore_index=True)
            nb_try = nb_try + 1
    except:
        failed = failed.append({
            'Failed index': nb_try,
            'cid': campaign_id,
            'first': 'first'
            }, ignore_index=True)
        nb_try = nb_try + 1
    if df_events.shape[0] > 0:
        df_events['sent_date'] = convert_time(df_events, 'sentBy.created')
        df_events['event_date'] = convert_time(df_events, 'created')
        df_events['emailCampaignId'] = df_events['emailCampaignId'].fillna(0)\
                                            .astype(int).astype(str)\
                                            .str.pad(width=8, side='left',
                                                     fillchar='0')
        df_events = df_events.drop_duplicates(keep='first')
    return df_events

    def convert_time(df, col):
        return  pd.to_datetime(df['col']/1000, unit='s')\
                .dt.tz_localize('Europe/London')\
                .dt.tz_convert('Europe/Paris')\
                .dt.strftime("%Y%m%d")

```

</details>

**Step 2: get event from SalesForce**

SalesForce we have the daily extract send to S3, we would then process that zip file.
<details>
  <summary>Click to see the exemple code...</summary>

```python
from auto_etl import functions, connections
import pandas as pd
import io
import zipfile


def get_mc_events_contact():
    max_time_query = f"""
    SELECT max(event_time)
    FROM {SCHEMA}.emails
    WHERE appname = 'SF'
    """
    MAX_TIME = pd.read_sql(max_time_query, CONNECTION)
    MAX_TIME = int(MAX_TIME['max'][0])

    events = pd.DataFrame()
    OBJ = INPUT_BUCKET.Object(LATEST_FILE)
    with io.BytesIO(OBJ.get()["Body"].read()) as tf:
        tf.seek(0)
        with zipfile.ZipFile(tf, mode='r') as zipf:
            for subfile in zipf.namelist():
                if subfile not in ['Complaints.csv', 'Conversions.csv']:
                    df_current = pd.read_csv(zipf.open(subfile),
                                             encoding=file_encoding,
                                             dtype=str)
                    if df_current.shape[0] > 0:
                        df_current['event_time'] = (pd.to_datetime(df_current['EventDate'])
                                                    .astype(int)/1000000)\
                                                    .astype(int)
                        eventtype = df_current.EventType.unique()[0]
                        events = pd.concat([events, df_current], sort=False)
    events = events[events.event_time > MAX_TIME].astype(str)
    if events.shape[0] > 0:
        events.to_csv(os.path.join(DATAPATH, 'events_raw.csv'), index=False)
        INCREMENT_PATH = f'email_sensitivity/{TODAY}/'
        OUTPUT_BUCKET.upload_file(os.path.join(DATAPATH, 'events_raw.csv'),
                                  INCREMENT_PATH + f'events_raw_{TODAY}.csv')
        events['events_key'] = ''
        for col in ['SendID', 'ListID', 'BatchID', 'SubscriberID']:
            events['events_key'] = events['events_key'] + events[col]
        events_key = tuple(events.events_key)
        if len(events_key) == 1:
            events_key = str(events_key).replace(',', '')
        # get related sendlog
        query_sendlog = f"""
            SELECT distinct jobid +'_' +listid +'_' +
                            batchid +'_' +subid as events_key,
            EXTRACT('epoch' FROM (CAST(senddate as timestamp))) as sent_time,
            REPLACE(CAST(CAST(senddate as date) as varchar)
                    ,'-','') as sent_date, *
            FROM {SCHEMA}.emails_sendlog
            WHERE events_key in {events_key}
        """
        email_info = pd.read_sql(query_sendlog, CONNECTION)
        events = events.merge(email_info, how='left', on='events_key')
        events.loc[events.sent_time > 0, 'sent_time'] = (events.loc[events.sent_time > 0, 'sent_time']*1000)\
                                                        .astype(int).astype(str)
        events['event_time'] = events['event_time'].astype(str)
        events['email_id'] = events['SendID'].astype(str)
        events['event_type'] = events['EventType'].str.upper()
        events['event_date'] = pd.to_datetime(events['EventDate'])\
                               .dt.strftime("%Y%m%d")
        events['email_name'] = events['emailcode']
        events['appname'] = 'Marketing Cloud'
        events['sys_update_date'] = TODAY
        events['Alias'] = events['Alias'].astype(str)\
                                         .fillna('')\
                                         .str.replace('nan', '')
        events = events.rename(columns={
                                        'sapcontactid': 'contact_num',
                                        'market': 'sales_org',
                                        'EmailAddress': 'recipient',
                                        'Alias': 'alias'}).fillna('')
        events = add_email_cate(add_email_campagin(events))
        mc_event = events[EVENT_COL]
    else:
        mc_event = pd.DataFrame(columns=EVENT_COL)
    return mc_event

```

</details>

**Step 3: merge two files result to our database**

However this is a processed result, we still have to create 
another table or save the file for the raw data, just incase the process has problems

