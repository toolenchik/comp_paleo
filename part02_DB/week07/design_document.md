# Central Asian Genomic Database — Preliminary Design Document
**Author:** Saida Tokmurzina
**Date:** October, 2026
**Domain:** Paleogenomics / ancient DNA population genetics
**Research context:** Population-genetic analysis of ancient human genomes from Central Asia, combining published data with our group's own newly generated, partly unpublished genomes.

---

## Mission Statement

The aim of the Central Asian Genomic Database is to track ancient human genomes for the purpose of understanding relationships between populations, migration patterns, and kinship. It brings together published genomes from external sources such as the AADR with [group name]'s own published and unpublished genomes, and serves [group name] researchers and their collaborators.

---

## Objectives

| # | Objective | Testable question | Query pattern |
|---|-----------|-------------------|---------------|
| 1 | Track genomic samples | List all genomic samples generated from a given individual | `WHERE individual_id = ?` |
| 2 | Manage the cultural context of each genomic sample | List all individuals from a given country with their site, culture, and date, oldest first | `JOIN locality WHERE modern_polity = ?` |
| 3 | Manage the biological context of each genomic sample | Find all individuals carrying a given Y-chromosome lineage | `WHERE y_haplogroup LIKE 'R1a%'` |
| 4 | Keep track of published and unpublished data | List all internal samples that are still unpublished | `WHERE data_origin = 'internal' AND publication_status = 'unpublished'` |
| 5 | Generate a supplementary table for a paper | List the samples reported in a given manuscript, with culture, date, sex, and coverage | `JOIN individual WHERE publication_abbreviation = ?` |
| 6 | Track kinship relationships between individuals | List all relatives of a given individual | `WHERE individual_id_1 = ? OR individual_id_2 = ?` |
| 7 | Assemble analysis-ready sample lists | List samples that pass QC with at least a minimum number of SNPs, as ID, sex, and group label | `WHERE qc_assessment = 'PASS' AND snps_1240k >= ?` |

### SQL sketches

**1. Track genomic samples:** all genomic samples generated from a given individual.

```sql
SELECT genetic_id, capture_method, snps_1240k, qc_assessment
FROM genetic_sample
WHERE individual_id = ?;
```

**2. Manage cultural context:** all individuals from a given country, oldest first.

```sql
SELECT i.individual_id, l.site_name, i.culture_name, i.date_mean_bp
FROM individual i
JOIN locality l ON i.locality_id = l.locality_id
WHERE l.modern_polity = ?
ORDER BY i.date_mean_bp DESC;          -- BP = years before 1950, so larger = older
```

**3. Manage biological context:** all individuals carrying a given Y-chromosome lineage.

```sql
SELECT individual_id, biological_sex, y_haplogroup, mt_haplogroup
FROM individual
WHERE y_haplogroup LIKE 'R1a%';        -- R1a and all its sub-lineages
```

**4. Keep track of published and unpublished data:** all internal samples that are still unpublished.

```sql
SELECT genetic_id, individual_id
FROM genetic_sample
WHERE data_origin = 'internal'
  AND publication_status = 'unpublished';
```

**5. Generate a supplementary table for a paper:** the samples reported in a given manuscript.

```sql
SELECT gs.genetic_id, i.culture_name, i.date_mean_bp,
       i.biological_sex, gs.snps_1240k
FROM genetic_sample gs
JOIN individual i ON gs.individual_id = i.individual_id
WHERE gs.publication_abbreviation = ?;
```

**6. Track kinship relationships:** all relatives of a given individual.

```sql
SELECT individual_id_1, individual_id_2, degree, relationship
FROM kinship
WHERE individual_id_1 = ? OR individual_id_2 = ?;   -- the person can be stored on either side of a pair
```

**7. Assemble analysis-ready sample lists:** samples that pass QC, as the three columns of an EIGENSTRAT `.ind` file.

```sql
SELECT gs.genetic_id, i.biological_sex, gs.group_label
FROM genetic_sample gs
JOIN individual i ON gs.individual_id = i.individual_id
WHERE gs.qc_assessment = 'PASS'
  AND gs.snps_1240k >= ?;              -- minimum SNPs covered, set per analysis
```

---

## Entities

| Entity | Justification | Example attributes |
|--------|--------------|-------------------|
| `locality` | A site exists whether or not anyone buried there has been sequenced, and it has its own name, coordinates, and modern political unit. One locality yields many individuals, so its facts are stored once instead of being repeated for every person. | `site_name`, `latitude`, `longitude`, `modern_polity` |
| `individual` | An ancient person (AADR Master ID) exists as an excavated, dated, culturally attributed skeleton before or without any sequencing. One individual can yield several genetic samples (for example I1234 and I1234.SG), and sex, haplogroups, cultural attribution, and date describe the person rather than any one dataset. | `age_at_death`, `y_haplogroup`, `culture_name` |
| `genetic_sample` | The central thing being tracked, as `fossils` is in OTB. Each genetic dataset (AADR Genetic ID) has its own identifier and properties that differ between datasets from the same person, so they cannot live in `individual`. A sample always comes from an individual, but that is a relationship (a foreign key), not a reason to merge the two tables. | `capture_method`, `snps_1240k`, `publication_status` |

### Subjects from the preliminary ERD that are not separate tables in this draft

