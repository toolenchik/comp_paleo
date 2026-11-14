# %% 1.3 Loading JSON with the standard library
import json

with open('ecv_otb_subset.json') as f:
    ecv_raw = json.load(f)

print(type(ecv_raw))                    # dict
print(ecv_raw['source'])                # citation string
print(ecv_raw['region'])
print(len(ecv_raw['specimens']))        # 20 specimens
print(ecv_raw['specimens'][0])          # first record as a dict

# %% 1.4 Normalizing nested JSON to a DataFrame

import pandas as pd

ecv_otb = pd.json_normalize(ecv_raw['specimens'])
print(ecv_otb.head())
print(ecv_otb.dtypes)
print(ecv_otb.shape)

# %% 1.5 Reading the full CSV dataset
ecv_full = pd.read_csv('ecv_by_specimen.csv')
print(ecv_full.shape)     
print(ecv_full.dtypes)
print(ecv_full.head())

# %% 1.6 Comparing formats
# Column names are the same — confirm the subset is a true subset of the full CSV
print(set(ecv_otb.columns) == set(ecv_full.columns))   # True

# Confirm the 20 OTB specimen IDs are all present in the full CSV
print(ecv_otb['ID'].isin(ecv_full['ID']).all())         # True

ecv_full = pd.read_csv('ecv_by_specimen.csv', dtype={'ID': str}) ## overrides default dtype
print(ecv_full.dtypes)

# %% 1.8 Deliverables — Part 1

import json
import pandas as pd
from sqlalchemy import create_engine


# %% 1
with open('ecv_otb_subset.json') as f:
    ecv_json = json.load(f)

print(ecv_json['source'])
print(ecv_json['region'])
print(len(ecv_json['specimens']))        # 20 specimens

ecv_otb = pd.json_normalize(ecv_json['specimens'])
print(ecv_otb.dtypes)
print(ecv_otb.shape)                    # (20, 8)

# %% [markdown] 2
# (a) JSON `null` becomes `NaN`. `NaN` is a float, so one `null` turns an
# `int64` column into `float64`. (b) A single column can only have one dtype. 
# Some medians have decimals (e.g. 737.5), so he whole column becomes `float64`.
# (c) Numeric IDs with leading zeros (e.g. `00731`): without
# `dtype={'ID': str}` they become `731`, and joins to text IDs fail.

# %% 3
import sys
# loading week 10 directory, to use confiq.py
sys.path.append('/Users/saidatokmurzina/comp_paleo/part3_AL/week10') 
from config import DSN
engine = create_engine(DSN)

otb_sql = pd.read_sql('SELECT * FROM otb_fossils', engine)
otb_csv = pd.read_csv('otb_fossils.csv')    

print(otb_sql.dtypes)
print(otb_csv.dtypes)


# %%2.1 Missing values

ecv_full.isnull().sum()                            # count per column
ecv_full.dropna(subset=['ecv_median_cm3'])         # drop rows missing ECV
ecv_full['ecv_median_cm3'].fillna(ecv_full['ecv_median_cm3'].mean())

# %% 2.2 The n_estimates column as a data quality indicator
print(ecv_full['n_estimates'].value_counts().sort_index())

# How many specimens have only one estimate?
single = (ecv_full['n_estimates'] == 1).sum()
print(f"{single} of {len(ecv_full)} specimens have n_estimates == 1")

# Compare mean ECV for single-estimate vs multi-estimate specimens
print(ecv_full.groupby(ecv_full['n_estimates'] > 1)['ecv_median_cm3'].mean())

# %% 2.3 The grade column
grade_labels = {
    'archaic': 'Archaic australopith',
    'mega':    'Robust australopith / Paranthropus',
    'trans':   'Transitional (H. habilis)',
    'pre.mod': 'Pre-modern Homo'
}
ecv_full['grade_label'] = ecv_full['grade'].map(grade_labels)
print(ecv_full['grade_label'].value_counts())

# %% 2.4 Binning by age
bins   = [0.0, 1.0, 2.0, 2.6, 3.5]
labels = ['Late Pleistocene', 'Early Pleistocene', 'Plio-Pleistocene', 'Pliocene']

ecv_full['time_bin'] = pd.cut(ecv_full['age_mid_Ma'],
                               bins=bins, labels=labels)
print(ecv_full['time_bin'].value_counts())

# %% 2.5 String cleaning
print(ecv_full['taxon'].unique())


