CREATE TABLE public.buffer_zone (
	buffer_zone_id serial4 NOT NULL,
	buffer_zone_name varchar(50) NULL,
	CONSTRAINT buffer_zone_pkey PRIMARY KEY (buffer_zone_id)
);

CREATE TABLE queue_length_all (
	row_id serial4 NOT NULL,
	buffer_zone_id INTEGER,
    count_all INTEGER,
    count_car INTEGER,
    count_truck INTEGER,
    count_bus INTEGER,
    count_motorcycle INTEGER,
    count_live_queue INTEGER,
    count_bookings INTEGER,
    count_priority INTEGER,
    count_passed_scc INTEGER,
    insert_dt timestamp DEFAULT CURRENT_TIMESTAMP NULL
);

CREATE TABLE public.buffer_zone_statistics (
	id serial4 NOT NULL,
	buffer_zone_id int4 NULL,
	native_id int4 NULL,
	checkpoint_id uuid NULL,
	car_last_hour int4 NULL,
	motorcycle_last_hour int4 NULL,
	truck_last_hour int4 NULL,
	bus_last_hour int4 NULL,
	car_last_day int4 NULL,
	truck_last_day int4 NULL,
	bus_last_day int4 NULL,
	motorcycle_last_day int4 NULL,
	insert_dt timestamp DEFAULT CURRENT_TIMESTAMP NULL
);

CREATE TABLE public.car_live_queue (
    row_id serial4 NOT NULL,
    buffer_zone_id INTEGER NOT NULL,
    regnum VARCHAR(10) NOT NULL,
    status INTEGER NOT NULL,
    order_id INTEGER,
    type_queue INTEGER,
    registration_date TIMESTAMP,
    changed_date TIMESTAMP,
    insert_dt timestamp DEFAULT CURRENT_TIMESTAMP NULL,
    PRIMARY KEY (regnum, registration_date)
);

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