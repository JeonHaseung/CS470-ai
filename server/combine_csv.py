# combine tac_pairs csv files into one csv file

import csv
import os


DIR_PATH = './tac_pair'

g = open(DIR_PATH + '/' + 'tac_pairs.csv', 'w')
csv_writer = csv.writer(g)

added_fields = False

for file in os.listdir(DIR_PATH):
    if (file == 'tac_pairs.csv'):
        continue

    f = open(DIR_PATH + '/' + file, 'r')

    csv_reader = csv.reader(f)
    
    is_field_row = True
    for row in csv_reader:
        if is_field_row:
            is_field_row = False

            if not (added_fields):
                added_fields = True
                csv_writer.writerow(row)

        else:
            csv_writer.writerow(row)

    f.close()

g.close()
