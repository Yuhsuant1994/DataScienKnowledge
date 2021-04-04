# my often used aws related python code

## sns
```python
message = "this is the email content"
finalmessage = f"""
                aws sns publish \
                --message '{message}' \
                --topic arn:aws:sns:eu-west-1:1234566778:team \
                --subject 'subject'
                """
os.system(finalmessage)
```
## secret key manager

## s3
from s3 to redshift
```python
import boto3
SCHEMA = 'table_schema'
BUCKETNAME = 'bucket'
IAM_ROLE = "role"
S3 = boto3.resource('s3')
BUCKET = S3.Bucket(BUCKETNAME)
S3_CLIENT = boto3.client('s3')


def fromS3_to_redshift(target_table, file_name):
    cur = connection_mdp.cursor()
    query_transfer = f"""
        copy {SCHEMA}.{target_table} --(optional {columns})
        FROM  's3://{BUCKETNAME}/folder1/{file_name}'
        iam_role 'arn:aws:iam::123456:role/{iam_role}' 
        DELIMITER ',' 
        IGNOREHEADER 1;
        """
    cur.execute(query_transfer)
    connection_mdp.commit()
    cur.close()
```
* file download
```python
BUCKET.download_file('folder/sendlog.csv',os.path.join(DATAPATH, 'sendlog.csv'))
```
* read file
```python
df_lead = pd.DataFrame()
for objects in BUCKET.objects.filter(Prefix='folder1/2021/01/28'):
    obj = S3_CLIENT.get_object(Bucket=BUCKETNAME, Key=objects.key)
    df_current_lead = pd.read_csv(io.BytesIO(obj['Body'].read()), dtype=str)
    df_lead = pd.concat([df_lead, df_current_lead], sort=False)
```