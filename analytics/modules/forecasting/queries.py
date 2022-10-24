get_locations_by_cluster="""
--begin-sql
    SELECT
        hp.latitud AS lat,
        hp.longitud AS lng,
        CAST(hp.fecha as DATE) AS date,
        CAST(hp.fecha as TIME) AS time,
        ST_Distance_Sphere(
            point({lng},{lat}),
            point(hp.longitud,hp.latitud)
            ) AS distance
    FROM hurto_personas as hp
    WHERE  ST_Distance_Sphere(
            point(-75.5662,6.25092),
            point(hp.longitud,hp.latitud)
            ) <= {radius}
    ORDER BY date;
"""