# velocity-map

Intermediate  server layer to show data from bom.gov.au on Leaflet maps

## Source data

Source data as .nc files should be accesible in ./bom_file folder

The current software downloads files from bom.gov.ua to quickly demonstrate conversion capabilities, but for production it is recommended to develop a more redundant download process. Please note that bom.gov.au FTP is slow, and it takes much time to download files for first time, at least 1 minute for small file.

## JSON data for maps

The current software automatically generates the .json files required for the Leaflet maps and stores them in the ./bom_data folder. These files are generated automatically on demand. Generation takes 10-20 seconds on the cheapest AWS instance, but after generation file is cached permanently.

## Data sampling

Data is sampled with a rate defined by `divisor` varible in files model_scalar.py and model_vector.py

Due to low performance of Leaflet IDW plugin it is not recommended to use divisor lower than 10 for scalar data. For vector data divisor may be lowered uo to 1, due to enough high performance of Leaflet Velocity plugin

## App running

To start app use command:

`python application.py`