from sys import argv
from subprocess import Popen, PIPE
from os.path import basename, splitext
from tempfile import mkstemp
from os import remove
from re import compile

if __name__ == '__main__':

    shapefile, pg_user, pg_dbname = argv[1:]
    handle, table = mkstemp(prefix='shapefile_')
    
    print basename(table)
    
    shp2pgsql = Popen('shp2pgsql -dID -W Windows-1252'.split() + [shapefile, basename(table)], stdout=PIPE)
    psql = Popen('psql -U'.split() + [pg_user, pg_dbname], stdin=shp2pgsql.stdout)
    
    shp2pgsql.wait()
    psql.wait()
    
    prefix, suffix = splitext(shapefile)
    badshapes = prefix + '-errors' + suffix
    
    pgsql2shp = Popen(['pgsql2shp', '-f', badshapes, '-u', pg_user, pg_dbname, 'SELECT * FROM %s WHERE NOT ST_IsValid(the_geom)' % basename(table)], stderr=PIPE)
    pgsql2shp.wait()
    
    errors = pgsql2shp.stderr.read()
    error_pat = compile(r'\bat or near point (-?\d+\.\d+) (-?\d+\.\d+)\b')
    
    print badshapes
    
    psql = Popen(['psql', '-U', pg_user, pg_dbname], stdin=PIPE)
    psql.stdin.write('DROP TABLE %s' % basename(table))
    psql.stdin.close()
    psql.wait()
    
    remove(table)
    
    errorfile = prefix + '-errors.txt'
    errorfile = open(errorfile, 'w')
    
    print >> errorfile, 'longitude\tlatitude'
    
    for (lon, lat) in error_pat.findall(errors):
        print >> errorfile, '%(lon)s\t%(lat)s' % locals()
