import tempfile

import boto3
import ffmpeg

s3r = boto3.resource('s3')

def lambda_handler(event, context):
    """This expects an event in the following format:

    .. highlight:: python
        {
            "source": {
                "Bucket": "",
                "Key": ""
            },
            "target": {
                "Bucket": "",
                "Key": ""
            },
            "timestamps": [
                {"begin": "1000", "end": "2000"},
                {"begin": "5000", "end": "8000"}
            ]
        }

    times provided in milliseconds
    """
    original = tempfile.NamedTemporaryFile()
    redacted = tempfile.NamedTemporaryFile(suffix='.wav')
    with original, redacted:
        # download original
        s3r.Object(
            event['source']['Bucket'],
            event['source']['Key']
        ).download_file(original.name)
        
        # loop through timestamps and mute sections
        redacted_file = ffmpeg.input(original.name)
        for ts in event['timestamps']:
            enable = f"between(t,{int(ts['begin'])/1000},{int(ts['end'])/1000})"
            redacted_file = redacted_file.filter('volume', enable=enable, volume=0)
        redacted_file.output(redacted.name).overwrite_output().run()
        
        # upload redacted
        s3r.Object(
            event['target']['Bucket'],
            event['target']['Key']
        ).upload_file(redacted.name)
