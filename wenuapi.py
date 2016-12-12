from eve import Eve
from eve_sqlalchemy import SQL
from wenuapi.influx_db_handler import InfluxDBHandler
from wenuapi.models.common import Base
import wenuapi.settings as settings
import wenuapi.auth as auth

app = Eve(data=SQL, settings=settings.SETTINGS, auth=auth.WenuBasicAuth)
#app = Eve(data=SQL, settings=settings.SETTINGS)
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base

if settings.use_influxdb:
    # Register influx for /measurements
    influx_handler = InfluxDBHandler(
        settings.influxdb_host,
        settings.influxdb_port,
        settings.influxdb_username,
        settings.influxdb_password,
        settings.influxdb_db,
        app,
    )
else:
    registerSchema(Measurement.__tablename__)(Measurement)
    settings.SETTINGS['DOMAIN']['measurement'] = Measurement._eve_schema['measurement']

#Base.metadata.drop_all(db.engine)
#Base.metadata.create_all(db.engine)

app.run(debug=True)
