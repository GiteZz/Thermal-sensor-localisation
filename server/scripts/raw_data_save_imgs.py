from datetime import datetime
from help_module.csv_helper import load_csv, write_csv_list_frames
from help_module.time_helper import convert_to_datetime
from localization.processing import ImageProcessor

csv_file = "raw_data.csv"

pros = ImageProcessor()



pcb_versions = ['v2_met_batterij', 'v2_zonder_batterij', 'pcb_Gilles', 'breadboard', 'v1', 'volledig_batterij']

for file_name in pcb_versions:
    meas = load_csv(file_name + '.csv', to_numpy=True, split=False, csv_tag=False)[0]
    pros.set_thermal_data(meas.data)
    img = pros.get_imgs()[0]

    img.save(file_name + '.png')
