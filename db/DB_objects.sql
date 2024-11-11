CREATE TABLE public.buffer_zone (
	buffer_zone_id serial4 NOT NULL,
	buffer_zone_name varchar(50) NULL,
	CONSTRAINT buffer_zone_pkey PRIMARY KEY (buffer_zone_id)
);

CREATE TABLE public.queue_length (
	id serial4 NOT NULL,
	buffer_zone int4 NULL,
	vehicle_count  int4 NULL,
	date_src timestamp NULL,
	insert_dt timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT queue_length_pkey PRIMARY KEY (id)
);

CREATE OR REPLACE VIEW public.vsl_lt_3_hrs
AS SELECT ql.insert_dt,
    bz.buffer_zone_name,
    ql.vehicle_count
   FROM queue_length ql
     JOIN buffer_zone bz ON ql.buffer_zone = bz.buffer_zone_id
  WHERE bz.buffer_zone_name::text = ANY (ARRAY['Kamenny Log'::character varying::text, 'Benyakoni'::character varying::text]) and
  		DATE_TRUNC('hour', insert_dt) >= DATE_TRUNC('hour', current_timestamp) - interval '3 hour'
  ORDER BY ql.insert_dt;
 
CREATE OR REPLACE VIEW public.vsl_lt_24_hrs
AS SELECT ql.insert_dt,
    bz.buffer_zone_name,
    ql.vehicle_count
   FROM queue_length ql
     JOIN buffer_zone bz ON ql.buffer_zone = bz.buffer_zone_id
  WHERE bz.buffer_zone_name::text = ANY (ARRAY['Kamenny Log'::character varying::text, 'Benyakoni'::character varying::text]) and
  		DATE_TRUNC('hour', insert_dt) >= DATE_TRUNC('hour', current_timestamp) - interval '24 hour'
  ORDER BY ql.insert_dt;
 
CREATE OR REPLACE VIEW public.vsl_lt_1_wk
AS SELECT ql.insert_dt,
    bz.buffer_zone_name,
    ql.vehicle_count
   FROM queue_length ql
     JOIN buffer_zone bz ON ql.buffer_zone = bz.buffer_zone_id
  WHERE bz.buffer_zone_name::text = ANY (ARRAY['Kamenny Log'::character varying::text, 'Benyakoni'::character varying::text]) and
  		insert_dt >= DATE_TRUNC('day', current_timestamp) - interval '6 day'
  ORDER BY ql.insert_dt;
 
CREATE OR REPLACE VIEW public.vsl_lt_1_mnth
AS SELECT ql.insert_dt,
    bz.buffer_zone_name,
    ql.vehicle_count
   FROM queue_length ql
     JOIN buffer_zone bz ON ql.buffer_zone = bz.buffer_zone_id
  WHERE bz.buffer_zone_name::text = ANY (ARRAY['Kamenny Log'::character varying::text, 'Benyakoni'::character varying::text]) and
  		insert_dt >= DATE_TRUNC('day', current_timestamp) - interval '30 day'
  ORDER BY ql.insert_dt;