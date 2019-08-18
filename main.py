#!/usr/bin/env python3.7

import waitress
from backend import app


waitress.serve(app, listen='*:8008')
