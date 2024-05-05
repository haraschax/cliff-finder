import os
import sys
import glob 
import numpy as np
import rasterio
import multiprocessing
import cv2
from tqdm import tqdm
from random import shuffle
from pyproj import Geod
import shutil
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource


# lat, lon, blackout area radius
blacklist = [[27.822736740112305, 92.57917785644531, 20000],
             [27.879862, 93.0008, 20000],
             [28.443410873413086, 85.11734771728516, 20000],
             [29.648374557495117, 101.93683624267578, 15000],
             [5.212995529174805, -76.18224334716797, 10000],
             [59.947605, 6.6277957, 2000],
             [71.83742, -52.464878, 10000],
             [71.418915, -51.742565, 10000],
             [75.57478, -21.901924, 10000],
             [-12.0806055, -74.27191, 2000],
             [-49_05573, -74_76408, 10000],
             [-49.784317 , -74.62307, 5000],
             [-61.090355, -54.72234, 10000],
             [-66_79399, 163.20633, 10000],
             [29.65848541,   95.11452484,1000],
             [29.63715744,   95.06532288, 1000],
             [71.56819153,  -52.0521698, 1000],
             [-43.61115265,  170.07957458, 1000],
             [27.70921326,   97.11391449, 1000],
             [-67.37149811,  164.75134277, 10000]]

METERS_PER_PIXEL = 30
MAX_LAT = 85
MIN_DROP = 600
GRADE = 3
ROTATE_ANGLE_DEGREES = 30
IMAGE_SAVE_PAD = 200
MIN_SPACING_METERS = 3000

def in_blacklist(lat, lon):
  for black in blacklist:
      if calculate_distance(lat, lon, black[0], black[1]) < black[2]:
        return True
  return False

def save_topo(file_name, topo_array, cmap=matplotlib.cm.gist_earth, azdeg=315, altdeg=45):
  ls = LightSource(azdeg=azdeg, altdeg=altdeg)
  shaded = ls.shade(topo_array, cmap=cmap, vert_exag=0.1, blend_mode='overlay')
  plt.figure()
  plt.imshow(shaded, aspect='auto')
  plt.axis('off')  # Hide axes and ticks
  plt.savefig(file_name, bbox_inches='tight', pad_inches=0)
  plt.close()


def pad_array(array, num_rows, num_cols):
    padded_array = np.pad(array, ((num_rows, num_rows), (num_cols, num_cols)), mode='constant', constant_values=0)
    return padded_array

def calculate_distance(lat1, lon1, lat2, lon2):
    geod = Geod(ellps='WGS84')
    _, _, dist = geod.inv(lon1, lat1, lon2, lat2)
    return dist

def rotate(image, angle):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, scale=1.0)
    rotated = cv2.warpAffine(image, M, (w, h), borderValue=np.nan)
    return rotated

def get_image(lat, lon, array, coord_array):
    min_dist = np.nanargmin(np.linalg.norm(coord_array - np.array([lat, lon]), axis=-1))
    row, col = np.unravel_index(min_dist, array.shape)
    array = pad_array(array, IMAGE_SAVE_PAD, IMAGE_SAVE_PAD)
    row = row + IMAGE_SAVE_PAD
    col = col + IMAGE_SAVE_PAD
    return array[row-IMAGE_SAVE_PAD:row+IMAGE_SAVE_PAD, col-IMAGE_SAVE_PAD:col+IMAGE_SAVE_PAD]

