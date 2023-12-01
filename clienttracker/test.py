import pandas as pd
from parse import parse_vcard

pd.DataFrame(data=parse_vcard('data/contacts.vcf')).to_csv('data/target.csv')