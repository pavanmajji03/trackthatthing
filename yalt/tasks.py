import os
import datetime

import webapp2
from google.appengine.ext import db

from models import Location

# are we on the cloud or a local dev server:
is_dev_server = os.environ['SERVER_SOFTWARE'].startswith('Dev')


class CleanUp(webapp2.RequestHandler):
    def get(self):
        print 'hello, world'
        limit = 1000
        if 'limit' in self.request.arguments():
            limit = int(self.request.get('limit'))

        one_week_ago = datetime.datetime.now() - datetime.timedelta(7,0,0)
        lq = db.GqlQuery('SELECT __key__ FROM Location WHERE date < :1', one_week_ago)

        db.delete(lkey for lkey in lq.fetch(limit))

        print 'finished cleaning up stuff older than a week'

url_spec = [('/tasks/cleanup', CleanUp)]

application = webapp2.WSGIApplication(
    url_spec,
    debug=is_dev_server)