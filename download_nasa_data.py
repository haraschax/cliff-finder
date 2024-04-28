import os
import requests
from tqdm import tqdm

base_url = "https://e4ftl01.cr.usgs.gov/ASTT/ASTGTM.003/2000.03.01/"
save_dir = "/home/batman/Documents/global_topo_nasa/"
username = 'cliff_finder'
password = 'Iwant1000mcliffs!'
prefix = "ASTGTMV003"

with requests.Session() as session:
    for lat in tqdm(range(-85, 85)):
        for lon in range(-180, 180):
            lat_prefix = 'N' if lat >= 0 else 'S'
            lon_prefix = 'E' if lon >= 0 else 'W'
            
            lat_str = f"{lat_prefix}{abs(lat):02d}"
            lon_str = f"{lon_prefix}{abs(lon):03d}"
            tile_name = f"{prefix}_{lat_str}{lon_str}.zip"

            if os.path.isfile(save_dir + tile_name):
                continue

            session.auth = (username, password)
            r1 = session.request('get', base_url + tile_name)
            r = session.get(r1.url, auth=(username, password))                
        
            if r.ok:
                with open(save_dir + tile_name, "wb") as binary_file:
                    binary_file.write(r.content)
