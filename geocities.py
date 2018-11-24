import copy
import csv
import datetime
import re
import pywikibot

from api.descriptors import geonames_field_description as field_description
from api.descriptors.mappers import \
    type_cast, convert_date, get_admin1_code, get_admin2_code, fill_admin_codes


TEMPLATE = open('wikipedia.template', 'r').read()


def to_wikipedia_article(described_data):
    return TEMPLATE % described_data


field_mappers = {
    4: type_cast(float, 4),
    5: type_cast(float, 5),
    10: get_admin1_code,
    11: get_admin2_code,
    18: convert_date(18)
}


def get_populated_places(csv_filename, additional_data):
    csv_file = open(csv_filename, 'r')
    file_reader = csv.reader(csv_file, 'excel-tab')
    for line in file_reader:
        described_data = copy.deepcopy(additional_data)
        for column_nb, column_data in enumerate(line):
            described_data[field_description[column_nb]] = column_data

        for column_nb, column_data in enumerate(line):
            if column_nb in field_mappers:
                mapped_data = field_mappers[column_nb](described_data)
                described_data['mapped_' + field_description[column_nb]] = mapped_data

        yield described_data

    csv_file.close()


def main():
    fill_admin_codes()
    c = 0
    today = datetime.datetime.now()
    additional_data = {
        'country': "Japana",
        'country_short': "Japana",
        'today': '%d/%2d/%4d' % (today.day, today.month, today.year)
    }

    for d in get_populated_places('JP.csv', additional_data):
        if (d['feature class'] == 'P'
                and 70000 > int(d['population']) > 60000
                #and d['mapped_admin1 code'] == 'Shandong'
        ):
            c += 1
            d['wiki_name'] = d['name'].replace('City', '(tanàna)')
            pywikibot.output('>>>>>> \03{white} #' + str(c) + ' -- ' + d['wiki_name'] + '\03{default} <<<<<<')
            content = to_wikipedia_article(d)
            pywikibot.output('\03{yellow}' + content + '\03{default}')
            create_wikipedia_entry(d)


def create_wikipedia_entry(d):
    page = pywikibot.Page(pywikibot.Site('mg', 'wikipedia'), d['wiki_name'])
    if page.exists() and not page.isRedirectPage():
        return

    content = to_wikipedia_article(d)
    page.put(content, "tanàna ao amin'i %s" % d['mapped_admin1 code'])


def add_coord(d):
    page = pywikibot.Page(pywikibot.Site('mg', 'wikipedia'), d['name'])
    if page.exists() and not page.isRedirectPage():
        old_content = content = page.get()
        if content.find(d['mapped_admin1 code']) != -1:
            coord = '{{coord|%f|%f}}\n' % (float(d['latitude']), float(d['longitude']))
            content = re.sub('\{\{coord(.*)\}\}\n', '', content)
            if content.find('{{coord') == -1:
                content = coord + content
        else:
            print(content.find(d['mapped_admin1 code']))

        if old_content != content:
            pywikibot.showDiff(old_content, content)
            page.put(content, "tanàna ao %s" % d['mapped_admin1 code'])
    else:
        print('pejy tsy misy')


if __name__ == '__main__':
    main()
