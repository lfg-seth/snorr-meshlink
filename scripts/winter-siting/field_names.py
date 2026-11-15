"""Field-facing names. The original model IDs remain stable GIS join keys."""
LABELS = {
    'GK': ('KFS', 'Kyle Fire Station'), 'GL': ('LFS', 'Lee Fire Station'),
    'LF': ('LB', 'Lower Bristlecone'), 'LC': ('LJ', 'Lee Junction'),
    'CH': ('UC', 'Upper Cathedral'), 'FL': ('FL', 'Fletcher'),
    'AL': ('AP', 'Angel Peak Approach'), 'EL': ('LH', 'Lee Highway'),
    'SG': ('SG', 'Showgirl'), 'CM': ('CP', 'Champion'), 'KJ': ('KJ', 'Kyle Junction'),
    'SK': ('UB', 'Upper Bristlecone Helipad'), 'CL': ('LC', 'Lower Cathedral'),
    'AV': ('AV', 'Angel Peak Vegas Side'), 'AM': ('AM', 'Angel Peak Mountain Side'),
    'SI': ('SI', 'Sisters'), 'DV': ('DV', 'Desert View'), 'SA': ('SM', 'Sawmill'),
    'MK': ('MM', 'Macks Middle'), 'MU': ('UM', 'Upper Macks'),
    'HT': ('HT', 'Hilltop'), 'RR': ('RR', 'Robbers Roost'),
    'FV': ('FV', 'Fletcher View'), 'DC': ('DC', 'Deer Creek'),
    'KV': ('KV', 'Kyle Visitor Approach'), 'LM': ('LM', 'Lee Meadows'),
    'LS': ('AS', 'Angel Peak Saddle'), 'KR': ('UK', 'Upper Kyle'),
    'ML': ('ME', 'Macks East'), 'MW': ('MW', 'Macks West'),
    'BC': ('DCN', 'Deer Creek North'), 'BS': ('DCS', 'Deer Creek South'),
    'EK': ('KH', 'Kyle Highway'),
    'BE': ('LBE', 'Lee Bowl East'), 'BW': ('LBW', 'Lee Bowl West'),
    'JS': ('LJS', 'Lee Junction South'), 'LE': ('LME', 'Lee Meadows East'),
    'SE': ('SER', 'Sisters East Ridge'), 'MN': ('MMN', 'Macks Mouth North'),
    'MS': ('MSS', 'Macks South Shoulder'), 'UN': ('UMN', 'Upper Macks North'),
    'MR': ('MSR', 'Macks South Ridge'), 'NR': ('MNR', 'Macks North Ridge'),
    'RE': ('LRE', 'Lee Road East'), 'SN': ('SNE', 'Sisters Northeast'),
}

def field_code(key):
    return LABELS[key][0]

def field_name(key):
    return LABELS[key][1]

def navigation_name(key):
    return f'{field_name(key)} ({field_code(key)})'
