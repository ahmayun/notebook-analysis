# Importing Libraries
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
%matplotlib inline

# Importing Image data to numpy array
img = mpimg.imread('image.jpg')
print(type(img))
print(img)

# Ploting Numpy arrays as Image
imgplot = plt.imshow(img)

# Applying pseudocolor schemes to image plots
# (Pseudocolor can be a useful tool for enhancing contrast and visualizing your data more easily.)

pseudo_img = img[:, :, 0] # slicing in numpy array
plt.imshow(pseudo_img) # luminosity (2D, no color) image

plt.imshow(pseudo_img, cmap='hot')

# another way of using cmap is set_cmap() function
imgplot = plt.imshow(pseudo_img)
imgplot.set_cmap('nipy_spectral')

# Color scale reference
imgplot = plt.imshow(pseudo_img)
plt.colorbar()

imgplot = plt.imshow(pseudo_img, clim = (0.0, 500))

# Array Interpolation schemes 
# nterpolation calculates what the color or value of a pixel "should" be, according to different mathematical schemes.
from PIL import Image
img = Image.open('image.jpg')
img.thumbnail((64, 64), Image.ANTIALIAS) # resize the image in-place # play with numbers to get more idea
imgplot = plt.imshow(img)

# Interpolation "neatest"
imgplot = plt.imshow(img, interpolation='nearest')

# Interpolation 'bicubic'
imgplot = plt.imshow(img, interpolation='bicubic')



