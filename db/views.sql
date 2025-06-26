CREATE OR REPLACE VIEW public.vsl_lt_1_mnth
AS SELECT qla.insert_dt,
    bz.buffer_zone_name,
    qla.count_car
  FROM queue_length_all qla
     JOIN buffer_zone bz ON qla.buffer_zone_id = bz.buffer_zone_id
  WHERE (bz.buffer_zone_name::text = ANY (ARRAY['Kamenny Log'::character varying::text, 'Benyakoni'::character varying::text])) AND qla.insert_dt >= (date_trunc('day'::text, CURRENT_TIMESTAMP) - '30 days'::interval)
  ORDER BY qla.insert_dt DESC;
  
CREATE OR REPLACE VIEW public.vsl_lt_1_wk
AS SELECT qla.insert_dt,
    bz.buffer_zone_name,
    qla.count_car
  FROM queue_length_all qla
     JOIN buffer_zone bz ON qla.buffer_zone_id = bz.buffer_zone_id
  WHERE (bz.buffer_zone_name::text = ANY (ARRAY['Kamenny Log'::character varying::text, 'Benyakoni'::character varying::text])) AND qla.insert_dt >= (date_trunc('day'::text, CURRENT_TIMESTAMP) - '6 days'::interval)
  ORDER BY qla.insert_dt DESC;
  
CREATE OR REPLACE VIEW public.vsl_lt_24_hrs
AS SELECT qla.insert_dt,
    bz.buffer_zone_name,
    qla.count_car
   FROM queue_length_all qla
     JOIN buffer_zone bz ON qla.buffer_zone_id = bz.buffer_zone_id
  WHERE (bz.buffer_zone_name::text = ANY (ARRAY['Kamenny Log'::character varying::text, 'Benyakoni'::character varying::text])) AND date_trunc('hour'::text, qla.insert_dt) >= (date_trunc('hour'::text, CURRENT_TIMESTAMP) - '24:00:00'::interval)
  ORDER BY qla.insert_dt;

CREATE OR REPLACE VIEW public.vsl_lt_3_hrs
AS SELECT qla.insert_dt,
    bz.buffer_zone_name,
    qla.count_car
   FROM queue_length_all qla
     JOIN buffer_zone bz ON qla.buffer_zone_id = bz.buffer_zone_id
  WHERE (bz.buffer_zone_name::text = ANY (ARRAY['Kamenny Log'::character varying::text, 'Benyakoni'::character varying::text])) AND date_trunc('hour'::text, qla.insert_dt) >= (date_trunc('hour'::text, CURRENT_TIMESTAMP) - '03:00:00'::interval)
  ORDER BY qla.insert_dt;

CREATE OR REPLACE VIEW vsl_all_car_origin_ratio AS 
WITH car_origin_by_country AS (
    SELECT 
        buffer_zone_name,
        clq.regnum,
        CASE 
            WHEN clq.regnum ~ '^\d{4}[A-Z]{2}\d{1}$' THEN 'by'
            ELSE 'other'
        END AS country,
        CASE 
            WHEN clq.regnum ~ '^\d{4}[A-Z]{2}\d{1}$' AND clq.regnum ~ '1$' THEN 'Brest'
            WHEN clq.regnum ~ '^\d{4}[A-Z]{2}\d{1}$' AND clq.regnum ~ '2$' THEN 'Vitebsk'
            WHEN clq.regnum ~ '^\d{4}[A-Z]{2}\d{1}$' AND clq.regnum ~ '3$' THEN 'Gomel'
            WHEN clq.regnum ~ '^\d{4}[A-Z]{2}\d{1}$' AND clq.regnum ~ '4$' THEN 'Grodno'
            WHEN clq.regnum ~ '^\d{4}[A-Z]{2}\d{1}$' AND clq.regnum ~ '6$' THEN 'Mogilev'
            WHEN clq.regnum ~ '^\d{4}[A-Z]{2}\d{1}$' AND clq.regnum ~ '5$' THEN 'Minsk'
            WHEN clq.regnum ~ '^\d{4}[A-Z]{2}\d{1}$' AND clq.regnum ~ '7$' THEN 'Minsk'
            ELSE 'other'
        END AS city,
        DATE_TRUNC('day', clq.insert_dt) AS insert_dt
    FROM car_live_queue clq 
    JOIN buffer_zone bz USING(buffer_zone_id)
),
counts AS (
    SELECT 
        gco.buffer_zone_name,
        gco.country,
        gco.insert_dt,
        COUNT(gco.regnum) AS cnt
    FROM car_origin_by_country gco
    GROUP BY gco.insert_dt, gco.country, gco.buffer_zone_name
),
ratios AS (
    SELECT 
        c.buffer_zone_name,
        c.insert_dt::date,
        SUM(CASE WHEN c.country = 'by' THEN c.cnt ELSE 0 END) AS by_count,
        SUM(CASE WHEN c.country = 'other' THEN c.cnt ELSE 0 END) AS other_count
    FROM counts c
    GROUP BY c.insert_dt, c.buffer_zone_name
)
SELECT 
    r.buffer_zone_name,
    r.insert_dt,
    CASE 
        WHEN (r.by_count + r.other_count) > 0 THEN ROUND(r.by_count / (r.by_count + r.other_count) * 100, 2)
        ELSE 0 
    END AS "ratio_BY_to_other"
FROM ratios r;