import boto3

def getAvailableRegions(aws_access_key_id, aws_secret_access_key):
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    regions = session.get_available_regions('polly')
    
    return regions
