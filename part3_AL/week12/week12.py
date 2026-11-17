# %% Imports
import json
import os
import pandas as pd
from plotnine import *
from sqlalchemy import create_engine

from config import DSN

# %% Load data
engine = create_engine(DSN)

fossils = pd.read_sql(
    """
    SELECT f.*, t.scientific_name, l.*
    FROM fossils f
    JOIN taxa t USING (taxon_id)
    JOIN localities l USING (locality_id)
    """,
    engine
)

# set the path to the week 11 folder so the file can be located.
path = os.path.join("/Users/saidatokmurzina/comp_paleo/part3_AL/week11/ecv_by_specimen.csv")
ecv_full = pd.read_csv(path)

# Grade is a ordered categorical variable. 
# We need to set the ordering or else it will default
# to alphabetical. 
grade_order = ['archaic', 'mega', 'trans', 'pre.mod']
ecv_full['grade'] = pd.Categorical(ecv_full['grade'],
	categories=grade_order,
	ordered=True)
# %%	
# Re-create taxon_map and fossils_ecv from Week 11
# (copy your working code from otb_analysis_w11.py)

# l.* repeats locality_id, so drop the duplicate column
fossils = fossils.loc[:, ~fossils.columns.duplicated()]

# OTB: remove author and year
fossils['taxon_name'] = fossils['scientific_name'].str.extract(r'^([A-Z][a-z]+(?: [a-z]+)?)')[0]

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
ecv_full['taxon'] = ecv_full['taxon'].replace(taxon_map)

# Two specimens classified differently in OTB
ecv_full.loc[ecv_full['ID'] == 'KNM-ER 3732',  'taxon'] = 'Homo habilis'
ecv_full.loc[ecv_full['ID'] == 'KNM-ER 23000', 'taxon'] = 'Paranthropus boisei'

# ECV summary by taxon, joined to OTB fossils
ecv_by_taxon = (
    ecv_full
    .groupby('taxon')['ecv_median_cm3']
    .agg(ecv_mean='mean', ecv_median='median',
         ecv_min='min', ecv_max='max', ecv_n='count')
    .reset_index()
)

fossils_ecv = pd.merge(fossils, ecv_by_taxon,
                       left_on='taxon_name', right_on='taxon', how='left')

# Age midpoint and time bins
fossils_ecv['age_mid_Ma'] = (fossils_ecv['earliest_chronometric_age'] +
                             fossils_ecv['latest_chronometric_age']) / 2

bins   = [0.0, 1.0, 2.0, 2.6, 3.5]
labels = ['Late Pleistocene', 'Early Pleistocene', 'Plio-Pleistocene', 'Pliocene']
fossils_ecv['time_bin'] = pd.cut(fossils_ecv['age_mid_Ma'], bins=bins, labels=labels)

print(fossils.shape)
print(fossils_ecv.shape)  

# %% Part 1 — Univariate Distributions
# ## 1.1 Histogram
# ECV distribution across all specimens in Du et al.
p1 = (ggplot(ecv_full, aes(x='ecv_median_cm3'))
      + geom_histogram(binwidth=60, fill='steelblue', color='white')
      + labs(x='Endocranial volume (cm³)', y='Count',
             title='Distribution of hominin ECV estimates')
      + theme_bw()
)
p1.save('ecv_histogram.png', dpi=150)

# %% 1.2 Density plot
p2 = (ggplot(ecv_full, aes(x='ecv_median_cm3', fill='grade'))
      + geom_density(alpha=0.4)
      + scale_fill_brewer(type='qual', palette='Set2')
      + labs(x='Endocranial volume (cm³)', fill='Grade')
      + theme_bw()
)
p2.save('ecv_density_by_grade.png', dpi=150)

# %% 1.3 Deliverables
# ## 1. Histogram 

p1_25 = (ggplot(ecv_full, aes(x='ecv_median_cm3'))
         + geom_histogram(binwidth=25, fill='steelblue', color='white')
         + labs(x='Endocranial volume (cm³)', y='Count', title='Bin width 25')
         + theme_bw()
)
p1_25.save('ecv_histogram_25.png', dpi=150)

