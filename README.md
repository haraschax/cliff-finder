[Interactive Cliff Map Click Here](https://haraschax.github.io/cliff-finder/)
# cliff-finder, world's best finder of cliffs

I like cliffs; they look cool. If you're a lover of cliffs, you may also be annoyed by the lack of rigorous cataloging and recordkeeping of the world's tallest/steepest cliffs. [Wikipedia entries](https://en.wikipedia.org/wiki/Cliff) and others are polluted with inflated metrics and cliffs that are predominately famous because they are close to populated areas. This repo finds cliffs through an objective analysis of world topographic maps. Many of the world's most extreme cliffs are not close to civilization, and are not well documented, if documented at all. Some may have never even have been photographed.

This repo uses the [Copernicus GLO-30](https://portal.opentopography.org/raster?opentopoID=OTSDEM.032021.4326.3) dataset. It's the most accurate free dataset that I could find. It still has numerous flaws, but far fewer than ASTER, ALOS, SRTM, and others.

![cliffs_map_simple](cliffs_map_simple.png)
The above image is a map of all cliffs over 600m tall. Cliffs are defined here as an average slope of over 300%, though I'll be happy to use a different definition if anyone has strong arguments.

# How to use
install the needed packages and then run the download script (~1.5T of data) and run the search (2hrs on my machine):
```
cd cliff-finder
./dl_copernicus_glo30.sh
./find_cliffs.py
```
This will output a list of cliffs found, and a topographic map of each cliff in `cliffs_found`

# Some cool cliffs this algorithm found
### Latok I, Pakistan, 35°55'50.9"N 75°49'26.6"E
The north face of Latok 1 shows a 300%+ grade for 1900m of elevation change, according to cliff-finder. Which would make it the tallest cliff in the world. The total height change from the cliff peak to the valley right in front of it is ~2300m.
![latok1](cliff_pics/latok1_north_face.jpg)

### Namcha Barwa, China, 29°37'14.8"N 95°02'12.6"E
![barwa](cliff_pics/namcha_barwa_west.jpg)

### Mount Foster, Antarctica, 63°00'25.7"S 62°35'14.6"W
![foster](cliff_pics/foster.jpg)

### Cerro Duida, Venezuela, 3°20'10.9"N 65°33'15.2"W
Deep in the Venezuelan jungle. Over 100km from the closest road lies Cerro Duida. A large plateau mountain with close to 1000m cliffs all around.\
![duida](cliff_pics/duida.jpeg)

### Fatu Hiva's Sea Cliffs, French Polynesia, 10°31'30.9"S 138°41'03.5"W
![fatu](cliff_pics/fatu_hiva.jpg)

### Takamaka Valley, Reunion, 21°05'49.5"S 55°37'13.6"E
![takamaka](cliff_pics/takamaka.jpg)

### Filchner Mountains, Antarctica, 71°58'36.2"S 7°35'47.9"E
![filchner](cliff_pics/filchner.jpg)

### Schiben, Switzerland, 46°48'59.6"N 8°57'52.4"E
![schiben](cliff_pics/schiben.png)

### Sumidero Canyon, Mexico, 16°49'59.1"N 93°03'52.7"W
![sumidero](cliff_pics/sumidero.webp)

### Half Dome and El Capitan in Yosemite, USA, 37°44'41.5"N 119°32'10.3"W and 37°43'48.0"N 119°38'11.0"W
Both Yosemite's famous cliff walls show up with cliff-finder too
![both_yosemite](cliff_pics/both_yosemite.jpg)
