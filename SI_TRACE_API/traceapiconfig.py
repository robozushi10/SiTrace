#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.dont_write_bytecode = True

REST_URL = 'http://localhost:8000/api/v1/si/trace/svc/'

ACT_INT = {
  'Unknown'   : 0,
  'Initialize': 1,
  'Mark'      : 2,
  'Sweep'     : 3,
  'Stop'      : 4,
  'Finalize'  : 5,
  'Collect'   : 6,
}

DEFAULT_FILTER = {
  'limit'     : 5,
  'order'     : 1,
  'order_by'  : 2,
  'filterdata': 0,
}

