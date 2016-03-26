
CREATE TABLE IF NOT EXISTS raw_pickup_data(
	id bigserial NOT NULL,
	date_time timestamp with time zone DEFAULT NULL,
	latlng geography(POINT) DEFAULT NULL,
	base varchar(255) DEFAULT NULL,
	CONSTRAINT raw_primary_key PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS pickups(
	id bigserial NOT NULL,
	date_time timestamp with time zone DEFAULT NULL,
	lat double precision DEFAULT NULL,
	lng double precision DEFAULT NULL,
	base varchar(255) DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS rides(
	id bigserial NOT NULL,
	pickup_time timestamp with time zone DEFAULT NULL,
	dropoff_time timestamp with time zone DEFAULT NULL,
	pickup_latlng geography(POINT) DEFAULT NULL,
	dropoff_latlng geography(POINT) DEFAULT NULL,
	base varchar(255) DEFAULT NULL
)
