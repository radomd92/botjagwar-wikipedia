import datetime

today = datetime.datetime.now()
SAME = object()
DEFAULT = object()


class State(object):
    country_code = None
    adm1_name = None
    adm1_name_poss = None
    country = None
    country_short = None
    translations = []

    def __init__(self, country='', country_short=SAME,
                 adm1_name=DEFAULT, adm1_name_poss=DEFAULT):
        if self.country is None:
            self.country = country
            if country_short == SAME:
                self.country_short = self.country
            else:
                self.country_short = country_short

        self.adm1_name = (
            adm1_name
            if adm1_name == DEFAULT
            else self.adm1_name
        )
        self.adm1_name_poss = (
            adm1_name_poss
            if adm1_name_poss != DEFAULT
            else self.adm1_name_poss
        )

    def serialise(self) -> dict:
        return {
            'translations': self.translations,
            'country_code': self.country_code,
            'adm1_name': self.adm1_name,
            'adm1_name_poss': self.adm1_name_poss,
            'country': self.country,
            'country_short': self.country_short,
            'today': '%d/%2d/%4d' % (today.day, today.month, today.year)
        }


class FederalState(State):
    adm1_name = 'faritany mizaka tena'
    adm1_name_poss = "faritany mizaka tenan'i"


class ProvinceState(State):
    adm1_name = 'faritany'
    adm1_name_poss = "faritanin'i"


class RegionState(State):
    adm1_name = 'faritra'
    adm1_name_poss = "faritra"


class PrefectureState(State):
    adm1_name = 'prefektiora'
    adm1_name_poss = "prefektioran'i"


from api.descriptors.additional_data.countries import (
    Australia, Indonesia
)


countries = {
    'AU': Australia(),
    'BR': FederalState('Brazila'),
    'CN': ProvinceState('Sina', "Repoblika Entim-bahoakan'i Sina"),
    'ES': RegionState('Espaina'),
    'IN': FederalState('India'),
    'IT': RegionState('Italia'),
    'ID': Indonesia(),
    'JP': PrefectureState('Japana'),
    'MG': RegionState('Madagasikara'),
    'MZ': ProvinceState('Mozambika'),
    'PT': ProvinceState('Pôrtogaly'),
    'ZA': ProvinceState('Afrika Atsimo')
}


country_contexts = {
    k: v.serialise() for k, v in countries.items()
}