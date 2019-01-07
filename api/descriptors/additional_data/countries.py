from api.descriptors.additional_data import FederalState, ProvinceState


class Indonesia(ProvinceState):
    country = "Indonezia"
    country_short = "Indonezia"
    translations = [
        ('Riau Islands', 'Nosy Riao'),
        ("West Nusa Tenggara", "Nusa Tenggara Andrefana"),
        ("North Sumatra", "Sumatra Avaratra"),
        ("West Kalimantan", "Kalimantan Andrefana"),
        ("South Sulawesi", "Sulawesi Atsimo"),
        ("West Sumatra", "Sumatra Andrefana"),
        ("East Nusa Tenggara", "Nusa Tenggara Atsinanana"),
        ("Central Java", "Java Afovoany"),
        ("North Sulawesi", "Sulawesi Avaratra"),
        ("Central Sulawesi", "Sulawesi Avaratra"),
        ("North Kalimantan", "Kalimantan Avaratra"),
        ("South Kalimantan", "Kalimantan Atsimo"),
        ("West Papua", "Papoa Andrefana"),
        ("North Maluku", "Maluku Avaratra"),
        ("Bangka–Belitung Islands ", "Nosy Bangka–Belitung"),
        ("West Sulawesi", "Sulawesi Andrefana"),
        ("East Java", "Java Atsinanana"),
        ("Southeast Sulawesi", "Sulawesi Atsimo Atsinanana"),
        ("South Sumatra", "Sumatra Atsimo"),
        ("West Java", "Java Andrefana"),
        ("East Kalimantan", "Kalimantan Atsimanana"),
        ("Central Kalimantan", "Kalimantan Afovoany"),
    ]


class Australia(FederalState):
    country = "Aostralia"
    country_short = "Aostralia"
    translations = [
        ('New South Wales', 'Valesa Atsimo Vaovao'),
        ('South Australia', 'Aostralia Atsimo'),
        ('West Australia', 'Aostralia Andrefana'),
        ('Western Australia', 'Aostralia Andrefana'),
        ('Northern Territories', 'Faritany Avaratra'),
        ('Northern Territory', 'Faritany Avaratra'),
        ('ACT', 'Faritanin-drenivohitra Aostralianina'),
    ]