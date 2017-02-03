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
import webapp2
import re
import cgi
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))


user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_re = re.compile(r"^.{3,20}$")
email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return username and user_re.match(username)

def valid_password(password):
    return password and password_re.match(password)

def valid_email(email):
    return not email or email_re.match(email)




class MainHandler(webapp2.RequestHandler):

    def get(self):

        template = jinja_env.get_template("form.html")
        content = template.render()
        self.response.write(content)

class SignUp(webapp2.RequestHandler):

    def post(self):

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        username = cgi.escape(username)
        password = cgi.escape(password)
        verify = cgi.escape(verify)
        email = cgi.escape(email)

        template = jinja_env.get_template("form.html")

        if not valid_username(username):
            error = "Please enter a valid username."
            error = cgi.escape(error)
            content = template.render(username=username, error1=error)
            self.response.write(content)

        elif not valid_password(password):
            error = "Please enter a valid password."
            error = cgi.escape(error)
            content = template.render(error2=error)
            self.response.write(content)

        elif password != verify:
            error = "Your passwords do not match."
            error = cgi.escape(error)
            content = template.render(error3=error)
            self.response.write(content)

        elif not valid_email(email):
            error = "That is not a valid email."
            error = cgi.escape(error)
            content = template.render(error4=error)
            self.response.write(content)

        else:
            self.response.write("Welcome, " + username)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignUp)
], debug=True)
