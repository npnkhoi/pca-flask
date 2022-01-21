from sklearn.decomposition import PCA, TruncatedSVD
import numpy as np
from PIL import Image
import PIL
import math

def compress_image(img, method, n_components=5):
  """Compress an image and save to .pkl file. Return the reversed image"""
  print(f'Doing {method} with {n_components} components ...')
  new_img = []
  compression = []

  for i in range(3):
    # Create compressor (SVD or PCA)
    if method == 'pca':
      compressor = PCA(n_components=n_components)
    elif method == 'svd':
      compressor = TruncatedSVD(n_components=n_components)

    # Compress and reverse image
    data = img[:, :, i]
    compressor.fit(data)
    compressed = compressor.fit_transform(data)
    reversed = compressor.inverse_transform(compressed)
    
    compression.append((compressor, compressed))
    new_img.append(reversed / 255)
  
  # save to pickle file
  # pickle.dump(compression, open(f'data/{method}_{n_components}.pkl', 'wb'))
  
  # return reversed image
  new_img = np.dstack(new_img)
  new_img *= 255 / new_img.max() # normalize again
  new_img = new_img.astype(np.uint8)
  return new_img

def batch_pca(path):
  img = Image.open(path)
  img = np.array(img)
  h, w, _ = img.shape
  NUM_SEGMENTS = 10
  LENGTH_SEGMENT =  w // 10

  step = w ** (1 / (NUM_SEGMENTS - 1))
  pc = [math.floor(step ** i) for i in range(NUM_SEGMENTS)]
  for i, x in enumerate(pc):
    new_img = compress_image(img, 'pca', n_components=x)    
    new_img = Image.fromarray(new_img)
    new_img.save(f'static/new-{i+1}.jpg')
  return (w, pc)