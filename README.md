# Connect Audio Utils

This is a set of lambda and ffmpeg powered tools for working with audio from Amazon Connect

## Tools

### Connect Audio Utils Layer

This layer includes:

* statically compiled ffmpeg
* boto3
* [pydub](https://github.com/jiaaro/pydub)
* requests
* [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)

### Overlay Audio

This function overlays two audio tracks and accepts input in the following form:

```json
{
    "sources": [{
        "Bucket": "",
        "Key": ""
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
```

### Redact Audio

This function mutes/removes sections of audio from a track based no timestamps and accepts input in the following form:

```json
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
```

## Build Instructions

1. Install CDK (npm i -g aws-cdk)
1. First build the layer:

    ```bash
    cd resources/connect-audio-utils-layer
    mkdir bin/
    curl -s https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJC bin --strip=1 'ffmpeg-*-amd64-static/ffmpeg'
    docker run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.8 pip3 install -r requirements.txt -t python
    zip -r9 layer.zip bin python -x "*.pyc"
    ```

1. Change back to root directory of project `cd ../..`
1. Install deps: `npm install`
1. Next run `npm run build`
1. Deploy with run `cdk deploy` (you may need to run `cdk bootstrap` first)

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template

## License

This project is licensed under the Apache-2.0 License.