def find_max_diff(file_path):
  repo_dir = os.path.dirname(__file__) 
  output_dir = repo_dir + "/cliffs_found/"
  with rasterio.open(file_path) as src:
    original_array = src.read(1)
    bounds = src.bounds

    # High latitudes have problems
    if abs(bounds.top) > MAX_LAT or  abs(bounds.bottom) > MAX_LAT:
      return None
    if np.nanmax(original_array) - np.nanmin(original_array) < MIN_DROP:
      return None
    w_meters = calculate_distance(bounds.bottom, bounds.left, bounds.bottom, bounds.right)
    h_meters = calculate_distance(bounds.bottom, bounds.left, bounds.top, bounds.left)
    width_pixels = int(w_meters / METERS_PER_PIXEL)
    height_pixels = int(h_meters / METERS_PER_PIXEL)
    array = cv2.resize(np.copy(original_array), (width_pixels, height_pixels), interpolation=cv2.INTER_LINEAR)

    grid = np.meshgrid(np.linspace(bounds.top, bounds.bottom, original_array.shape[0], dtype=np.float32),
                       np.linspace(bounds.left, bounds.right, original_array.shape[1], dtype=np.float32), indexing='ij')
    original_coord_array = np.stack(grid, axis=-1)

    grid = np.meshgrid(np.linspace(bounds.top, bounds.bottom, array.shape[0], dtype=np.float32),
                       np.linspace(bounds.left, bounds.right, array.shape[1], dtype=np.float32), indexing='ij')
    coord_array = np.stack(grid, axis=-1)

    desired_size = max(width_pixels, height_pixels) * 1.45
    pad_rows = int((desired_size - height_pixels) / 2)
    pad_cols = int((desired_size - width_pixels) / 2)
    array = np.pad(array, ((pad_rows, pad_rows), (pad_cols, pad_cols)), mode='constant', constant_values=np.nan)
    coord_array = np.pad(coord_array, ((pad_rows, pad_rows), (pad_cols, pad_cols), (0,0)), mode='constant', constant_values=np.nan)

  cliff_height = MIN_DROP
  test_runs = 0
  all_cliffs = []
  qualifying_cliffs = None
  while qualifying_cliffs is None or len(qualifying_cliffs) > 0:
    qualifying_cliffs = []
    for angle in range(0,180,ROTATE_ANGLE_DEGREES):
      array_rot = rotate(array.copy(), angle)
      coord_array_rot = rotate(coord_array.copy(), angle)
  
      LAT_DISTANCE = cliff_height / GRADE
      LAT_PIXELS = int(LAT_DISTANCE / METERS_PER_PIXEL)
      diff = abs(np.column_stack([0.0*array_rot[:,:LAT_PIXELS//2], array_rot[:,LAT_PIXELS:] - array_rot[:,:-LAT_PIXELS], 0.0*array_rot[:,-(LAT_PIXELS-LAT_PIXELS//2):]]))
      while np.nanmax(diff) > cliff_height:
        argmax_flat = np.nanargmax(diff)

        row, col = np.unravel_index(argmax_flat, diff.shape)
        lat, lon = coord_array_rot[row, col]

        qualifying_cliffs.append([diff[row, col], lat, lon, angle, original_array, original_coord_array])
        blackout_pixels = (MIN_SPACING_METERS / METERS_PER_PIXEL) //2
        diff[ min(0, row - blackout_pixels): max(row + blackout_pixels, diff.shape[0]),
              min(0, col - blackout_pixels): max(col + blackout_pixels, diff.shape[0])] = 0.0
        test_runs += 1
        if test_runs > 100:
          print(f"Test runs: {test_runs} on {file_path}, {cliff_height}m {len(all_cliffs)} cliffs found, might be hitting infinite loop")
    all_cliffs.extend(qualifying_cliffs)
    cliff_height += 100




  all_cliffs.sort(key=lambda x: x[0], reverse=True)
  for i, cliff in enumerate(all_cliffs):
    drama_factor, lat, lon, angle, original_array, original_coord_array = cliff
    
    # check if not too close to other cliffs
    too_close = False
    for other_cliff in all_cliffs[:i]:
      _, other_lat, other_lon, _, _, _ = other_cliff
      if calculate_distance(lat, lon, other_lat, other_lon) < MIN_SPACING_METERS:
        too_close = True
    if too_close or in_blacklist(lat, lon):
      continue
    else:
      print(f'Found {drama_factor}m diff at {lat}, {lon} in {file_path} at angle {angle}')
      lat_str = str(lat).replace(".", "_")
      lon_str = str(lon).replace(".", "_")
      image = get_image(lat, lon, original_array, original_coord_array)
      save_topo(f"{output_dir}lat_{lat_str}_lon_{lon_str}.png", np.nan_to_num(image))
      with open(f'{output_dir}full_list.txt', 'a') as the_file:
        the_file.write(f'{drama_factor}, {lat}, {lon}\n')
  return


def main():
  repo_dir = os.path.dirname(__file__) 
  output_dir = repo_dir + "/cliffs_found/"
  topo_database_dir = "/home/batman/Documents/global_topo_copernicus/"
  shutil.rmtree(output_dir, ignore_errors=True)
  os.makedirs(output_dir, exist_ok=True)
  print(f"Starting to find cliffs in {output_dir}")


  all_tifs = glob.glob(topo_database_dir + "*/*.tif")
  shuffle(all_tifs)
  num_processes = 20

  with multiprocessing.Pool(processes=num_processes) as pool:
    results = list(tqdm(pool.imap(find_max_diff, all_tifs), total=len(all_tifs)))


if __name__ == "__main__":
  main()