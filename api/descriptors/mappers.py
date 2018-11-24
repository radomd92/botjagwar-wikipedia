import csv
import datetime
from . import geonames_field_description as field_description


admin_code = {}


def fill_admin_codes():
    for csv_filename in ['admin2Codes.txt', 'admin1CodesASCII.txt']:
        csv_file = open(csv_filename, 'r')
        file_reader = csv.reader(csv_file, 'excel-tab')
        for line in file_reader:
            admin_code[line[0]] = line[1]


def type_cast(_type, field_no):
    def _type_cast(described_line):
        return _type(described_line[field_description[field_no]])
    return _type_cast


def convert_date(field_no):
    def _type_cast(described_line):
        year, month, day = [int(x) for x in described_line[field_description[field_no]].split('-')[:3]]
        return datetime.date(year, month, day).year
    return _type_cast


def get_admin1_code(described_line):
    key = (described_line['country code']
           + '.' + described_line['admin1 code'])
    return admin_code.get(key, described_line['admin1 code'])


def get_admin2_code(described_line):
    key = (described_line['country code']
           + '.' + described_line['admin1 code']
           + '.' + described_line['admin2 code'])

    mapped = admin_code.get(key, described_line['admin2 code'])

    return mapped