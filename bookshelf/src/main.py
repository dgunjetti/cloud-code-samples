# Copyright 2015 Google Inc.
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

import bookshelf
import config
import ptvsd
import os

# Note: debug=True is enabled here to help with troubleshooting. You should
# remove this in production.
app = bookshelf.create_app(config, debug=False)


# Make the queue available at the top-level, this allows you to run
# `psqworker main.books_queue`. We have to use the app's context because
# it contains all the configuration for plugins.
# If you were using another task queue, such as celery or rq, you can use this
# section to configure your queues to work with Flask.
with app.app_context():
    books_queue = bookshelf.tasks.get_books_queue()

# Set up debugger. Remove for production
debug_port = os.getenv('DEBUG_PORT', None)
if debug_port is not None:
    ptvsd.enable_attach(address=('0.0.0.0', debug_port))

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    server_port = os.getenv('SERVER_PORT', 8080)
    app.run(debug=False, port=server_port, host='0.0.0.0')
