# MARUMARU_Collector

## Description
Download the comics registered on the Marumaru website.(marumaru.in)
Web crawler based action, images convert to pdf.
You can download cartoon shorts or download the whole series.

## Use
### Install files...
```bash
$ sudo apt-get install chromium-chromedriver python3-venv
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

------

## How to use
```python
> python mmc.py
Select mode All or Single(a/s)(Short or Series)
Plz input URL(only MARUMARU URL)
```
## Make windows runtime binary
```python
> python setup.py build
```
컴파일 후 buile/lib/multiprocessing/Pool.pyc 파일을 pool.pyc로 변경해 줘야 함.

## Not perfect

   Thank you.