ecv_full = pd.read_csv('ecv_by_specimen.csv')

# %%  2.6 Deliverables — Part 2
# ## 1. Missing values, grade labels, time bins

print(ecv_full.isnull().sum())

grade_labels = {
    'archaic': 'Archaic australopith',
    'mega':    'Robust australopith / Paranthropus',
    'trans':   'Transitional (H. habilis)',
    'pre.mod': 'Pre-modern Homo'
}
ecv_full['grade_label'] = ecv_full['grade'].map(grade_labels)
print(ecv_full['grade_label'].value_counts())

bins   = [0.0, 1.0, 2.0, 2.6, 3.5]
labels = ['Late Pleistocene', 'Early Pleistocene', 'Plio-Pleistocene', 'Pliocene']
ecv_full['time_bin'] = pd.cut(ecv_full['age_mid_Ma'], bins=bins, labels=labels)
print(ecv_full['time_bin'].value_counts())


# %% 2
print(ecv_full['taxon'].unique())     

ecv_hominin = ecv_full[ecv_full['taxon'].str.startswith(('P.', 'H.'))]
print(ecv_hominin.shape)
print(ecv_hominin['taxon'].unique())

# %% [markdown]
# None of the Australopithecus specimens come from the Turkana Basin. 
# They are from Ethiopia and South Africa.

# %% 3.2 Preparing the join keys
from sqlalchemy import create_engine
from config import DSN

engine = create_engine(DSN)
fossils = pd.read_sql(
    "SELECT f.*, t.scientific_name FROM fossils f JOIN taxa t USING (taxon_id)",
    engine
)

# Compare taxon names
print("OTB taxa:", sorted(fossils['scientific_name'].unique()))
print("ECV taxa:", sorted(ecv_full['taxon'].unique()))

# %%
## WHAT I ADDED:
# Drop years and author names
fossils['taxon'] = fossils['scientific_name'].str.extract(r'^([A-Z][a-z]+(?: [a-z]+)?)')[0]

# ECV: write the genus out in full
taxon_map = {
    'Au. afarensis':      'Australopithecus afarensis',
    'Au. africanus':      'Australopithecus africanus',
    'Au. garhi':          'Australopithecus garhi',
    'Au. sediba':         'Australopithecus sediba',
    'P. aethiopicus':     'Paranthropus aethiopicus',
    'P. boisei':          'Paranthropus boisei',
    'P. robustus':        'Paranthropus robustus',
    'H. habilis':         'Homo habilis',
    'H. erectus':         'Homo erectus',
    'H. heidelbergensis': 'Homo heidelbergensis',
}
ecv_full['taxon'] = ecv_full['taxon'].map(taxon_map)

print("OTB taxa:", sorted(fossils['taxon'].unique()))
print("ECV taxa:", sorted(ecv_full['taxon'].unique()))
print("Shared:  ", sorted(set(fossils['taxon']) & set(ecv_full['taxon'])))

# %% 3.3 Summarizing ECV by taxon
ecv_by_taxon = (
    ecv_full
    .groupby('taxon')['ecv_median_cm3']
    .agg(ecv_mean='mean', ecv_median='median',
         ecv_min='min', ecv_max='max', ecv_n='count')
    .reset_index()
)
print(ecv_by_taxon)

# %% join to the OTB fossils:

fossils_ecv = pd.merge(
    fossils,
    ecv_by_taxon,
    left_on='taxon', right_on='taxon',
    how='left'
)
print(fossils_ecv.shape)        # should equal fossils.shape (left join preserves all rows)
print(fossils_ecv['ecv_mean'].isnull().sum())   # taxa with no ECV data

# %% 3.4 Including the age uncertainty range

# Specimen-level join — only works where catalog_number == ECV specimen ID
specimen_join = pd.merge(
    fossils,
    ecv_full[['ID', 'ecv_median_cm3', 'age_lo_Ma', 'age_hi_Ma', 'n_estimates']],
    left_on='organism_id', right_on='ID',
    how='inner'
)
print(f"{len(specimen_join)} OTB fossils matched a published ECV measurement")
print(specimen_join[['catalog_number', 'taxon', 'ecv_median_cm3', 'n_estimates']])


# %% PART 3 -deliverables
fossils = pd.read_sql(
    "SELECT f.*, t.scientific_name FROM fossils f JOIN taxa t USING (taxon_id)",
    engine
)
print("OTB taxa:", sorted(fossils['scientific_name'].unique()))
print("ECV taxa:", sorted(ecv_full['taxon'].unique()))

