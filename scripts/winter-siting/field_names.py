"""Field-facing names. The original model IDs remain stable GIS join keys."""
LABELS = {
    'GK': ('KFS', 'Kyle Fire Station'), 'GL': ('LFS', 'Lee Fire Station'),
    'LF': ('LB', 'Lower Bristlecone'), 'LC': ('LJ', 'Lee Junction'),
    'CH': ('UC', 'Upper Cathedral'), 'FL': ('FL', 'Fletcher'),
    'AL': ('LS', 'Lucky Strike'), 'EL': ('LH', 'Lee Highway'),
    'SG': ('SG', 'Showgirl'), 'CM': ('CP', 'Champion'), 'KJ': ('KJ', 'Kyle Junction'),
    'SK': ('RH', 'Resort Helipad'), 'CL': ('LC', 'Lower Cathedral'),
    'AV': ('AV', 'Angel Vegas'), 'AM': ('AM', 'Angel Mountain'),
    'SI': ('SI', 'Sisters'), 'DV': ('DV', 'Desert View'), 'SA': ('SM', 'Sawmill'),
    'MK': ('MM', 'Macks Middle'), 'MU': ('UM', 'Upper Macks'),
    'HT': ('HT', 'Hilltop'), 'RR': ('RR', 'Robbers Roost'),
    'FV': ('FV', 'Fletcher View'), 'DC': ('DC', 'Deer Creek'),
    'KV': ('KV', 'Kyle Visitor Approach'), 'LM': ('LM', 'Lee Meadows'),
    'LS': ('LSS', 'Lucky Strike Saddle'), 'KR': ('UK', 'Upper Kyle'),
    'ML': ('ME', 'Macks East'), 'MW': ('MW', 'Macks West'),
    'BC': ('DCN', 'Deer Creek North'), 'BS': ('DCS', 'Deer Creek South'),
    'EK': ('KH', 'Kyle Highway'),
}

def field_code(key):
    return LABELS[key][0]

def field_name(key):
    return LABELS[key][1]

def navigation_name(key):
    return f'{field_name(key)} ({field_code(key)})'
