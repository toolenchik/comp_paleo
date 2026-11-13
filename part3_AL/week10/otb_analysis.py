# 1.3 The # %% cell format
# %% Setup
import numpy as np
import pandas as pd
print(np.__version__, pd.__version__)

# %% Part 1 — language basics
squared = [x**2 for x in range(10)]
print(squared)

# %% [markdown]
# ## Why virtual environments matter
#
# Without isolation, installing Flask for one project can silently break
# another. A virtual environment confines every `pip install` to a single
# project directory.


# 1.4 Python language features used throughout NumPy and pandas'
# %% List comprehensions
squared = [x**2 for x in range(10)]
filtered = [x for x in range(20) if x % 3 == 0]
print(squared)
print(filtered)

# %% Dictionary comprehensions
groups = {
    'Australopithecus': ['OTB-001', 'OTB-004'],
    'Paranthropus': ['OTB-002'],
    'Homo': ['OTB-003'],
}
taxon_counts = {name: len(specimens) for name, specimens in groups.items()}
print(taxon_counts)

# %% zip and enumerate
for i, genus in enumerate(['Australopithecus', 'Paranthropus', 'Homo']):
    print(i, genus)

locality_names = ['Koobi Fora', 'Kanapoi', 'Ileret', 'Allia Bay', 'Kalam Area']
counts = [294, 188, 232, 54, 6]
for locality, count in zip(locality_names, counts):
    print(f"{locality}: {count}")

# %% *args and **kwargs
specimens = pd.DataFrame({
    'specimen_id': ['OTB-001', 'OTB-002', 'OTB-003', 'OTB-004'],
    'taxon': ['Australopithecus', 'Paranthropus', 'Homo', 'Australopithecus'],
    'locality': ['FLK', 'KBS', 'FLK', 'Natron'],
    'age_ma': [1.87, 2.35, 1.65, 2.10],
    'element': ['femur', 'mandible', 'cranium', 'tibia'],
})

def summarize(*fields, decimals=2):
    for f in fields:
        print(f"{f}: {round(specimens[f].mean(), decimals)}")

summarize('age_ma')

# %% Lambda 
specimens['epoch'] = specimens['age_ma'].apply(lambda x: 'Pleistocene' if x < 2.6 else 'Pliocene')
print(specimens)

# 1.5 Deliverables — Part 1

# %% [markdown]
# A virtual environment or .venv is a folder that holds its "own" copy
# of Python and its packages. I am using it to keep my projects organized and use correct versions of
# packages to avoid conflicts with other projects.

# %% Setup
import numpy as np
import pandas as pd
print(np.__version__, pd.__version__)

# %% List comprehension
genus = ["Homo", "Paranthropus", "Australopithecus", "Kenyanthropus"]
print([x.upper() for x in genus if len(x) > 4])

# %% Dict comprehension
tuff_ages = {"KBS": 1.87, "Okote": 1.6, "Tulu Bor": 3.4}
print({tuff: age * 1000 for tuff, age in tuff_ages.items()})

# %% zip and enumerate
catalog = ["KNM-ER 406", "KNM-ER 1470", "KNM-WT 15000"]
taxon = ["Paranthropus", "Homo", "Homo"]
for i, (c, t) in enumerate(zip(catalog, taxon)):
    print(f"{i}: {c} ({t})")

# %% *args and **kwargs
def mean_age(*ages, units="Ma", **info):
    print(info)
    return f"{sum(ages) / len(ages):.2f} {units}"

print(mean_age(1.87, 1.6, 1.53, formation="Koobi Fora"))

# %% Lambda
to_ka = lambda age: age * 1000
print(to_ka(1.87))

# %% [markdown]
# ## Part 2 — NumPy
#%% ndarray
ages = np.array([1.87, 2.35, 1.65, 2.10, 1.92, 2.44, 1.73])
print(ages.dtype)    # float64
print(ages.shape)    # (7,)
print(ages.ndim)     # 1

# 3 specimens × 4 measurements (length, width, height, mass)
measurements = np.array([
    [45.2, 12.1, 8.3, 0.14],
    [38.7, 10.5, 7.1, 0.09],
    [51.0, 14.2, 9.6, 0.21],
])
print(measurements.shape)   # (3, 4)
print(measurements[0, :])   # first specimen, all measurements
print(measurements[:, 2])   # all specimens, height only

# %% Vectorized arithmetic
ages_bp = ages * 1_000_000          # Ma → years before present
print(ages_bp)
log_ages = np.log(ages)             # natural log of each element
print(log_ages)
z_scores = (ages - ages.mean()) / ages.std()
print(z_scores)

np.sqrt(measurements)     # element-wise square root
np.abs(z_scores)          # element-wise absolute value
np.log10(ages * 1e6)      # base-10 log


