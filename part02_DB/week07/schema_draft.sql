-- schema_draft.sql
-- Central Asian Genomic Database — Preliminary Schema
-- Week 7 Design Assignment

-- Archaeological sites where individuals were found
CREATE TABLE locality (
    locality_id     INTEGER PRIMARY KEY,
    site_name       TEXT NOT NULL,
    province        TEXT,
    modern_polity   TEXT NOT NULL,      -- present-day country
    latitude        REAL,               -- decimal degrees
    longitude       REAL                -- decimal degrees
);

-- Ancient individuals (AADR Master ID), with cultural and biological context
CREATE TABLE individual (
    individual_id         TEXT PRIMARY KEY NOT NULL,   -- e.g. I1234
    locality_id           INTEGER NOT NULL REFERENCES locality(locality_id),
    culture_name          TEXT,
    archaeological_period TEXT,
    date_mean_bp          INTEGER,     -- years before 1950
    verbatim_date         TEXT,        -- date exactly as published
    age_at_death          TEXT,        -- e.g. 'adult', '30-40'
    biological_sex        TEXT,        -- 'M' or 'F'
    y_haplogroup          TEXT CHECK (y_haplogroup IS NULL OR biological_sex = 'M'),  -- males only
    mt_haplogroup         TEXT
);

-- Genetic datasets (AADR Genetic ID); one individual can have several
CREATE TABLE genetic_sample (
    genetic_id               TEXT PRIMARY KEY NOT NULL,   -- e.g. I1234.SG
    individual_id            TEXT NOT NULL REFERENCES individual(individual_id),
    group_label              TEXT,                 -- population label used in analyses
    capture_method           TEXT NOT NULL,        -- '1240k capture', 'Twist capture', 'shotgun'
    udg_treatment            TEXT,                 -- 'none', 'half', 'full'
    snps_1240k               INTEGER,              -- number of 1240k SNPs covered
    qc_assessment            TEXT,                 -- 'PASS', 'QUESTIONABLE', 'FAIL'
    data_origin              TEXT NOT NULL,        -- 'internal' or 'external'
    publication_status       TEXT NOT NULL DEFAULT 'unpublished',   -- 'published' or 'unpublished'
    publication_abbreviation TEXT,
    created_at               TEXT DEFAULT CURRENT_TIMESTAMP,
    CHECK (data_origin = 'internal' OR publication_status = 'published')   -- external data is always published
);

-- Kinship between pairs of individuals; each pair is stored once
CREATE TABLE kinship (
    individual_id_1 TEXT NOT NULL REFERENCES individual(individual_id),
    individual_id_2 TEXT NOT NULL REFERENCES individual(individual_id),
    degree          INTEGER NOT NULL,   -- 1, 2, or 3
    relationship    TEXT,               -- e.g. 'siblings'
    PRIMARY KEY (individual_id_1, individual_id_2),
    CHECK (individual_id_1 < individual_id_2)
);
