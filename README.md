# Image analysis of culture growth on petris dishes
Take an image of a petris dish with cultures and detect the culture circle.

Example (best so far):
![example](test.png)

# Setup virtual environment
## Install virtual environment
```
pip install virtualenv
```

## Install required packages
```
pip install -r requirements.txt
```

# Run code
Crop pictures (not needed, I think?)
```
$ python petrisCropper.py --help
usage: petrisCropper.py [-h] -c CIRCLESIZE

optional arguments:
  -h, --help            show this help message and exit
  -c CIRCLESIZE, --circlesize CIRCLESIZE
                        Size of circle
```
run example:
```
python petrisCropper.py -c 1000
```

Detect circles (cultures)
```
$ python colorManipulator.py --help
usage: colorManipulator.py [-h] -i IMAGE

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        path to image
```
run example:
```
python colorManipulator.py -i cropped_pic/23-06-2018_plates/MEA_47.5_Sc_#1.jpg
```
