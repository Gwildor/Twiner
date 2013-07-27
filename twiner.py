import ConfigParser
import io
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import Api
import models


def run():
    conf = ConfigParser.SafeConfigParser()
    with io.open('conf.ini', 'rb') as fd:
        conf.readfp(fd)

    try:
        db_url = conf.get('database', 'url')
    except ConfigParser.NoOptionError:
        if conf.get('database', 'type') == 'sqlite':
            db_url = 'sqlite://{0}'.format(conf.get('database', 'name'))
        else:
            db_url = '{0}://{1}:{2}@{3}/{4}'.format(
                conf.get('database', 'type'),
                conf.get('database', 'user'),
                conf.get('database', 'password'),
                conf.get('database', 'host'),
                conf.get('database', 'name')
            )

    engine = create_engine(db_url)
    models.Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    api = Api(conf.get('api', 'consumer_key'), conf.get('api',
                                                        'consumer_secret'))

if __name__ == '__main__':
    run()
