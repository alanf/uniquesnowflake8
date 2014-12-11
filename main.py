#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import httplib
import os
import sys

import config
from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class BaseHandler(webapp.RequestHandler):
	template_path = ''
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'templates', self.template_path)
		self.response.out.write(template.render(path, {}))

class MainHandler(BaseHandler):
	template_path = 'index.html'

class ResumeHandler(BaseHandler):
	template_path = 'resume.html'

class JenHandler(BaseHandler):
	template_path = 'jen.html'

class DogSpottingHandler(BaseHandler):
	template_path = 'dog_spotting.html'

	def compute_score(self, tweet_text):
		if '#dogspot' not in tweet_text:
			return 0

		result = 0
		for keyword, point_value in config.scoring_keywords.iteritems():
			if keyword in tweet_text:
				result += point_value
		return result
		
	def get(self):
		context = {'users': []}
		connection = httplib.HTTPConnection(config.twitter_api_host)
		for user_id in config.users:
			user_results = {'id': user_id, 'tweets': []}
			context['users'].append(user_results)
			
			# get all the tweets for a user
			url = config.twitter_timeline_url % {'id': user_id}
			connection.request('GET', url)
			response = json.loads(connection.getresponse().read())

			for tweet in response:
				if not isinstance(tweet, dict):
					break
			
				user_results.update(tweet['user'])
				# calculate its value
				tweet_text = tweet['text']
				tweet_score = self.compute_score(tweet_text)
				tweet_create_date = ' '.join(tweet['created_at'].split()[:4])
				# todo: store all this
				user_results['tweets'].append({
					'text': tweet_text,
					'score': tweet_score,
					'create_date': tweet_create_date,
				})
				
		context['locals'] = locals()
		path = os.path.join(os.path.dirname(__file__), 'templates', self.template_path)
		self.response.out.write(template.render(path, context))

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('^/resume.*$', ResumeHandler),
		('^/jen.*$', JenHandler),
		('^/dogspotting.*$', DogSpottingHandler),
	], debug=False)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()
