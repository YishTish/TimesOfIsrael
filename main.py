# Copyright 2018 Google LLC
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

# [START gae_python37_app]
import os
from flask import Flask, request, Response, send_from_directory,render_template
import TweetManager

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.

public_dir = os.path.join(os.getcwd(), "public/")
print("serving public files from: %s" % public_dir)
app = Flask(__name__, static_url_path=public_dir)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return send_from_directory("%s/html" % public_dir, "index.html")


@app.route("/search_tweets", methods=['GET'])
def search_tweets():
    term = request.values['term']
    tweets_array, word_count = TweetManager.run_tweets_search(term)
    headers = tweets_array.pop(0)
    return render_template("terms.html", term=term, tweet_count=len(tweets_array), headers=headers, tweets=tweets_array)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