# 2.3 Boolean indexing and fancy indexing
# %% Boolean
old = ages[ages > 2.0]          # specimens older than 2 Ma
print(old)                      # array of selected values

# Compound conditions require & and |, not 'and' / 'or'
window = ages[(ages > 1.8) & (ages < 2.2)]
print(window)

# %% Fancy
idx = np.array([0, 2, 5])
print(ages[idx])                # ages at positions 0, 2, 5

# %% [markdown]
# ## 2.4 Axis operations
# Column means (mean of each measurement across all specimens)
col_means = measurements.mean(axis=0)   # shape (4,)
print(col_means)
# Row means (mean measurement per specimen)
row_means = measurements.mean(axis=1)   # shape (3,)
print(row_means)

# %% [markdown]
# ## 2.5 Deliverables — Part 2
# ## Part 2 — NumPy
# %% 1-D array 
ages = np.array([0.20, 1.53, 1.65, 1.70, 1.87, 1.90, 2.33, 2.50, 3.40, 4.10])
print(ages.dtype)
print(ages.shape)
print(ages.ndim)

ages_ka = ages * 1000
print(ages_ka)

# %% 2-D array: 5 molars × 3 measurements (length, width, height in mm)
molars = np.array([
    [13.2, 12.5, 7.1],
    [16.8, 15.4, 8.2],
    [12.1, 11.8, 6.5],
    [17.5, 16.0, 8.6],
    [12.9, 12.2, 6.9],
])
print(molars[0, :])        # first specimen
print(molars[:, 1])        # width of all specimens
print(molars.mean(axis=0)) 
print(molars.std(axis=1))  

# %% Boolean & fancy indexing
print(ages[ages < 2.0])                   

idx = np.array([0, 4, 9])
print(ages[idx])                           # three specimens by position

print(ages[(ages > 1.5) & (ages < 2.5)])   # between 1.5 and 2.5 Ma

# %% [markdown]
# NumPy is faster because it keeps similar values together and uses fast
# code behind the scenes, instead of having Python handle them one by one.
# For example, `ages * 1000` multiplies every value in one line,
# so we don't have to write a loop.
# Loops are still useful when we need the result from one step before
# starting the next, or when doing things like reading files one at a time
# or looking up each record in a database.

# %% Part 3 — pandas
# 3.1 Series

specimen_counts = pd.Series(
    [312, 187, 244, 98, 402],
    index=['FLK', 'KBS', 'Natron', 'Chesowanja', 'Turkana'],
)
print(specimen_counts['KBS'])          # 187  — label-based access
# print(specimen_counts[2])              # 244  — integer position
print(specimen_counts.iloc[2])                # added .iloc, otherwise prints error
print(specimen_counts[specimen_counts > 200])  # boolean filter

counts_2022 = pd.Series({'FLK': 312, 'KBS': 187, 'Natron': 244})
counts_2023 = pd.Series({'FLK': 19,  'KBS': 41,  'Natron': 8})
total = counts_2022 + counts_2023    # aligns on locality name
print(total)

# %% 3.2 DataFrame
# DataFrame from a dict
specimens = pd.DataFrame({
    'specimen_id': ['OTB-001', 'OTB-002', 'OTB-003', 'OTB-004'],
    'taxon':       ['Australopithecus', 'Paranthropus', 'Homo', 'Australopithecus'],
    'locality':    ['FLK', 'KBS', 'FLK', 'Natron'],
    'age_ma':      [1.87, 2.35, 1.65, 2.10],
    'element':     ['femur', 'mandible', 'cranium', 'tibia'],
})
print(specimens)

# %% DataFrame from a CSV
df = pd.read_csv('otb_fossils.tsv', sep='\t')
print(df.head())

# %% DataFrame from PostgreSQL
from sqlalchemy import create_engine
from config import DSN

# %% 3.4 Inspection
print(df.shape)
print(df.dtypes)
print(df.head(10))
print(df.tail(5))
df.info()
print(df.describe())
print(df.isnull().sum())

# %% loc and iloc
print(df.loc[5, 'scientific_name'])
print(df.iloc[0:5, 2:4])
print(df.loc[df['scientific_name'] == 11, 'formation'])
print(df.loc[df['scientific_name'] == 11, ['formation', 'preparations']])
print(df.iloc[:10, 1:4])

# %% Chained assignment (incorrect)
df[df['taxon'] == 'Homo']['age_ma'] = 0

# %% Boolean selection
pliocene_paranthropus = df[(df['earliest_epoch_or_lowest_series'] == 'Pliocene') & df['scientific_name'].isin([3, 4, 14])]
print(pliocene_paranthropus)
print(df.columns.tolist())

