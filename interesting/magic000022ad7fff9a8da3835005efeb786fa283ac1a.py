#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing Libraries
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Importing Image data to numpy array
img = mpimg.imread('image.jpg')
print(type(img))
print(img)


# In[3]:


# Ploting Numpy arrays as Image
imgplot = plt.imshow(img)


# In[4]:


# Applying pseudocolor schemes to image plots
# (Pseudocolor can be a useful tool for enhancing contrast and visualizing your data more easily.)

pseudo_img = img[:, :, 0] # slicing in numpy array
plt.imshow(pseudo_img) # luminosity (2D, no color) image


# In[5]:


plt.imshow(pseudo_img, cmap='hot')


# In[6]:


# another way of using cmap is set_cmap() function
imgplot = plt.imshow(pseudo_img)
imgplot.set_cmap('nipy_spectral')


# In[7]:


# Color scale reference
imgplot = plt.imshow(pseudo_img)
plt.colorbar()


# In[20]:


imgplot = plt.imshow(pseudo_img, clim = (0.0, 500))


# In[35]:


# Array Interpolation schemes 
# nterpolation calculates what the color or value of a pixel "should" be, according to different mathematical schemes.
from PIL import Image
img = Image.open('image.jpg')
img.thumbnail((64, 64), Image.ANTIALIAS) # resize the image in-place # play with numbers to get more idea
imgplot = plt.imshow(img)


# In[36]:


# Interpolation "neatest"
imgplot = plt.imshow(img, interpolation='nearest')


# In[37]:


# Interpolation 'bicubic'
imgplot = plt.imshow(img, interpolation='bicubic')


# In[ ]:




