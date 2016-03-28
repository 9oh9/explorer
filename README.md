# Explorer
Ride explorer.


## Architecture

The application is hosted in Amazon Web Services in a Virtual Private Cloud.  The application is
built on a PostgresSQL database.  Postgres was selected for its Geospatial support using the
PostGIS extension.  Data was transformed using a python script which compared the datetimes of
two records.  Setting the record with the earlier datetime as the pickup and the record with the
later datetime as the dropoff.

The api is written using Flask microframework written in python.  The application is deployed
using uwsgi wsgi server and proxied by nginx.  Database connections were made via the python
library psycopg2 which allowed for calls to the stored procedure used to retrieve data
completely contained by the polygon geography / geometric feature provided via the clients api
request.


## Database

As stated above Postgresql was selected for its Geospatial features through the PostGIS
extension.  The rides table contained four fields, timestamps for both pickup and dropoff as
well as pickup and dropoff geometry Point type fields representing the prospective pickup and
dropoff locations.  GIST indexes were added to both Point fields to improve query time.  This
index creates a bounding box for the geometric shape of the field in question. This allows for
faster intersection comparisons for Geospatial specific functions.  A stored procedure was
written to perform the select of contained Rides.  In order make the query as performant as
possible the following strategy was employed.  The POLYGON geometric feature is passed to the
stored procedure as a string. A temporary table is created to hold the value of the client
passed polygon.  The value of the polygon is then inserted into the temporary table and indexed
using a GIST index.  This was done to help postgis better compare the polygon against the ride
pickup / dropoff POINT fields when performing the ST_Within function.  The stored procedure
returns a table type object allowing the procedure call to be selected from as a table.


## API

The API is written using python 3.4 along with Flask, psycopg2 for database communications.
SQLAlchemy and GEOAlchemy2 were also considered for database / ORM features.  The anticipated
high latency of the spatial DB query against a large dataset steered the implementation toward a
simpler solution with psycopg2 that provided less overhead than that of an ORM.  A simple flask
extension was written to open and destroy database connection on each request context.  The
python package is itself set up with growth in mind.  The API code resides in its own module
directory.  The package has also been set up to easily create python execubles via setup.py for
jobs independent of the API (as is the case for the data transformation script / executable).
Data is returned from the API as JSON.  Specifically JSON compliant to the GeoJSON spec.
A universally supported geospatial data format.  This allows for seamless integration
onto the map upon return to the client.


## Client

The clientside application is built using ES6 javascript.  The JSPM (Javascript Packaage
Manager) is used to provide module support for all javascript module types (ES6, Commonjs,
etc).  It also served as the transpiler from ES6 javascript to the browser supported ES5.
AngularJS was selected to provide the foundation of the application as a single page clientside
application.  The application  made use of the Google Maps Javascript API for all map related
functionality.  In order to support the large number of data points needed to be plotted on the
map, WebGl was selected to plot Point features.  The large dataset pushed the implementation
away from other visualization tools such as D3.js for performance reasons related to the number
of DOM elements needed to visualize a large dataset with such libraries.  A library called
WebGLLayer that originated from google was used to add a WebGL enabled layer to the map.  It
also provided interfaces for integrating GeoJSON data directly onto the map.  Two libraries were
explored for realtime clientside data manipulation and disection.  The library JSTS which
provides a set of Spatial Related functions for comparing spatial related features on the client
was found to be possible opportunity for the expansion of clientside analysis tools.  Secondly
the library crossfilter developed by the payment processing company Square provided an awesome
and efficient way to explore subsets of data based on predefined dimensions (in this case date
ranges).  Crossfilter provides a way to give extremely dynamic exploration of large datasets
directly to the user.



## Bottlenecks and Proposed Improvements

The largest bottleneck is the latency necessary to run spatial queries against a large spatial
dataset.  Solving this problem while still maintaining the data's integrity can be a challenge
given the need for flexible queries from the user (user submitted polygon).  The best argument
for improving performance would be to shrink the dataset by removing redundant data via a
spatial clustering algorithm such as DBSCAN.  Clusters can provide clear insight into areas with
a high density of data.  In the case of this application implementing clusters can be difficult
given the unknown bounds of the users query.  Ie. clustering for a quite large space versus a
couple blocks should look drastically different given the proximity of the data and should be
taken into account when deriving the clusters.  Also to solve this in realtime would add
additional latency to the applicaiton and degrading the user's experience further.  For example
the popular python library scikitlearn has an implementation of dbscan and can take a second or
two to run against a large dataset.  This would suggest clustering data independent of the
existing Rides table and maintaining a clustered dataset in another data store.  Such an
operation would need to be performed regularly independent of the API (daemon, job, etc).
