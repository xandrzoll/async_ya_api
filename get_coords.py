import asyncio
import pandas as pd
import re
import json

from pathlib import Path
from services.async_func import process_get_geo_coordinates_async, get_geo_coordinates_async, choose_address
from services.func import get_distance_sph


DATA_PATH = Path()
DATA_PATH_OUT = Path()


def main():
    data = pd.read_excel(DATA_PATH)
    data['address'] = data['region'] + ', ' + data['address']
    data['geo_data'] = asyncio.run(
        process_get_geo_coordinates_async(get_geo_coordinates_async, iterator=data['address'])
    )
    data['geo_data'] = data['geo_data'].apply(lambda x: choose_address(x) if x != '' else {})
    data['geo_coords'] = data['geo_data'].apply(lambda x: x.get('GeoObject', {}).get('Point', {}).get('pos', ''))
    data.to_excel(DATA_PATH_OUT, index=False)


def work_with_data():
    import json

    data = pd.read_csv(DATA_PATH_OUT, sep=';')
    data['geo_json'] = data['geo_data'].apply(lambda x: json.dumps(x.replace("'", '"')))


if __name__ == '__main__':
    main()



