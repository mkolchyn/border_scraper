CREATE OR REPLACE FUNCTION get_queue_speed(buffer_zone_id_param INTEGER)
RETURNS TABLE (
    queue_speed float
) AS $$
BEGIN
    RETURN QUERY 
    WITH time_diff_count_ini AS (
        SELECT 
            regnum,
			changed_date,
			registration_date,
		CASE 
			WHEN extract(day from changed_date) > extract(day from registration_date) then
				round (((60 - extract(minute from registration_date)) + (24 - (extract(hour from registration_date)+1))*60 +
				extract(hour from changed_date)*60 + extract(minute from changed_date))/60,2)
			ELSE 
				ROUND((EXTRACT(hour FROM (changed_date - registration_date)) * 60 + EXTRACT(minute FROM (changed_date - registration_date))) / 60, 2)
		END AS time_diff,
            count_car
        FROM car_live_queue clq 
        JOIN queue_length_all qla ON 
            clq.buffer_zone_id = qla.buffer_zone_id AND 
            DATE_TRUNC('minute', registration_date) - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM registration_date) % 10) = DATE_TRUNC('minute', qla.insert_dt) + '01:00:00'::interval
        WHERE clq.buffer_zone_id = buffer_zone_id_param
        ORDER BY clq.insert_dt DESC
    ) 
    SELECT 
        CASE 
            WHEN time_diff >= 1 THEN CAST(ROUND(count_car / time_diff,2) AS float)
        END AS queue_speed
    FROM time_diff_count_ini
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_car_origin(buffer_zone_id_param INTEGER)
RETURNS TABLE (
    regnum VARCHAR(10),
    country TEXT,
    city TEXT,
    insert_dt TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
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
    WHERE clq.buffer_zone_id = buffer_zone_id_param;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_car_origin_ratio(buffer_zone_id_param INTEGER)
RETURNS TABLE (
    insert_dt TIMESTAMP,
    ratio_by_to_other TEXT
) AS $$
BEGIN
    RETURN QUERY
    WITH counts AS (
        SELECT 
            gco.country,
            gco.insert_dt,
            COUNT(gco.regnum) AS cnt
        FROM get_car_origin(buffer_zone_id_param) gco
        GROUP BY gco.insert_dt, gco.country
    ),
    ratios AS (
        SELECT 
            c.insert_dt,
            SUM(CASE WHEN c.country = 'by' THEN c.cnt ELSE 0 END) AS by_count,
            SUM(CASE WHEN c.country = 'other' THEN c.cnt ELSE 0 END) AS other_count
        FROM counts c
        GROUP BY c.insert_dt
    )
    SELECT 
        r.insert_dt,
		CONCAT(ROUND(r.by_count / (r.by_count + r.other_count) * 100, 2), '%') AS ratio_by_to_other
    FROM ratios r;
END;
$$ LANGUAGE plpgsql;