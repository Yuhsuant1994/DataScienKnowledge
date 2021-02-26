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

<details>
  <summary>Click to expand!</summary>

```python
def get_new_email_events():
    cnxn = open_cnxn_mdp()
    START_TIME = str(int(pd.read_sql("""
        SELECT max(event_time)
        FROM email_events
        WHERE source='Hubspot'
        """, cnxn)['max'][0]) + 1)
    cnxn.close()
    df_events = pd.DataFrame()
    failed = pd.DataFrame(columns=['Failed index', 'cid', 'first'])
    URL = f'https://api.hubapi.com/email/public/v1/events?hapikey={hapikey}'\
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