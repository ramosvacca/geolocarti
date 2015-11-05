__author__ = 'RAMOSVACCA'

import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

print(strip_accents('https://www.google.com/maps?q=CSIC-+Estación+Biológica+de+Doñana+EBD'))