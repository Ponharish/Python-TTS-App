import boto3
import formatteddate

from datetime import datetime, timedelta

def fetchUsage(aws_access_key_id, aws_secret_access_key, region):
    cloudwatch = boto3.client(
        'cloudwatch',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        region_name = region
    )

    end_time = datetime.utcnow()
    start_time = datetime(end_time.year, end_time.month, 1) 

    response = cloudwatch.get_metric_statistics(
        Namespace = 'AWS/Polly',
        MetricName = 'RequestCharacters',
        Dimensions = [{'Name': 'Operation', 'Value': 'SynthesizeSpeech'}],
        StartTime = start_time,
        EndTime = end_time,
        Period = 300,  
        Statistics = ['Sum']
    )

    total_characters = int(sum(datapoint['Sum'] for datapoint in response['Datapoints']))

    return "Usage since "+ formatteddate.fetchFormattedDate(datetime(datetime.utcnow().year, datetime.utcnow().month, 1))+ ": "+ str(total_characters) + " Chars"

