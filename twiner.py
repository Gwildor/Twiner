import datetime
import ConfigParser
import io
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api import Api
import models


def run(path_to_conf='conf.ini'):
    conf = ConfigParser.SafeConfigParser()
    with io.open(path_to_conf, 'rb') as fd:
        conf.readfp(fd)

    params = {}
    for key, val in conf.items('params'):
        if key in ['trim_user', 'exclude_replies', 'contributor_details',
                   'include_rts']:
            params[key] = int(conf.getboolean('params', key))
        else:
            params[key] = val

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

    for tl in session.query(models.Timeline):

        if not tl.last_update or datetime.datetime.now() >= tl.last_update + tl.interval:

            last_tweet = tl.tweets.order_by(models.Tweet.id.desc()).first()
            if last_tweet:
                params['since_id'] = last_tweet.id
            elif 'since_id' in params:
                del params['since_id']

            tweets = api.get_user_timeline(params=params,
                                           screen_name=tl.screen_name)
            for tweet in tweets:
                if not session.query(models.Tweet).get(tweet['id']):
                    tl.tweets.append(models.Tweet(tweet))

            tl.last_update = datetime.datetime.now()

    session.commit()

if __name__ == '__main__':
    run()