# %%
fossils['taxon_name'] = fossils['scientific_name'].str.extract(r'^([A-Z][a-z]+(?: [a-z]+)?)')[0]

taxon_map = {
    'Au. afarensis':      'Australopithecus afarensis',
    'Au. africanus':      'Australopithecus africanus',
    'Au. garhi':          'Australopithecus garhi',
    'Au. sediba':         'Australopithecus sediba',
    'P. aethiopicus':     'Paranthropus aethiopicus',
    'P. boisei':          'Paranthropus boisei',
    'P. robustus':        'Paranthropus robustus',
    'H. habilis':         'Homo habilis',
    'H. erectus':         'Homo erectus',
    'H. heidelbergensis': 'Homo heidelbergensis',
}
ecv_full['taxon'] = ecv_full['taxon'].replace(taxon_map)

ecv_full.loc[ecv_full['ID'] == 'KNM-ER 3732',  'taxon'] = 'Homo habilis'
ecv_full.loc[ecv_full['ID'] == 'KNM-ER 23000', 'taxon'] = 'Paranthropus boisei'

print("Shared taxa:", sorted(set(fossils['taxon_name']) & set(ecv_full['taxon'])))

# %% [markdown]
# ECV: species names written in full. OTB: authorship removed (Homo erectus (Dubois, 1892) 
# to Homo erectus). KNM-ER 3732: H. erectus in Du et al., H. habilis in OTB,  mapped to
# H. habilis. KNM-ER 23000: P. aethiopicus in Du et al., P. boisei in OTB, mapped to
# P. boisei.


# %% 2
ecv_by_taxon = (
    ecv_full
    .groupby('taxon')['ecv_median_cm3']
    .agg(ecv_mean='mean', ecv_median='median',
         ecv_min='min', ecv_max='max', ecv_n='count')
    .reset_index()
)
print(ecv_by_taxon)

fossils_ecv = pd.merge(fossils, ecv_by_taxon,
                       left_on='taxon_name', right_on='taxon', how='left')
print(fossils.shape)
print(fossils_ecv.shape)

# %% [markdown]
# Same row count: a left join keeps every fossil, and ecv_by_taxon has one
# row per taxon, so no rows are duplicated.

# %%
print(fossils_ecv[['catalog_number', 'taxon_name', 'ecv_mean']].head(10))
print(fossils_ecv['ecv_mean'].isnull().sum())
print(fossils_ecv[fossils_ecv['ecv_mean'].isnull()]['taxon_name'].value_counts())

# %% [markdown]
# 718 rows have no ECV: Hominini, Australopithecus, Kenyanthropus
# records identified only to genus. Du et al. has no ECV for any of these.


# %% 3
ecv_full['ID'] = ecv_full['ID'].replace({
    'Omo L.338y-6':     'L 338/Y-6',
    'Omo 323-1976-896': 'OMO 323-1976-896',
})

specimen_join = pd.merge(
    fossils,
    ecv_full[['ID', 'ecv_median_cm3', 'age_lo_Ma', 'age_hi_Ma', 'n_estimates']],
    left_on='organism_id', right_on='ID', how='inner'
)
print(f"{specimen_join['organism_id'].nunique()} OTB fossils matched a published ECV measurement")

# %% [markdown]
# Only 18 of 663 individuals match. Most OTB fossils are teeth or jaws. ECV needs a braincase.
# IDs are written differently in the two sources (2 Omo IDs fixed by hand).
# Two specimens have a different species in each source.
# Most Du et al. specimens are not from Turkana.

# %% 4
fossils_ecv['age_mid_Ma'] = (fossils_ecv['earliest_chronometric_age'] +
                             fossils_ecv['latest_chronometric_age']) / 2
fossils_ecv['time_bin'] = pd.cut(fossils_ecv['age_mid_Ma'], bins=bins, labels=labels)

ecv_pivot = pd.pivot_table(fossils_ecv, values='ecv_mean', index='taxon_name',
                           columns='time_bin', aggfunc='mean', observed=True)
print(ecv_pivot.round(1))

# %% [markdown]
# Each taxon has a single ecv_mean, so the table shows when each taxon
# occurs, not brain growth within a species. P. aethiopicus (419) comes
# first, then P. boisei (488) and H. habilis (658), then H. erectus (923).
# Larger-brained taxa appear later.