# %% 3.5 
# Derived column
df['avg_age'] = df[['earliest_chronometric_age', 'latest_chronometric_age']].mean(axis=1)
df['epoch'] = df['avg_age'].apply(lambda x: 'Pleistocene' if x < 2.6 else 'Pliocene')
df.loc[df['avg_age'].isna(), 'epoch'] = None
df['taxon_short'] = df['scientific_name'].str.split().str[0]
print(df[['scientific_name', 'avg_age', 'epoch', 'taxon_short']].head())

# %% 3.6 Sorting & summarizing
df = df.sort_values('avg_age', ascending=False)
print(df[['catalog_number', 'avg_age']].head())

print(df['taxon_short'].value_counts())

by_taxon = df.groupby('taxon_short')['avg_age'].agg(['mean', 'min', 'max', 'count'])
print(by_taxon)

by_locality = df.groupby('locality').size()
print(by_locality)

# %% 3.7
fossils = pd.DataFrame({
    'specimen_id': ['KNM-ER 1470a', 'KNM-ER 819', 'KNM-WT 15000aa', 'KNM-ER 13750',
                    'KNM-ER 1464', 'KNM-WT 17000', 'KNM-KP 29281a', 'KNM-KP 29282'],
    'taxon':       ['Homo', 'Homo', 'Homo', 'Paranthropus',
                    'Paranthropus', 'Paranthropus', 'Australopithecus', 'Australopithecus'],
    'locality':    ['Koobi Fora', 'Ileret', 'Nachukui', 'Koobi Fora',
                    'Ileret', 'Nachukui', 'Kanapoi', 'Kanapoi'],
    'age_ma':      [2.08, 1.54, 1.50, 1.93, 1.64, 2.57, 4.20, 4.20],
    'element':     ['Cranium', 'Mandible', 'Postcranium', 'Cranium',
                    'Postcranium', 'Cranium', 'Mandible', 'Tooth'],
})
fossils.info()
print(fossils.describe())

# %% loc and iloc
print(fossils.loc[fossils['taxon'] == 'Homo'])
print(fossils.iloc[0:3])

# %% Derived cols
fossils['age_ka'] = fossils['age_ma'] * 1000
fossils['epoch'] = fossils['age_ma'].apply(lambda x: 'Pleistocene' if x < 2.58 else 'Pliocene')
print(fossils.head())

# %% Sorting and grouping
print(fossils.sort_values('age_ma'))
print(fossils.groupby('taxon')['age_ma'].agg(['count', 'mean']))

# %% [markdown]
# Homo and Paranthropus each have three specimens, and Australopithecus has two.
# Australopithecus is the oldest group (4.2 Ma) and the only taxon from Pliocene.
# Average age for Homo is 1.7 MA, and 2.04 Ma for Paranthropus.

# %% [markdown]
# ## Part 4 Deliverables

# %% Load the OTB data from PostgreSQL
from sqlalchemy import create_engine
from config import DSN

engine = create_engine(DSN)
df = pd.read_sql("""
    SELECT f.catalog_number,
           t.scientific_name,
           l.place AS locality_name,
           l.country,
           f.earliest_chronometric_age,
           f.latest_chronometric_age,
           f.preparations
    FROM fossils f
    JOIN taxa t USING (taxon_id)
    JOIN localities l USING (locality_id)
""", engine)

print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
print(df.describe())

# %% [markdown]
# The dataset has 1243 specimens. 28 specimens have no chronometric age.
# The oldest earliest age is 6.5 Ma, which is much older than the rest of the sample.

# %% 2. Questions
# %% Specimens per taxon
print(df['scientific_name'].value_counts())

# %% [markdown]
# "Hominini" is the largest group (335), followed by Au. anamensis (242) and 
# P. boisei (205). Homo erectus has 154 specimens, while H. habilis has 100, H. Linnaeus has 91. 
# P. aethiopicus contains 66, Au. Dart has 28. P. Broom and K. platyops have 20 and 2, respectively.

# %% Age by locality
by_locality = df.groupby('locality_name')['earliest_chronometric_age'].agg(['mean', 'min', 'max'])
print(by_locality)

# %% [markdown]
# Lothagam and Kanapoi are the oldest localities (4.6 and 4.2 Ma on
# average), while Ileret and Koobi Fora are the youngest (1.7–1.9 Ma).

# %% Most common skeletal element
print(df['preparations'].value_counts())

# %% [markdown]
# Teeth are by far the most common element (688).

# %% Localities with only one taxon
taxa_per_locality = df.groupby('locality_name')['scientific_name'].nunique()
print(taxa_per_locality[taxa_per_locality == 1])

# %% [markdown]
# Kanapoi (Au. anamensis), Lothagam and South Turkwel (both
# only "Hominini") contain a single taxon.

# %% NumPy: ages (1 SD)
ages = df['earliest_chronometric_age'].dropna().to_numpy()
mean = ages.mean()
std = ages.std()
within = (ages > mean - std) & (ages < mean + std)
print(mean, std, within.mean())

