import os
from collections import defaultdict

POI_FILE_PATH = '../../cleansed_data/training_data/poi_data/poi_data'
OUTPUT_FOLDER = '../../processed_data/poi_summary_data'
OUTPUT_FILE_NAME = 'poi_summary_data'

if __name__ == '__main__':
    pois_dict = dict()
    max_category_number = 0
    for district_id in range(1, 67):
        pois_dict[str(district_id)] = defaultdict(int)
        for poi in range(1, 26):
            pois_dict[str(district_id)][str(poi)] = 0

    with open(POI_FILE_PATH, 'r') as f:
        for line in f.readlines():
            district_poi_counts = line.strip().split()
            district_id = district_poi_counts[0]
            poi_counts = district_poi_counts[1:]

            for poi_count in poi_counts:
                poi, count = poi_count.split(':')
                sharp_idx = poi.find('#')

                # Get top-level category
                if sharp_idx != -1:
                    poi = poi[: sharp_idx]

                pois_dict[district_id][poi] += int(count)

                if int(poi) > max_category_number:
                    max_category_number = int(poi)

    # Create output folder if not exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE_NAME)
    with open(output_path, 'w') as f:
        f.write('# district_id\tnumber_of_top_level_poi(from 1 to 25)\n')

        for district_id in range(1, 67):
            f.write(str(district_id))

            for poi in range(1, 26):
                f.write('\t' + str(pois_dict[str(district_id)][str(poi)]))
            f.write('\n')
