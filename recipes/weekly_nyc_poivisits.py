from _helper import aws

query = """
WITH daily_visits AS(
SELECT safegraph_place_id, location_name, poi_cbg, date_add('day', row_number() over(), date_start) AS date_current, CAST(visits AS SMALLINT) as visits
FROM (
  SELECT
     safegraph_place_id,
     location_name,
     poi_cbg,
     CAST(SUBSTR(date_range_start, 1, 10) AS DATE) as date_start,
     CAST(SUBSTR(date_range_end, 1, 10) AS DATE) as date_end,
     cast(json_parse(visits_by_day) as array<varchar>) as a
  FROM safegraph.monthly_patterns
  WHERE SUBSTR(poi_cbg,1,5) IN ('36085','36081','36061','36047','36005')
) b
CROSS JOIN UNNEST(a) as t(visits)
)

SELECT
   CAST(EXTRACT(year from a.date_current) AS VARCHAR)||'-'||LPAD(CAST(EXTRACT(week from a.date_current) AS VARCHAR),2,'0') as year_week,
   a.location_name as poi,
   b.street_address as address,
   a.poi_cbg,
   b.naics_code,
   SUM(CASE WHEN EXTRACT(dow from a.date_current) NOT IN (0, 6) THEN visits END) as visits_weekday,
   SUM(CASE WHEN EXTRACT(dow from a.date_current) IN (0, 6) THEN visits END) as visits_weekend,
   SUM(a.visits) as visits_daily,
   b.latitude,
   b.longitude
FROM daily_visits a
LEFT JOIN (
      SELECT distinct safegraph_place_id, naics_code, street_address, latitude, longitude
      FROM "safegraph"."core_poi"
      WHERE region = 'NY'
    ) b  
    ON a.safegraph_place_id=b.safegraph_place_id
GROUP BY EXTRACT(year from a.date_current), 
         EXTRACT(week from a.date_current), 
         a.location_name, 
         b.naics_code,
         a.poi_cbg,
         b.street_address,
         b.latitude,
         b.longitude
"""

aws.execute_query(
    query=query, 
    database="safegraph", 
    output="output/poi/weekly_nyc_poivisits.csv"
)