p1_50 = (ggplot(ecv_full, aes(x='ecv_median_cm3'))
      + geom_histogram(binwidth=50, fill='steelblue', color='white')
      + labs(x='Endocranial volume (cm³)', y='Count',
             title='Bin width 50')
      + theme_bw()
)
p1_50.save('ecv_histogram.png', dpi=150)
p1_100 = (ggplot(ecv_full, aes(x='ecv_median_cm3'))
          + geom_histogram(binwidth=100, fill='steelblue', color='white')
          + labs(x='Endocranial volume (cm³)', y='Count', title='Bin width 100')
          + theme_bw()
)
p1_100.save('ecv_histogram_100.png', dpi=150)

# %% [markdown]
# Bin width 25 is too fine. Many bins are empty or hold 1–2 specimens, so the plot looks 
# noisy. Bin width 50 shows the main pattern: a peak at about 400–500 cm^3(australopiths and Paranthropus), 
# a dip around 600–750, and a broad spread of Homo from about 750 to 1100. Bin width
# 100 is too coarse: the peak is still visible, but the dip mostly disappears
# and Homo looks like one flat block.

# %% 2. Density plot
p2 = (ggplot(ecv_full, aes(x='ecv_median_cm3', fill='grade'))
      + geom_density(alpha=0.4)
      + scale_fill_brewer(type='qual', palette='Set2')
      + labs(x='Endocranial volume (cm³)', fill='Grade')
      + theme_bw()
)
p2.save('ecv_density_by_grade.png', dpi=150)

# %% [markdown]
# (a) pre.mod has the widest range (500–1300 cm^3). It covers H.erectus and H. heidelbergensis,
# and about 1.6 million years, during which brain size increased. This rapid brain expansion trend
# perhaps was driven by a feedback loop between climate shifts, dietary changes, tool use. 
# Ecology shifts drastically, tool use enables easier access to new sources of calories and meat, 
# diigestive systems become less complex --> extra calories can then support brain expansion.
# (b) trans and pre.mod overlap at 550–800 cm³, mostly with H. erectus. ECV alone cannot 
# separate H. habilis from early H. erectus, hence other traits are needed.

# %% Part 2 — Bivariate Relationships
# ## 2.1 Scatter plot
p3 = (ggplot(ecv_full, aes(x='age_mid_Ma', y='ecv_median_cm3',
                            color='grade', size='n_estimates'))
      + geom_point(alpha=0.7)
      + scale_x_reverse()          # older ages on the left
      + scale_color_brewer(type='qual', palette='Set1')
      + labs(x='Age (Ma)', y='ECV (cm³)',
             color='Grade', size='N estimates',
             title='Hominin ECV through time')
      + theme_bw()
)
p3.save('ecv_vs_age.png', dpi=150)

# %% 2.2 Adding a trend line
p4 = (ggplot(ecv_full, aes(x='age_mid_Ma', y='ecv_median_cm3'))
      + geom_point(aes(color='grade'), alpha=0.6)
      + geom_smooth(method='lm', color='black', linetype='dashed')
      + scale_x_reverse()
      + labs(x='Age (Ma)', y='ECV (cm³)')
      + theme_bw()
)
p4.save('ecv_trend.png', dpi=150)

# %% 2.3 Boxplot by taxon
# Order taxa by median ECV
taxon_order = (ecv_full.groupby('taxon')['ecv_median_cm3']
               .median()
               .sort_values()
               .index.tolist())

ecv_full['taxon'] = pd.Categorical(ecv_full['taxon'],
                                    categories=taxon_order,
                                    ordered=True)

p5 = (ggplot(ecv_full, aes(x='taxon', y='ecv_median_cm3', fill='grade'))
      + geom_boxplot()
      + coord_flip()               # horizontal boxes, easier to read long labels
      + labs(x='', y='ECV (cm³)', fill='Grade')
      + theme_bw()
      + theme(legend_position='bottom')
)
p5.save('ecv_boxplot_taxon.png', dpi=150)

# %% 2.4 Deliverables — Part 2
# ## 1. Scatter with color and shape by grade

p3 = (ggplot(ecv_full, aes(x='age_mid_Ma', y='ecv_median_cm3',
                            color='grade', shape='grade', size='n_estimates'))
      + geom_point(alpha=0.7)
      + scale_x_reverse()
      + scale_color_brewer(type='qual', palette='Set1')
      + labs(x='Age (Ma)', y='ECV (cm³)',
             color='Grade', shape='Grade', size='N estimates',
             title='Hominin ECV through time')
      + theme_bw()
)
p3.save('ecv_vs_age.png', dpi=150)

