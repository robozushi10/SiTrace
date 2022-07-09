#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--
# https://qiita.com/FGtatsuro/items/0efebb9b58374d16c5f0
# % pytest test_trace_api.py
# % pytest -v --capture=no test_trace_api.py
# % cat setup.cfg
# [tool:pytest]
# addopts = -v --capture=no
# timeout = 5

import sys; sys.dont_write_bytecode = True
import os, json, time, copy, requests, textwrap, socket, pickle, base64, sh
from datetime import datetime
from pprint import pprint
import trace_api as sitrace

dc = {
  "uuid": "AutoRelease_{0}".format(sh.bash("-c", 'date +"%Y%m%d-%H%M%S"')),
  "service": "AutoRelease",
}

def etest_INIT():
  assert sitrace.SI_TRACE_INITIALIZE(dc) == True


def test_INIT_2_MARK_2_MARK():
  rc = sitrace.SI_TRACE_INITIALIZE(dc)
  if rc:
    dc['markid'] = 'setup'
    dc['tags'] = ['A1','B1','C1']
    rc = sitrace.SI_TRACE_MARK(dc) 
    assert rc == True
  if rc:
    dc['markid'] = 'setup'
    dc['tags'] = ['A2','B2','C2']
    rc = sitrace.SI_TRACE_MARK(dc) 
    assert rc == True
  return rc

def test_INIT_2_MARK_2_SWEEP():
  rc = sitrace.SI_TRACE_INITIALIZE(dc)
  if rc:
    dc['markid'] = 'setup'
    dc['tags'] = ['A1','B1','C1']
    rc = sitrace.SI_TRACE_MARK(dc) 
    assert rc == True
  if rc:
    dc['markid'] = 'setup'
    dc['tags'] = ['A1','B1','C1']
    rc = sitrace.SI_TRACE_SWEEP(dc) 
    assert rc == True
  return rc


def test_INIT_2_MARK_2_SWEEP_SWEEP_SWEEP_2_STOP():
  rc = sitrace.SI_TRACE_INITIALIZE(dc)
  if rc:
    dc['markid'] = 'setup'
    dc['tags'] = ['A1','B1','C1']
    rc = sitrace.SI_TRACE_MARK(dc) 
    assert rc == True
  if rc:
    dc['markid'] = 'setup'
    dc['tags'] = ['A1']
    print(['A1'])
    print(type(['A1']))
    pprint(dc['tags'])
    rc = sitrace.SI_TRACE_SWEEP(dc) 
    assert rc == True
  if rc:
    dc['markid'] = 'setup'
    rc = sitrace.SI_TRACE_STOP(dc)
    assert rc == True
  return rc


def test_INIT_2_MARK_2_SWEEP_SWEEP_SWEEP_2_STOP_FIN_COLLECT():
  rc = sitrace.SI_TRACE_INITIALIZE(dc)
  dc['markid'] = 'setup'
  if rc:
    dc['tags'] = ['A1','B1','C1']
    rc = sitrace.SI_TRACE_MARK(dc) 
    assert rc == True
  if rc:
    dc['tags'] = ['A1']
    print(['A1'])
    print(type(['A1']))
    pprint(dc['tags'])
    rc = sitrace.SI_TRACE_SWEEP(dc) 
    assert rc == True
  if rc:
    rc = sitrace.SI_TRACE_STOP(dc)
    assert rc == True
  if rc:
    rc = sitrace.SI_TRACE_FINALIZE(dc)
    assert rc == True
  if rc:
    filter = {
      'limit':    10, # 10 件
      'order':     1, # 昇順
      'order_by':  2, # last_at
      'mevent':    2, # 異常のみ
    }
    rc, gc = sitrace.SI_TRACE_COLLECT(dc, filter)
    assert rc == True
  return rc


if __name__ == '__main__':

  pass

