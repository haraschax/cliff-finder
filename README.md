# cliff-finder, world's best finder of cliffs
I like cliffs, they look cool. If you're a lover of cliffs you may also be annoyed by the lack of rigorous cataloguing and recordkeeping of the world's tallest/steepest cliffs. Wikipedia entries and others are polluted with inflated metrics and cliffs that are conveniently close to populated areas. This repo finds cliffs through an objective analysis of world topographic maps. Many of the world's most extreme cliffs are not close to civilation, are not well documented if documented at all. Some may have never even be photographed.

This repo uses the [Copernicus GLO-30](https://portal.opentopography.org/raster?opentopoID=OTSDEM.032021.4326.3) dataset. It's the most accurate free dataset that I could find. It still has numerous flaws but far less than ASTER, ALOS, SRTM, and others I could find.

![cliffs_map_simple](cliffs_map_simple.png)
The above image is a map of all cliffs over 600m tall. Cliffs are defined here as an average slope of over 300%, though I'll be happy to use a different definition if anyone has strong arguments.

# How to use
install the needed packages and then run the download script (~1.5T of data) and run the search (2hrs on my machine):
```
cd cliff-finder
./dl_copernicus_glo30.sh
./find_cliffs.py
```
This will output a list of cliffs found, and a topographic map of each cliffs in `cliffs_found`

# Some cool cliffs this algorithm found
## Latok I, north face
The north face of Latok 1 shows a 300%+ grade for 1900m of elevation change according to cliff-finder. Which would make it the tallest cliff in the world. The total height change from the cliff peak to valley right in front of it is ~2300m.
![latok1](cliff_pics/latok1_north_face.jpg)

## Namcha Barwa, west face
Namcha Barwas's west face show's a 1450m 300% grade drop. The total height change to the from the peak to the river a couple miles down stream is ~4000m.
![barwa](cliff_pics/namcha_barwa.jpg)
