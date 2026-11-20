-- Working copies of the layers this project uses
DROP TABLE IF EXISTS raw.pipelines, raw.wells;

CREATE TABLE raw.pipelines AS SELECT * FROM raw.pipe_pipe389l;
CREATE TABLE raw.wells     AS SELECT * FROM raw.well_well389s;

-- Stable IDs for joins and QA reporting
ALTER TABLE raw.pipelines ADD COLUMN seg_id  serial PRIMARY KEY;
ALTER TABLE raw.wells     ADD COLUMN well_pk serial PRIMARY KEY;

-- Spatial indexes make distance/intersection queries fast
CREATE INDEX pipelines_gix ON raw.pipelines USING gist (geom);
CREATE INDEX wells_gix     ON raw.wells     USING gist (geom);
CREATE INDEX county_gix    ON raw.county    USING gist (geom);
ANALYZE;
