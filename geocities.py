import copy
import csv
import sys
import re
import pywikibot

from api.descriptors.additional_data import country_contexts
from api.descriptors import geonames_field_description as field_description
from api.descriptors.mappers import (
    type_cast,
    convert_date,
    get_admin1_code,
    get_admin1_code_translation,
    get_admin2_code,
    fill_admin_codes
)
from api.decorator import retry_on_fail

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

field_translators = {
    10: get_admin1_code_translation
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

            if column_nb in field_translators:
                mapped_data = field_translators[column_nb](described_data)
                described_data['mapped_' + field_description[column_nb]] = mapped_data

        yield described_data

    csv_file.close()


def create_admin1_pages(country_code):
    fill_admin_codes()
    c = 0
    additional_data = country_contexts[country_code]
    admin1_codes = []
    for d in get_populated_places(
            'country_data/' + '%s.csv' % country_code,
            additional_data):
        admin1_codes.append(d['mapped_admin1 code'])
        c += 1
        d['wiki_name'] = d['name'].replace('City', '(tanàna)')
        pywikibot.output('>>>>>> \03{white} #' + str(c) + ' -- ' + d['wiki_name'] + '\03{default} <<<<<<')

    for name in set(admin1_codes):
        if not name:
            continue

        guo = additional_data['country_short']
        lim = name[0]
        adm1_name_poss = additional_data['adm1_name_poss']
        page = pywikibot.Category(pywikibot.Site('mg', 'wikipedia'), f"Tanàna ao amin'ny {adm1_name_poss} {name}")
        c = f"[[sokajy:Tanàna ao {guo}|{lim}]]\n[[sokajy:{guo}|{lim}]]"
        print(page, c)
        page.put(c, 'mamorona sokajy')


def create_wikipedia_article(country_code, feature_class='P'):
    fill_admin_codes()
    c = 0
    additional_data = country_contexts[country_code]
    for d in get_populated_places('country_data/' + '%s.csv' % country_code, additional_data):
        if d['feature class'] == feature_class and int(d['population']) >= 40000:
            c += 1
            d['wiki_name'] = d['name'].replace('City of', "Tanànan'i")
            d['wiki_name'] = d['name'].replace('City', '(tanàna)')
            pywikibot.output('>>>>>> \03{white} #' + str(c) + ' -- ' + d['wiki_name'] + '\03{default} <<<<<<')
            content = to_wikipedia_article(d)
            pywikibot.output('\03{yellow}' + content + '\03{default}')
            create_wikipedia_entry(d)

    print(c)


def create_wikipedia_entry(d):
    page = pywikibot.Page(pywikibot.Site('mg', 'wikipedia'), d['wiki_name'])

    content = to_wikipedia_article(d)
    page.put(content, "tanàna ao amin'i %s" % d['mapped_admin1 code'])
    if page.exists() and not page.isRedirectPage():
        try:
            link_wikidata(d)
        except Exception as e:
            print(e)
            return

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


@retry_on_fail(Exception, 5, 5)
def link_wikidata(d):
    site = pywikibot.Site('ceb', 'wikipedia')
    page = pywikibot.Page(site, d['wiki_name'])
    if not page.exists():
        print('No exists')
        return

    try:
        item = pywikibot.ItemPage.fromPage(page)  # this can be used for any page object
    except Exception:
        return

    # you can also define an item like this
    item.get()  # you need to call it to access any data.
    if 'mg' in item.labels:
        print('The label in Malagasy is: ' + item.labels['en'])
    else:
        print('No label in Malagasy...')
        item.setSitelink(sitelink={'site': 'mgwiki', 'title': d['wiki_name']}, summary=u'added link to mg.wikipedia')


if __name__ == '__main__':
    country = sys.argv[1]
    create_admin1_pages(country)
    create_wikipedia_article(country)
