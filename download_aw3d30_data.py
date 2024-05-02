import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_file(lat, lon, base_url, save_dir, session_info):
    username, password = session_info
    end_lat = lat + 5
    end_lon = lon + 5
    
    # Format the latitude part of the filename
    if lat < 0:
        lat_prefix = 'S' + f"{abs(lat):03}"
    else:
        lat_prefix = 'N' + f"{lat:03}"
        
    if end_lat <= 0:
        end_lat_prefix = 'S' + f"{abs(end_lat):03}"
    else:
        end_lat_prefix = 'N' + f"{end_lat:03}"
        
    # Format the longitude part of the filename
    if lon < 0:
        lon_prefix = 'W' + f"{abs(lon):03}"
    else:
        lon_prefix = 'E' + f"{lon:03}"
        
    if end_lon <= 0:
        end_lon_prefix = 'W' + f"{abs(end_lon):03}"
    else:
        end_lon_prefix = 'E' + f"{end_lon:03}"
    
    # Combine into full tile name
    tile_name = f"{lat_prefix}{lon_prefix}_{end_lat_prefix}{end_lon_prefix}.zip"

    if os.path.isfile(os.path.join(save_dir, tile_name)):
        return f"{tile_name} already exists."

    with requests.Session() as session:
        #session.auth = (username, password)
        r1 = session.request('get', base_url + tile_name)
        r = session.get(r1.url)

        if r.ok and len(r.content) > 10000:
            with open(os.path.join(save_dir, tile_name), "wb") as binary_file:
                binary_file.write(r.content)
            print(f"Downloaded {tile_name}")

def download_all_tiles(base_url, save_dir, username, password):
    session_info = (username, password)

    futures = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for lat in range(-85, 85, 5):  # Adjust latitude range if necessary
            for lon in range(-180, 180, 5):  # Adjust longitude range if necessary
                futures.append(executor.submit(download_file, lat, lon, base_url, save_dir, session_info))

        for future in tqdm(as_completed(futures), total=len(futures)):
            ret = future.result()

# Parameters
base_url = "https://www.eorc.jaxa.jp/ALOS/aw3d30/data/release_v2404/"
save_dir = "/home/batman/Documents/global_topo_aw3d30_v2404"
username = 'cliff_finder'
password = 'Iwant1000mcliffs!'

# Start the download process
download_all_tiles(base_url, save_dir, username, password)
