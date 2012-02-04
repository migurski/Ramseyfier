Ramseyfier
==========

Sometimes your shapefiles aren't good enough for GEOS: self-intersections, invalid
geometries, blah blah blah. The script ``find-errors.py`` will pass your shapefile
through PostGIS by way of ``shp2pgsql``, and spit out a list of whatever topology
errors it can find for you to fix.

Example usage:

    python find-errors.py stuff.shp pg_username pg_dbname

Results:

    stuff-errors.txt
    stuff-errors.shp
