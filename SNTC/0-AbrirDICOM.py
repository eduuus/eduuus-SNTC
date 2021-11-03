import pydicom as dicom
import PIL # optional
import pandas as pd
import matplotlib.pyplot as plt

# specify your image path
image_path = 'case5a_005 (cópia).dcm'
ds = dicom.dcmread(image_path)
plt.imshow( ds.pixel_array)

plt.show()