Ramseyfier
==========

Sometimes your shapefiles aren't good enough for GEOS: self-intersections, invalid
geometries, blah blah blah. The script ``find-errors.py`` will pass your shapefile
through PostGIS by way of ``shp2pgsql``, and spit out a list of whatever topology
errors it can find for you to fix.

You will need run this tool iteratively. PostGIS will only return the first error it
finds, not all the invalid bits. Sorry, blame GEOS.


Example usage:

    python find-errors.py stuff.shp pg_username pg_dbname

Results:

    stuff-errors.txt
    stuff-errors.shp
    stuff-errors.dbf
    stuff-errors.shx
    
Assumptions
-----------

This has been built and tested for blessing Natural Earth data
(naturalearthdata.com). As such, windows-1252 codepage and a few other parameters 
are hard coded. Edit the .py file for your needs.