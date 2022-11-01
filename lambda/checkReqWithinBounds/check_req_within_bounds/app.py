import json
import boto3
from datetime import datetime as dt
from datetime import timedelta

from HelperUtils.create_logger import create_logger

logger = create_logger(__name__)
ts_format = "%H-%M"


def get_log_file_idx(start_idx, end_idx, search_time, timestamps):
    """
    for the given search time & timestamps,
    returns the index of the search time in timestamps
    """

    # Calculate mid for binary search
    total = start_idx + end_idx
    mid_idx = total//2

    # Get the respective timestamps from string
    start_ts = dt.strptime(timestamps[start_idx], ts_format)
    mid_ts = dt.strptime(timestamps[mid_idx], ts_format)
    end_ts = dt.strptime(timestamps[end_idx], ts_format)

    search_ts = dt.strptime(search_time, ts_format)

    # if reach boundaries
    logger.warn(f"search_time: {search_time} not in timestamps")
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
        return get_log_file_idx(start_idx, mid_idx-1, search_time, timestamps)
    else:
        return get_log_file_idx(mid_idx+1, end_idx, search_time, timestamps)


def get_time_stamps(s3_bucket):
    """
    extracts the time stamps in the log files on given S3 bucket
    """
    try:
        files = s3_bucket.objects.all()
    except Exception as e:
        logger.exception("Issue with s3 bucket")

    return [file.key.split(".")[1] for file in files]


def get_end_time(start_time, time_delta):
    """
    calculates the upper bound of the requested window
    """
    try:
        start_time = dt.strptime(start_time, ts_format)
    except Exception as e:
        logger.exception("Incorrect string format for timestamp")

    return (start_time + timedelta(minutes=int(time_delta))).strftime(ts_format)


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

    try:
        s3 = boto3.resource('s3', aws_access_key_id="AKIAVA6CVFWCE57KTAWS",
                            aws_secret_access_key="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")
        s3_bucket = s3.Bucket(bucket)
    except Exception as e:
        logger.exception("Issue with accessing S3")

    payload = json.loads(event['body'])
    start_time = payload["start_time"]
    time_delta = payload["time_delta"]

    time_stamps = get_time_stamps(s3_bucket)
    log_file_start_idx = get_log_file_idx(0, len(time_stamps)-1,
                                          start_time, time_stamps)

    end_time = get_end_time(start_time, time_delta)
    log_file_end_idx = get_log_file_idx(0, len(time_stamps)-1,
                                        end_time, time_stamps)

    if log_file_start_idx == "Not found" or log_file_end_idx == "Not found":
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Did not found log files for the given time range"
            }),
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Found log files for the given time range",
            "log_files_start_idx": f"{log_file_start_idx}",
            "log_files_end_idx": f"{log_file_end_idx}",
        }),
    }
