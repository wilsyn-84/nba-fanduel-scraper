import os
import boto3
import csv
import gzip
import io 
import datetime
import json
from src.scraper import Scaper

sport_event_configs = {
    "nba": {"games": {"code": "63747.3", "details": True}, },
    "mlb": {"games": {"code": "60826.3", "details": True}, },
    "golf": {
        "winner": {"code": "68160.3", "details": False},
        "top5": {"code": "67760.3", "details": False},
        "top10": {"code": "67761.3", "details": False},
        "top20": {"code": "67762.3", "details": False},
        "roundLeader": {"code": "68199.3", "details": False},
        "matchBets": {"code": "53176.3", "details": False},
        "groupBetting": {"code": "67753.3", "details": False},
    }
}

def scraper_handler(event,context):
    lambda_client = boto3.client('lambda')
    for key in sport_event_configs:
        print(key)
        lambda_client.invoke(
            FunctionName=os.environ.get('SCRAPER_FN'),
            InvocationType="Event",
            Payload=json.dumps({
                'sport': key,
                'sport_configs': sport_event_configs[key]
            })
        )
    return {
        'message': 'Success'
    }
#key = 'nba'
#event = {"sport":key, "sport_configs": sport_event_configs[key]}
#os.environ['BUCKET_NAME'] = 'scraper-dev-269350797537'
def scraper(event, context):
    sport = event['sport']
    sport_configs = event['sport_configs']
    bucket = os.environ.get('BUCKET_NAME')
    
    scraper = Scaper(sport, sport_configs)
    data = scraper.download_data()
    files = {
        'selections': {"file": "{}/{}/selections/selections_{}.csv.gz", "type": "csv"},
        'events_response': {"file": "{}/{}/events/events_{}.json.gz", "type": "json"},
        'event_details_response': {"file": "{}/{}/event_details/event_details_{}.json.gz", "type": "json"},
    }
    for key in data:
        filename = files[key]['file'].format(
            sport,
            datetime.date.today().strftime("%Y_%m_%d"),
            datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")
        )
        writeDataToS3(data[key], bucket, filename, files[key]['type'])

    return { 
        'message': 'Success'
    }
#data = data[key]
#filename = files[key]['file']
def writeDataToS3(data, bucket, filename, filetype):
    file = None
    if filetype.lower() == 'csv':
        file = write_csv(data)
    elif filetype.lower() == 'json':
        file = write_json(data)

    if file:
        print("Send to S3")
        client = boto3.client('s3')
        client.put_object(Body=file, Bucket=bucket, Key=filename)
'''
def write_csv(data):
    print('Writing CSV')
    inmem = io.StringIO()
    fieldnames = data[0].keys()
    csv_writer = csv.DictWriter(inmem,fieldnames=fieldnames)
    csv_writer.writeheader()
    for row in data:
        csv_writer.writerow(row)
    return inmem.getvalue()
'''

def write_csv(data):
    inmem = io.BytesIO()
    with gzip.GzipFile(fileobj=inmem, mode='w') as gz:
        buff = io.StringIO()
        fieldnames = data[0].keys()
        csv_writer = csv.DictWriter(buff,fieldnames=fieldnames)
        csv_writer.writeheader()
        for row in data:
            csv_writer.writerow(row)
        print("Writing data to gzipped file.")
        gz.write(buff.getvalue().encode())
        print("Data written")
        gz.close()
        inmem.seek(0)
    return inmem


def write_json(data, default=None, encoding='utf-8'):
    ''' upload python dict into s3 bucket with gzip archive '''
    inmem = io.BytesIO()
    with gzip.GzipFile(fileobj=inmem, mode='wb') as fh:
        with io.TextIOWrapper(fh, encoding=encoding) as wrapper:
            wrapper.write(json.dumps(data, ensure_ascii=False, default=default))
    inmem.seek(0)
    return inmem


#handler('','')
"""date > type > sport > csv?"""