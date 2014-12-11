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

def main():
	application = webapp.WSGIApplication([
		('/', MainHandler),
		('^/resume.*$', ResumeHandler),
		], debug=False)
	util.run_wsgi_app(application)

if __name__ == '__main__':
		main()
