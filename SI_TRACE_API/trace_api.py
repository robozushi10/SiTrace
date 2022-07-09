#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys; sys.dont_write_bytecode = True
import os, json, time, copy, requests, textwrap, socket, pickle, base64, sh
from datetime import datetime
from pprint import pprint
import traceapiconfig as cfg  # configuration for this program

from logging import basicConfig, getLogger, DEBUG, ERROR
basicConfig(level=ERROR)      # これはメインのファイルにのみ書く
logger = getLogger(__name__)  # これはすべてのファイルに書く

class SiTrace:
  """
  非公開クラス
  クラスにする必要はなかったが、処理をまとめておきたかったのでクラスにしている.
  """
  def __init__(self):
    self.URL    = cfg.REST_URL
    self.ACTs   = cfg.ACT_INT
    self.FILTER = cfg.DEFAULT_FILTER
    pass


  def copy_base_payload(self, ud, role):
    """ pay のうち、必ず通知するパラメータを複製する """
    core            = {}
    core['uuid']    = ud['uuid']
    core['service'] = ud['service']   if 'service' in ud else None
    core['host']    = ud['host']      if 'host'    in ud else sh.bash("-c", "hostname")
    core['ip']      = ud['ip']        if 'ip'      in ud else sh.bash("-c", "hostname -I | cut -f1 -d' '")
    core['actid']   = self.ACTs[role]
    core['active']  = True
    return core


  def to_ser(self, des):
    """ convert the object (ex. list, dict) -> bytes """
    bytes = pickle.dumps(des)
    ser = base64.b64encode(bytes)
    return ser


  def to_des(self, ser):
    """ convert the bytes to object (ex. list, dict) """
    bytes = base64.b64decode(ser)
    des = pickle.loads(bytes)
    return des


  def initialize(self, ud):
    if(not 'uuid' in ud) or (not ud['uuid']):
      return False
    if(not 'service' in ud) or (not ud['service']):
      return False
    pay = self.copy_base_payload(ud, 'Initialize')
    res = requests.post(self.URL, pay)
    return True if res.status_code == 201 else False


  def mark(self, ud):
    if(not 'uuid' in ud) or (not ud['uuid']):
      return False
    if(not 'markid' in ud) or (not ud['markid']):
      return False
    pay = self.copy_base_payload(ud, 'Mark')
    pay['markid'] = self.to_ser(ud['markid']) if 'markid' in ud else None
    pay['tags']   = self.to_ser(ud['tags'])   if 'tags'   in ud else None
    pay['file']   = ud['file']                if 'file'   in ud else None
    pay['cls']    = ud['cls']                 if 'cls'    in ud else None
    pay['func']   = ud['func']                if 'func'   in ud else None
    pay['verb']   = self.to_ser(ud['verb'])   if 'verb'   in ud else None
    pay['wkr']    = ud['wkr']                 if 'wkr'    in ud else None
    res = requests.post(self.URL, pay)
    return True if res.status_code == 201 else False


  def sweep(self, ud):
    if(not 'uuid' in ud) or (not ud['uuid']):
      return
    if(not 'markid' in ud) or (not ud['markid']):
      return
    pay = self.copy_base_payload(ud, 'Sweep')
    pay['markid'] = self.to_ser(ud['markid']) if 'markid' in ud else None
    pay['tags']   = self.to_ser(ud['tags'])   if 'tags'   in ud else None
    res = requests.post(self.URL, pay)
    return True if res.status_code == 201 else False


  def stop(self, ud):
    if(not 'uuid' in ud) or (not ud['uuid']):
      return
    if(not 'markid' in ud) or (not ud['markid']):
      return
    pay = self.copy_base_payload(ud, 'Stop')
    pay['markid'] = self.to_ser(ud['markid']) if 'markid' in ud else None
    res = requests.post(self.URL, pay)
    return True if res.status_code == 201 else False


  def finalize(self, ud):
    if(not 'uuid' in ud) or (not ud['uuid']):
      return
    pay = self.copy_base_payload(ud, 'Finalize')
    res = requests.post(self.URL, pay)
    return True if res.status_code == 201 else False


  def collect(self, ud, fd):
    if(not 'uuid' in ud) or (not ud['uuid']):
      return None
    pay = self.copy_base_payload(ud, 'Collect')
    pay['collectopt'] = self.to_ser(fd)
    res = requests.get(self.URL, pay)
    rc = True if res.status_code == 200 else False
    return rc, res.json()


  @classmethod
  def unittest(cls, ud):
    pass



# 外部公開 API

def SI_TRACE_INITIALIZE(ud):
  obj = SiTrace()
  rc = obj.initialize(ud)
  return rc


def SI_TRACE_MARK(ud):
  obj = SiTrace()
  rc = obj.mark(ud)
  return rc


def SI_TRACE_SWEEP(ud):
  obj = SiTrace()
  rc = obj.sweep(ud)
  return rc


def SI_TRACE_STOP(ud):
  obj = SiTrace()
  rc = obj.stop(ud)
  return rc


def SI_TRACE_FINALIZE(ud):
  obj = SiTrace()
  rc = obj.finalize(ud)
  return rc


def SI_TRACE_COLLECT(ud, fd=None):
  obj = SiTrace()
  logger.error("-- obj.collect({0},{1})".format(ud,fd))
  rc, dc = obj.collect(ud, fd)
  return rc, dc

