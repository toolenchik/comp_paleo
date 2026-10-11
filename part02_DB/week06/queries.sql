-- queries.sql
-- OTB Fossil Database Queries
-- Week 6 Assignment

-- ── Query 1 ───────────────────────────────────────────────────────────────────
-- Question: How many fossil specimens are in the database?
-- What it does: Counts every row in the fossils table, b/c one row = one specimen.
-- Paleo importance: tells me how large the OTB hominin sampleset is
SELECT COUNT(*) AS total_specimens
FROM fossils;

-- ── Query 2 ───────────────────────────────────────────────────────────────────
-- Question: Which specimens were discovered by Kamoya Kimeu?

-- Returns catalog number, element type, and year for every fossil
-- where discovered_by field contains 'Kimeu'. The % wildcards are needed b/c 'Kimeu'
-- is recorded in other forms. Results are ordered by year in acsending order, catalog_number is a tiebreaker.

-- Tells as what specimens were discovered by Kimeu, noting that KNM-WT 15000 was one 
-- of the biggest findings in Paleoanthropology

SELECT catalog_number,
       preparations,
       year
FROM fossils
WHERE discovered_by LIKE '%Kimeu%'
ORDER BY year ASC, catalog_number;

-- ── Query 3 ───────────────────────────────────────────────────────────────────
-- Question: How many specimens come from each formation?

-- Joins each fossil to its locality, groups the
-- rows by formation, and counts the specimens in each group, with
-- the most productive formation on the top.

-- Tells us which formations yielded the most hominin fossils. This shows where
-- the record is concentrated.

SELECT l.formation,
       COUNT(*) AS specimen_count
FROM fossils f
JOIN localities l ON f.locality_id = l.locality_id
GROUP BY l.formation
ORDER BY specimen_count DESC;

-- ── Query 4 ───────────────────────────────────────────────────────────────────
-- Question: Which specimens are older than 3 million years?

-- Joins fossils to taxa and to localities, keeps only fossils whose earliest_chronometric_age 
-- is >3.0 Ma,lists them oldest first.

-- Tells us which hominins are present in the Miocene and  Pliocene, like Lothagam teeth 
-- and A. anamensis.

SELECT f.catalog_number,
       t.scientific_name,
       f.earliest_chronometric_age,
       l.formation
FROM fossils f
JOIN taxa t       ON f.taxon_id    = t.taxon_id
JOIN localities l ON f.locality_id = l.locality_id
WHERE f.earliest_chronometric_age > 3.0
ORDER BY f.earliest_chronometric_age DESC, f.catalog_number;


-- ── Query 5 ───────────────────────────────────────────────────────────────────
-- Question: Which taxon has the most specimens, and what anatomical
-- elements are most commonly preserved for that taxon?

-- (a) Joins fossils to taxa, groups by scientific_name, and returns
-- only the name of the highest specimen count (LIMIT 1).

SELECT t.scientific_name,
       COUNT(*) AS specimen_count
FROM fossils f
JOIN taxa t ON f.taxon_id = t.taxon_id
GROUP BY t.scientific_name
ORDER BY specimen_count DESC
LIMIT 1;

-- (b) For the taxon in (a), counts specimens by preparations in descending order
-- The subquery in the WHERE is query (a).

-- "Hominini" occurs more often than other taxons, many elements limit 
-- identification to genus or species.

SELECT f.preparations,
       COUNT(*) AS specimen_count
FROM fossils f
JOIN taxa t ON f.taxon_id = t.taxon_id
WHERE t.scientific_name = (
    SELECT t2.scientific_name
    FROM fossils f2
    JOIN taxa t2 ON f2.taxon_id = t2.taxon_id
    GROUP BY t2.scientific_name
    ORDER BY COUNT(*) DESC
    LIMIT 1
)
GROUP BY f.preparations
ORDER BY specimen_count DESC;

