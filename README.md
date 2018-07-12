# Image analysis of culture growth on petris dishes
Take an image of a petris dish with cultures and detect the culture circle. Based on that calculate the area and the growth differences on daily basis.

# Setup virtual environment
## Install virtual environment
```
pip install virtualenv
```

## Install required packages
```
pip install -r requirements.txt
```

# Detect circles in pictures with VIA
VIA: VGG Image Annotator (VIA)
can be downloaded from  [here](http://www.robots.ox.ac.uk/~vgg/software/via/).

Rename all pictures and put it into the same folder. Do this by running
```
python src/renaming.py
```

Then use VIA to circle all the colonies. An example of this looks like the picture below.
![example](test.png)

After all (!) pictures have been annotated, run dataWrangler.py to format the annotation.csv into a nice data frame for further use.
**needs an update**
```
python src/dataWrangler.py
```

# Draw nice plots with bokeh
Run the notebook, which will create super nice interactive bokeh plots!
See the data/growth_media.html as an example.
