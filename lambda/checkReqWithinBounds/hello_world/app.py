import json
import boto3
from datetime import datetime as dt


# def get_file(fname):
#     logFileObject = list(filter(lambda f: f.key == fname, my_bucket.objects.all()))[0].get()
#     logFile = logFileObject['Body'].read().decode('utf-8')
#     return logFile

def check_within_bounds(start_idx, end_idx, search_time, timestamps):

    # Calculate mid for binary search

    ts_format = "%H-%M"  # TO CONFIG
    total = start_idx + end_idx
    mid_idx = total//2

    # Get the respective timestamps from string
    start_ts = dt.strptime(timestamps[start_idx], ts_format)
    mid_ts = dt.strptime(timestamps[mid_idx], ts_format)
    end_ts = dt.strptime(timestamps[end_idx], ts_format)

    search_ts = dt.strptime(search_time, ts_format)

    # if reach boundaries
    if start_idx >= end_idx:
        if search_ts == start_ts:
            return start_idx
        if search_ts == end_ts:
            return end_idx
        return "Not found"
    # If the time interval found, return the index
    # - this will be the index of the file to search
    if mid_ts == search_ts:
        return mid_idx
    # Else continue binary search
    elif search_ts < mid_ts:
        return check_within_bounds(start_idx, mid_idx-1, search_time, timestamps)
    else:
        return check_within_bounds(mid_idx+1, end_idx, search_time, timestamps)


def get_time_stamps(s3_bucket):
    return [file.key.split("_")[-1][:5] for file in s3_bucket.objects.all()]


def lambda_handler(event, context):
    """
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict
    """

    bucket = "cs441-hw2-data"  # TO CONFIG
    # This file will be read to get the logs
    s3 = boto3.resource('s3', aws_access_key_id="AKIAVA6CVFWCE57KTAWS",
                        aws_secret_access_key="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")
    s3_bucket = s3.Bucket(bucket)

    time_stamps = get_time_stamps(s3_bucket)
    print(check_within_bounds(0, len(time_stamps)-1, "12-12", time_stamps))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