# %% [markdown]
# Using both color and shape for grade means the grades can still be told apart
# by readers with color blindness, in black-and-white prints, and where points
# overlap.

# %% 2. Trend lines: overall vs per grade
p4b = (ggplot(ecv_full, aes(x='age_mid_Ma', y='ecv_median_cm3', color='grade'))
       + geom_point(alpha=0.6)
       + geom_smooth(aes(group='grade'), method='lm')
       + geom_smooth(aes(group=1), method='lm', color='black', linetype='dashed')
       + scale_x_reverse()
       + labs(x='Age (Ma)', y='ECV (cm³)', color='Grade')
       + theme_bw()
)
p4b.save('ecv_trend_by_grade.png', dpi=150)

# %% [markdown]
# Overall, ECV rises, but the slopes are different per grade.
# Only pre.mod has a similar slope compared to the general graph. archaic and mega 
# are almost flat, and trans goes the other ways.

# %% [markdown]
# (a) H. erectus varies most (550–1300 cm^3). It spans about 1.6 million years
# and several continents. 
# (b) The australopiths and Paranthropus boxes overlap heavily (about
# 400–550 cm^3). P. robustus and H. habilis overlap, and so do lower H. erectus. 
# ECV separates small-brained taxa from later Homo, but it cannot 
# reliably tell individual species apart.

# %% Part 3 — OTB Data
# ## 3.1 Specimen counts by taxon and locality
counts = (fossils_ecv
          .groupby(['taxon_name', 'subregion'])
          .size()
          .reset_index(name='n_specimens'))

p6 = (ggplot(counts, aes(x='subregion', y='n_specimens', fill='taxon_name'))
      + geom_col()                 # stacked bar (geom_col uses a pre-computed y)
      + coord_flip()
      + labs(x='', y='Specimens', fill='Taxon')
      + theme_bw()
      + theme(legend_position='bottom',
              figure_size=(8, 5))
)
p6.save('otb_counts.png', dpi=150)

# %% 3.2 Faceting
# Find taxa with 2 or more specimens
taxon_counts = ecv_full['taxon'].value_counts()
multi_specimen_taxa = taxon_counts[taxon_counts > 1].index

p7 = (ggplot(ecv_full[~ecv_full['taxon'].isin(['Au. sediba', 'Au. garhi'])],
		aes(x='age_mid_Ma', y='ecv_median_cm3', color='taxon'))
	+ geom_point(alpha=0.6)
	+ geom_smooth(method='lm', se=False, linetype='dashed', size=0.8)
	+ facet_wrap('~taxon', scales='free_y')
	+ scale_x_reverse()
	+ labs(x='Age (Ma)', y='Median ECV (cm³)')
	+ theme_bw()
	+ theme(legend_position='none', # redundant with facet labels
		figure_size=(10, 6))
)
p7.save('otb_ecv_faceted.png', dpi=150)

# %% 3.3 Deliverables — Part 3
# # 1. Stacked vs dodged bars

counts = (fossils_ecv
          .groupby(['taxon_name', 'subregion'])
          .size()
          .reset_index(name='n_specimens'))

p6 = (ggplot(counts, aes(x='subregion', y='n_specimens', fill='taxon_name'))
      + geom_col()
      + coord_flip()
      + labs(x='', y='Specimens', fill='Taxon')
      + theme_bw()
      + theme(legend_position='bottom', figure_size=(8, 5))
)
p6.save('otb_counts.png', dpi=150)

p6b = (ggplot(counts, aes(x='subregion', y='n_specimens', fill='taxon_name'))
       + geom_col(position='dodge')
       + coord_flip()
       + labs(x='', y='Specimens', fill='Taxon')
       + theme_bw()
       + theme(legend_position='bottom', figure_size=(8, 6))
)
p6b.save('otb_counts_dodge.png', dpi=150)

# %% [markdown]
# Stacked bars are better for comparing totals per subregion and seeing each
# taxon's share. Dodged bars are better for comparing one taxon across
# subregions, because every bar starts at zero.

# %% 2. Faceted scatter plot
ecv_full['ID'] = ecv_full['ID'].replace({
    'Omo L.338y-6':     'L 338/Y-6',
    'Omo 323-1976-896': 'OMO 323-1976-896',
})

individuals = (fossils_ecv
               .groupby('organism_id')
               .agg(taxon_name=('taxon_name', 'first'),
                    age_mid_Ma=('age_mid_Ma', 'mean'),
                    n_elements=('catalog_number', 'count'))
               .reset_index())

