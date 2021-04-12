#  Copyright 2020 Board of Trustees of the University of Illinois.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('name'):
            return redirect(url_for('contribute.login'))
        return view(**kwargs)
    return wrapped_view
