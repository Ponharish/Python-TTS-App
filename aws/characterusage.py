import boto3
from util import formatteddate

from datetime import datetime, timedelta

def fetchUsage(aws_access_key_id, aws_secret_access_key, region):
    prevDay = datetime.utcnow() - timedelta(days=1)
    endTime1 = datetime(prevDay.year, prevDay.month, prevDay.day, 23, 59, 59)
    startTime1 = datetime(endTime1.year, endTime1.month, 1)

    today = datetime.utcnow()
    startTime2 = datetime(today.year, today.month, today.day, 0, 0, 0)
    endTime2 = datetime.utcnow()

    cloudwatch1 = boto3.client(
        'cloudwatch',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        region_name = region
    )

    response1 = cloudwatch1.get_metric_statistics(
        Namespace = 'AWS/Polly',
        MetricName = 'RequestCharacters',
        Dimensions = [{'Name': 'Operation', 'Value': 'SynthesizeSpeech'}],
        StartTime = startTime1,
        EndTime = endTime1,
        Period = 86400,  
        Statistics = ['Sum']
    )

    cloudwatch2 = boto3.client(
        'cloudwatch',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        region_name = region
    )

    response2 = cloudwatch2.get_metric_statistics(
        Namespace = 'AWS/Polly',
        MetricName = 'RequestCharacters',
        Dimensions = [{'Name': 'Operation', 'Value': 'SynthesizeSpeech'}],
        StartTime = startTime2,
        EndTime = endTime2,
        Period = 120,  
        Statistics = ['Sum']
    )

    totalCharacters = 0
    totalCharacters += int(sum(datapoint['Sum'] for datapoint in response1['Datapoints']))
    totalCharacters += int(sum(datapoint['Sum'] for datapoint in response2['Datapoints']))
    
    return "Usage since "+ formatteddate.fetchFormattedDate(datetime(datetime.utcnow().year, datetime.utcnow().month, 1))+ ": "+ str(totalCharacters) + " Chars"
