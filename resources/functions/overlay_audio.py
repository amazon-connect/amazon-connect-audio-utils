import io
import json


import boto3
from pydub import AudioSegment

s3r = boto3.resource('s3')

def lambda_handler(event, context):
    """This expects an evnet in the following format:

    .. highlight:: python
        {
            "sources": [{
                "Bucket": "",
                "Key": "",
            },
            {
                "Bucket": "",
                "Key": ""
            }],
            "target": {
                "Bucket": "",
                "Key": ""
            }
        }
    """
    source1_buf = io.BytesIO()
    source2_buf = io.BytesIO()
    source1 = event['sources'][0]
    source2 = event['sources'][1]
    s3r.Object(
        source1['Bucket'],
        source1['Key']
    ).download_fileobj(source1_buf)
    s3r.Object(
        source2['Bucket'],
        source2['Key']
    ).download_fileobj(source2_buf)

    sound1 = AudioSegment.from_wav(source1_buf)
    sound2 = AudioSegment.from_wav(source2_buf)
    one_track = sound1.overlay(sound2)
    combined_buf = io.BytesIO()
    one_track.export(combined_buf, format='wav')
    combined_buf.seek(0)
    s3r.Object(
        event['target']['Bucket'],
        event['target']['Key']
    ).upload_fileobj(combined_buf)


