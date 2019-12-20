# Build Instructions

```bash
mkdir bin/
curl -s https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJC bin --strip=1 'ffmpeg-*-amd64-static/ffmpeg'
docker run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.8 pip3 install -r requirements.txt -t python
zip -r9 layer.zip bin python -x "*.pyc"
```
