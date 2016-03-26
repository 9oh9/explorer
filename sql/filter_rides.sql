CREATE OR REPLACE FUNCTION filter_rides(text, int)
	RETURNS
	table(
		date_time text,
		latlng text
	)
	AS $$
	DECLARE

	poly geometry(POLYGON);

	BEGIN

		DROP TABLE IF EXISTS hells_kitchen;

		CREATE TEMPORARY TABLE
			hells_kitchen AS
				SELECT
					1 AS id,
					ST_GeomFromText($1, 4326) as polygon;

		CREATE INDEX hells_kitchen_idk ON hells_kitchen USING GIST (polygon);

		SELECT hk.polygon INTO poly FROM hells_kitchen hk WHERE hk.id = 1;

		IF $2 = 1 THEN

			RETURN QUERY SELECT
				r.pickup_time::TEXT,
				ST_AsGeoJson(r.pickup_latlng)
			FROM
				rides r
			WHERE
				ST_Within(r.pickup_latlng, poly)
			AND
				ST_Within(r.dropoff_latlng, poly);

		ELSE

			RETURN QUERY SELECT
				r.dropoff_time,
				ST_AsGeoJson(r.dropoff_latlng)
			FROM
				rides r
			WHERE
				ST_Covers(poly, r.dropoff_latlng) = true;
		END IF;

	END;

$$ LANGUAGE plpgsql;
