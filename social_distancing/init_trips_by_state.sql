CREATE TABLE IF NOT EXISTS sg_trips_by_state (
    year_week text,
    state text,
    to_nyc int,
    from_nyc int,
    net_nyc int,
    state_geom geometry(Geometry,4326)
);

CREATE TABLE IF NOT EXISTS state_days_included (
    year_week text,
    date text
);