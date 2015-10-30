__author__ = 'RAMOSVACCA'

import re
def regcoord(coord):
    a = re.findall("-?\d+\.\d+\s*,-?\d+\.\d+\s*", coord)
    #a = re.findall("\[-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?\]", coord)
    return a

#regcoord('ljdfkljaldjfdsaljfhljdf@3.35,-75.47jhfadshf poadshfp oadf @3.20,-74.3')


# \@          # at symbol
# -?          # An optional hyphen (for negative numbers)
# \d+         # one or more digits
# (?:\.\d+)?  # An optional period followed by one or more digits (for fractions)
# \s*         # Zero or more whitespace characters
# ,
# -?          # An optional hyphen (for negative numbers)
# \d+         # one or more digits
# (?:\.\d+)?  # An optional period followed by one or more digits (for fractions)
# \s*         # Zero or more whitespace characters
# $