| ERD subject | Where it goes | Why |
|-------------|---------------|-----|
| Cultural context | `culture_name`, `archaeological_period` in `individual`; `site_name` in `locality` | In this draft a culture has no attributes beyond its name, so it is a lookup value (controlled vocabulary), like `preparations` in OTB |
| Age | dating fields and `age_at_death` in `individual` | Dates and age at death describe the person |
| Biological data | sex and haplogroups in `individual`; SNP coverage in `genetic_sample` | "Max SNP coverage" is derived from other values, so it is not stored; "Relatives" holds several values and is replaced by the kinship relationship |
| Lab methods | `capture_method`, `udg_treatment`, `qc_assessment` in `genetic_sample` | Lookup values with no attributes of their own |
| Publication | `publication_status`, `data_origin`, `publication_abbreviation` in `genetic_sample` | Kept as fields while each sample is tied to one publication; the first candidate for a fourth entity |
| Source researcher | deferred | Passes the test (it has its own name, affiliation, and contact details), so it is the next entity to add when the design expands |
| Relationships (kinship) | `kinship` linking table, defined under Relationships | Kinship is a relationship between two individuals rather than a thing in its own right: a many-to-many relationship of `individual` with itself |

---

## Field Specifications

### Table: locality

| Field name | Data type | Required | Default | Notes |
|------------|-----------|----------|---------|-------|
| `locality_id` | INTEGER | YES (PK) | — | Surrogate key |
| `site_name` | TEXT | YES | — | Site name as published |
| `province` | TEXT | NO | — | Administrative region |
| `modern_polity` | TEXT | YES | — | Present-day country; controlled vocabulary |
| `latitude` | REAL | NO | — | Decimal degrees; NULL if not reported |
| `longitude` | REAL | NO | — | Decimal degrees; NULL if not reported |

### Table: individual

| Field name | Data type | Required | Default | Notes |
|------------|-----------|----------|---------|-------|
| `individual_id` | TEXT | YES (PK) | — | Natural key (e.g. I1234) |
| `locality_id` | INTEGER | YES | — | FK → `locality` |
| `culture_name` | TEXT | NO | — | Archaeological culture; controlled vocabulary |
| `archaeological_period` | TEXT | NO | — | Controlled vocabulary (Eneolithic, Bronze Age, …) |
| `date_mean_bp` | INTEGER | NO | — | Mean date in years before 1950; NULL if undated |
| `verbatim_date` | TEXT | NO | — | Date exactly as published |
| `age_at_death` | TEXT | NO | — | Osteological estimate ("adult", "30–40") |
| `biological_sex` | TEXT | NO | — | 'M' or 'F'; NULL if undetermined |
| `y_haplogroup` | TEXT | NO | — | Males only; NULL if female or undetermined |
| `mt_haplogroup` | TEXT | NO | — | NULL if undetermined |

### Table: genetic_sample

| Field name | Data type | Required | Default | Notes |
|------------|-----------|----------|---------|-------|
| `genetic_id` | TEXT | YES (PK) | — | Natural key (e.g. I1234, I1234.SG) |
| `individual_id` | TEXT | YES | — | FK → `individual` |
| `group_label` | TEXT | NO | — | Population label used in analyses (AADR Group ID) |
| `capture_method` | TEXT | YES | — | '1240k capture', 'Twist capture', or 'shotgun' |
| `udg_treatment` | TEXT | NO | — | 'none', 'half', or 'full'; NULL if unknown |
| `snps_1240k` | INTEGER | NO | — | SNPs covered; NULL until genotyped |
| `qc_assessment` | TEXT | NO | — | 'PASS', 'QUESTIONABLE', or 'FAIL' |
| `data_origin` | TEXT | YES | — | Internal/external status: 'internal' or 'external' |
| `publication_status` | TEXT | YES | 'unpublished' | 'published' or 'unpublished'; external data must be 'published' |
| `publication_abbreviation` | TEXT | NO | — | Paper or manuscript key; NULL if none yet |
| `created_at` | TEXT | NO | CURRENT_TIMESTAMP | Entry timestamp |

### Table: kinship (linking table)

| Field name | Data type | Required | Default | Notes |
|------------|-----------|----------|---------|-------|
| `individual_id_1` | TEXT | YES (PK) | — | FK → `individual` |
| `individual_id_2` | TEXT | YES (PK) | — | FK → `individual` |
| `degree` | INTEGER | YES | — | 1, 2, or 3 |
| `relationship` | TEXT | NO | — | e.g. 'siblings'; NULL if unresolved |

**Rules:** external data is always published; a Y haplogroup is recorded only for males; each kinship pair is stored once (`individual_id_1 < individual_id_2`).

---

## Relationships

| Relationship | Cardinality | Implementation |
|-------------|-------------|---------------|
| One locality → many individuals | 1:∞ | `individual.locality_id` → `locality.locality_id` |
| One individual → many genetic samples | 1:∞ | `genetic_sample.individual_id` → `individual.individual_id` |
| Many individuals ↔ many individuals (kinship) | ∞:∞ | Junction table `kinship`: `kinship.individual_id_1` → `individual.individual_id` and `kinship.individual_id_2` → `individual.individual_id` |

---

## Key Choices

locality uses an auto-assigned INTEGER key (locality_id) because site names can vary or repeat, and coordinates can change. individual and genetic_sample use existing AADR Master IDs and Genetic IDs (e.g. I1234, I1234.SG) as TEXT keys, keeping them consistent with lab records and genotype files. The kinship table handles the many-to-many links between individuals, using both IDs as a composite primary key. Each pair appears once, with the smaller ID first. Foreign keys match the names and types of the primary keys they reference.