ind_ecv = pd.merge(individuals, ecv_full[['ID', 'ecv_median_cm3', 'grade']],
                   left_on='organism_id', right_on='ID')
print(ind_ecv)

p7b = (ggplot(ind_ecv, aes(x='age_mid_Ma', y='ecv_median_cm3'))
       + geom_point(aes(color='grade', size='n_elements'), alpha=0.7)
       + geom_smooth(method='lm', se=False, linetype='dashed', size=0.8)
       + facet_wrap('~taxon_name', scales='free_y', ncol=2)
       + scale_x_reverse()
       + labs(x='Age (Ma)', y='ECV (cm³)', color='Grade', size='N elements')
       + theme_bw()
       + theme(strip_text=element_text(size=9), figure_size=(8, 6))
)
p7b.save('otb_ecv_faceted_grade.png', dpi=150)

# %% [markdown]
# P. boisei is quite flat, about 400–500 cm^3 from 2.1 to 1.6 Ma.
# H. habilis gets smaller toward the present. The H. habilis panel has one pre.mod point,
# KNM-ER 3732, which was reassigned in Week 11.

# %% 3. Heatmap: locality and taxon
counts_loc = (fossils_ecv
              .groupby(['place', 'taxon_name'])
              .size()
              .reset_index(name='n_specimens'))

p8 = (ggplot(counts_loc, aes(x='taxon_name', y='place', fill='n_specimens'))
      + geom_tile(color='white')
      + geom_text(aes(label='n_specimens'), size=7)
      + scale_fill_gradient(low='#f7fbff', high='#08306b')
      + coord_equal()
      + labs(x='', y='', fill='Specimens')
      + theme_bw()
      + theme(axis_text_x=element_text(rotation=45, ha='right'),
              figure_size=(9, 7))
)
p8.save('otb_heatmap.png', dpi=150)

# %% [markdown]
# The most common combinations are Kanapoi with Au. anamensis (188), Type Area
# with Hominini (143) and P. aethiopicus (60), Ileret with P. boisei (99), and
# Nachukui with H. erectus (84). Many combinations are empty. H. habilis is
# almost only in East Turkana. Lothagam and South Turkwel have only Hominini.
# Most of these gaps come from the age of each site's deposits and from how
# intensively it was collected, not from ecology. Koobi Fora and Ileret are
# large and heavily surveyed, while the Type Area holds many small fragments
# that can only be identified as Hominini. A real ecological signal would need
# localities of the same age with similar sampling effort.

# %% 4. Figure quality: ECV vs age
grade_colors = {'archaic': '#E69F00', 'mega': '#56B4E9',
                'trans': '#009E73', 'pre.mod': '#CC79A7'}   # Okabe-Ito, colorblind-safe

p9 = (ggplot(ecv_full, aes(x='age_mid_Ma', y='ecv_median_cm3',
                            color='grade', shape='grade', size='n_estimates'))
      + geom_point(alpha=0.8)
      + annotate('point', x=1.959, y=756.2, size=7, shape='o',
                 fill='none', color='black')                     # ring around the point
      + annotate('segment', x=2.45, xend=1.99, y=880, yend=770,
                 color='black', size=0.4)                         # line to the point
      + annotate('text', x=2.6, y=900, label='KNM-ER 1470', size=10)
      + scale_color_manual(values=grade_colors)
      + scale_x_reverse(labels=lambda breaks: [f'{b:.1f} Ma' for b in breaks])
      + labs(x='Age', y='Endocranial volume (cm³)',
             color='Grade', shape='Grade', size='N estimates',
             title='Hominin brain size through time',
             caption='Source: Du et al. 2026')
      + theme_bw()
      + theme(axis_text=element_text(size=11),
              axis_title=element_text(size=12))
)
p9.save('ecv_vs_age_final.png', dpi=300, width=7, height=5)

# %% [markdown]
# Custom colors: The palette is readable with color blindness, and
# shape still separates the grades in grayscale. Tick labels: "2.0 Ma" shows
# the unit on the axis itself. Annotation: KNM-ER 1470 is a well-known
# specimen and gives readers a reference point. Caption: credits the data
# source. Larger fonts: stay readable when the figure is shrunk on a page.
# 300 dpi: the print standard for journals and theses.
# Audience: readers of a thesis or paper who know human evolution but have not
# seen this dataset.