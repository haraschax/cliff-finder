import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_file(lat, lon, base_url, save_dir, session_info):
    username, password = session_info
    prefix = "ASTGTMV003"
    lat_prefix = 'N' if lat >= 0 else 'S'
    lon_prefix = 'E' if lon >= 0 else 'W'
    lat_str = f"{lat_prefix}{abs(lat):02d}"
    lon_str = f"{lon_prefix}{abs(lon):03d}"
    tile_name = f"{prefix}_{lat_str}{lon_str}.zip"

    if os.path.isfile(os.path.join(save_dir, tile_name)):
        return f"{tile_name} already exists."

    with requests.Session() as session:
        session.auth = (username, password)
        r1 = session.request('get', base_url + tile_name)
        r = session.get(r1.url, auth=(username, password))

        if r.ok:
            with open(os.path.join(save_dir, tile_name), "wb") as binary_file:
                binary_file.write(r.content)
            print(f"Downloaded {tile_name}")

def download_all_tiles(base_url, save_dir, username, password):
    session_info = (username, password)

    futures = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for lat in range(-85, 85):  # Adjust latitude range if necessary
            for lon in range(-180, 180):  # Adjust longitude range if necessary
                futures.append(executor.submit(download_file, lat, lon, base_url, save_dir, session_info))

        for future in tqdm(as_completed(futures), total=len(futures)):
            ret = future.result()

# Parameters
base_url = "https://e4ftl01.cr.usgs.gov/ASTT/ASTGTM.003/2000.03.01/"
save_dir = "/home/batman/Documents/global_topo_nasa/"
username = 'cliff_finder'
password = 'Iwant1000mcliffs!'

# Start the download process
download_all_tiles(base_url, save_dir, username, password)
