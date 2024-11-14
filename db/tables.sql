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
    status INTEGER NULL,
    order_id INTEGER,
    type_queue INTEGER,
    registration_date TIMESTAMP NOT NULL,
    changed_date TIMESTAMP,
    insert_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    PRIMARY KEY (regnum, registration_date)
);