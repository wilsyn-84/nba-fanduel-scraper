import os
import boto3
import csv
import io 
import datetime
from NBA.Scrapper import NBAScapper

def test_handler(event, context):
    return("Success!")

def handler(event, context):

    bucket = os.environ.get('BUCKET_NAME')
    print(bucket)
    filename = "Daily_Downloads/wagers_{}.csv".format(
        datetime.date.today().strftime("%Y_%m_%d")
    )
    
    scrapper = NBAScapper()
    games = scrapper.download_today_games()

    print('Writing CSV')
    with io.StringIO() as csvfile:
        fieldnames = games[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in games:
            writer.writerow(row)
        print("Send to S3")
        client = boto3.client('s3')
        client.put_object(Body=csvfile.getvalue(), Bucket=bucket, Key=filename)

    return { 
        'message' : 'Success'
    }
#handler('','')