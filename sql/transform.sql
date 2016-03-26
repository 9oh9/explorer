CREATE OR REPLACE FUNCTION transform_data() RETURNS 
TABLE(id bigint, date_time timestamp, latlng geography(POINT), used int) AS $$
DECLARE

	end_date timestamp;
	rec RECORD;
	pair RECORD;
	num_hours bigint DEFAULT 1;

BEGIN

	CREATE TEMPORARY TABLE IF NOT EXISTS raw_ride_data(
		id bigint NOT NULL,
		date_time timestamp NOT NULL,
		latlng geography(POINT) NOT NULL,
		used int DEFAULT 0
	);

	CREATE TEMPORARY TABLE IF NOT EXISTS no_matches(
		id bigint NOT NULL,
		date_time timestamp NOT NULL,
		latlng geography(POINT) NOT NULL,
		used int DEFAULT 0
	);

	INSERT INTO
		raw_ride_data
	SELECT
		rpd.id,
		rpd.date_time,
		rpd.latlng,
		0 AS used
	FROM
		raw_pickup_data rpd
	ORDER BY rpd.id ASC
	LIMIT 1133582;

	CREATE INDEX raw_ride_comp_idx ON raw_ride_data(date_time, latlng, used, id);

	CREATE UNIQUE INDEX un_id_idx ON raw_ride_data(id);

	SELECT * INTO rec FROM raw_ride_data rrdh WHERE rrdh.used = 0 LIMIT 1;

	num_hours := 1;

	WHILE rec.id IS NOT NULL LOOP

		end_date := rec.date_time + interval '60 minute';
		num_hours = 1;

		SELECT
			*
		INTO
			pair
		FROM
			raw_ride_data rrdm
		WHERE
			rrdm.used = 0
		AND
			rrdm.id != rec.id
		AND
			rrdm.latlng != rec.latlng
		AND
			rrdm.date_time BETWEEN rec.date_time AND end_date;

		WHILE pair.id IS NULL LOOP

			end_date := end_date + interval '60 minute';
			num_hours := num_hours + 1;

			EXIT WHEN num_hours > 4;

			SELECT
				*
			INTO
				pair
			FROM
				raw_ride_data rrds
			WHERE
				rrds.used = 0
			AND
				rrds.id != rec.id
			AND
				rrds.latlng != rec.latlng
			AND
				rrds.date_time BETWEEN rec.date_time AND end_date;

		END LOOP;

		if pair.id IS NOT NULL THEN

			INSERT INTO rides (pickup_time, dropoff_time, pickup_latlng, dropoff_latlng) VALUES
					(rec.date_time, pair.date_time, rec.latlng, pair.latlng);

			UPDATE raw_ride_data rrda SET used=1 WHERE rrda.id = rec.id OR rrda.id = pair.id;

			SELECT * INTO rec FROM raw_ride_data rrdf WHERE rrdf.used = 0 LIMIT 1;

		ELSE

			INSERT INTO no_matches (id, date_time, latlng, used) VALUES
					(rec.id, rec.date_time, rec.latlng, 0);

			UPDATE raw_ride_data rrdg SET used=2 WHERE rrdg.id = rec.id OR rrdg.id = pair.id;

			SELECT * INTO rec FROM raw_ride_data rrdk WHERE rrdk.used = 0 LIMIT 1;

		END IF;

	END LOOP;

	RETURN QUERY SELECT * FROM raw_ride_data rrd WHERE rrd.used = 1 ORDER BY rrd.id DESC LIMIT 1;

END;
$$ LANGUAGE plpgsql;
