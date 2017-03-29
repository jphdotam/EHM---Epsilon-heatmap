import scipy.ndimage
import scipy.misc
import numpy as np

MAPS_DIR = "./maps/"

key_17 = [[50, 10, 0],  [50, 20, 0],  [50, 30, 0],  [50, 40, 0],  [50, 50, 0],  [50, 60, 0], #Pixel colours for the key
          [100, 10, 0], [100, 20, 0], [100, 30, 0], [100, 40, 0], [100, 50, 0], [100, 60, 0],
          [150, 10, 0], [150, 20, 0], [150, 30, 0], [150, 40, 0], [150, 50, 0], [150, 60, 0],
          [200, 0, 0]]

map_17_dirty = scipy.ndimage.imread("{}map_17_dirty.png".format(MAPS_DIR))
map_17 = np.zeros(map_17_dirty.shape)

for y in range(map_17_dirty.shape[0]):
    for x in range(map_17_dirty.shape[1]):
        #print("Checking: {}".format(np.ndarray.tolist(map_17_dirty[y, x][:-1])))
        if np.ndarray.tolist(map_17_dirty[y, x][:-1]) in key_17:
            map_17[y,x] = map_17_dirty[y,x]
scipy.misc.imsave("{}map_17.png".format(MAPS_DIR),map_17)
