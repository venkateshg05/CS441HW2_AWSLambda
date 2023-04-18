import json
import boto3
import re
import hashlib
from datetime import datetime as dt
from datetime import timedelta

from create_logger import create_logger

logger = create_logger(__name__)
ts_format = "%H-%M"
matcher = re.compile("([a-c][e-g][0-3]|[A-Z][5-9][f-w]){5,15}")


def get_logs(file_names, s3_bucket):
    logFileObjects = list(
        filter(
            lambda f: f.key in file_names, s3_bucket.objects.all()
        )
    )
    log_messages = [logFileObject.get()['Body'].read().decode('utf-8')
                    for logFileObject in logFileObjects]
    return log_messages


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
    if start_idx >= end_idx:
        if search_ts == start_ts:
            return start_idx
        if search_ts == end_ts:
            return end_idx
        logger.warn(f"search_time: {search_time} not in timestamps")
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


def get_files_from_s3(s3_bucket):
    """
    returns the log file names on given S3 bucket
    """
    try:
        files = s3_bucket.objects.all()
    except Exception as e:
        logger.exception("Issue with s3 bucket")

    return [file.key for file in files]


def get_time_stamps(files):
    """
    extracts the time stamps in the log files
    """
    return [file.split(".")[1] for file in files]


def get_end_time(start_time, time_delta):
    """
    calculates the upper bound of the requested window
    """
    try:
        start_time = dt.strptime(start_time, ts_format)
    except Exception as e:
        logger.exception("Incorrect string format for timestamp")
    return (start_time + timedelta(minutes=int(time_delta))).strftime(ts_format)


def get_msgs(log_messages):
    messages = list(
        map(
            lambda l: l.split(" ")[-1],
            log_messages.split("\n")
        )
    )
    return messages


def get_matched_msgs(messages):
    matched_msgs = [
        msg for msg in messages if matcher.search(msg) != None
    ]
    return matched_msgs


def get_md5_checksums(msg):
    return hashlib.md5(msg.encode('utf-8')).hexdigest()


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
        s3 = boto3.resource('s3', aws_access_key_id="",
                            aws_secret_access_key="")
        s3_bucket = s3.Bucket(bucket)
    except Exception as e:
        logger.exception("Issue with accessing S3")

    payload = json.loads(event['body'])
    start_time = payload["start_time"]
    time_delta = payload["time_delta"]

    # start_time = event["start_time"]
    # time_delta = event["time_delta"]

    log_files_in_s3 = get_files_from_s3(s3_bucket)
    time_stamps = get_time_stamps(log_files_in_s3)

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

    log_messages = get_logs(
        log_files_in_s3[log_file_start_idx:log_file_end_idx+1],
        s3_bucket
    )

    messages = list(map(get_msgs, log_messages))
    messages = list(map(get_matched_msgs, messages))
    messages = [msg for msgs in messages for msg in msgs]
    md5_checksums = list(map(get_md5_checksums, messages))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "md5_checksums": md5_checksums,
        }),
    }
