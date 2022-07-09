from rest_framework import serializers
from django.utils import timezone
from django.db import models 

from datetime import datetime
import re, time, sh, base64, pickle
from sitrace.models import SIContext
 
from logging import basicConfig, getLogger, DEBUG, ERROR, CRITICAL
basicConfig(level=ERROR)      # これはメインのファイルにのみ書く
logger = getLogger(__name__)  # これはすべてのファイルに書く

class SIContextSerializer(serializers.ModelSerializer):
  class Meta:

    model   = SIContext
    fields  = (
                '_id',
                'uuid',
                'actid',
                'created_at',
                'closed_at',
                'host',
                'ip',
                'active',
                'markid',
                'service',
                'file',
                'cls',
                'func',
                'tags',
                'verbose',
                'worker',
                'starts_at',
                'lasts_at',
                'ends_at',
              )

  def create(self, vd):
    """
    REST POST で呼び出しされる関数のオーバライドをする.
    vd = validated_data には REST POST で渡されたパラメータが格納されている.
    """
    actid = vd['actid'] if 'actid' in vd.keys() else 0

    def initialize(vd):
      """ 以前の context を active = False にしたうえで、新規 context を作成する """
      logger.error(vd['host'])
      old_list = SIContext.objects.all().filter(service=vd['service'], host=vd['host'], active=True)
      for oc in old_list:
        oc.active = False
        oc.save() # store to DB
      now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      ctx = SIContext(
        uuid=vd['uuid'], service=vd['service'], host=vd['host'], ip=vd['ip'], created_at=now, lasts_at=now, active=True
      )
      ctx.save() # store to DB
      return ctx


    def mark(vd):
      """
      markid が DB にすでに存在している場合は DB から該当する context を取り出す.
      markid が DB に存在しない場合は新規 context を作成する. 
      """
      exists = SIContext.objects.all().filter(uuid=vd['uuid'], host=vd['host'], active=True).exists()
      if not exists:
        logger.critical("Error: Could not found context. You must call SI_TRACE_INITIALIZE. !!!!!!!!!")
        pass # SI_TRACE_INITIALIZE を実行し忘れていた場合でも救う
      now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      ctx, new_created = SIContext.objects.get_or_create(
        uuid=vd['uuid'], markid=vd['markid'], service=vd['service'], host=vd['host'], ip=vd['ip'], active=True
      )
      ctx.file = vd['file'] if 'file' in vd else None
      ctx.cls  = vd['cls']  if 'cls'  in vd else None
      ctx.func = vd['func'] if 'func' in vd else None
      ctx.tags = vd['tags'] if 'tags' in vd else None
      ctx.verb = vd['verb'] if 'verb' in vd else None
      ctx.verb = vd['wkr']  if 'wkr'  in vd else None
      ctx.starts_at, ctx.lasts_at, ctx.ends_at, ctx.active = now, now, None, True
      ctx.save() # store to DB
      return ctx


    def sweep(vd):
      """
      Mark 処理に対応する context を取り出し, REST POST で通知された tags を使って
      context が持つ tags を消す.
      """
      ctx = SIContext.objects.get(uuid=vd['uuid'], host=vd['host'], markid=vd['markid'], active=True)
      list_tags = self.to_des(ctx.tags) # context has tags
      for erase in self.to_des(vd['tags']): # tags with Sweep method
        logger.error("-- remove {0} by {1}".format(list_tags, erase))
        list_tags.remove(erase)
      now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      ctx.tags = list_tags
      ctx.tags = self.to_ser(list_tags)
      ctx.starts_at, ctx.lasts_at, ctx.ends_at, ctx.active = now, now, None, True  
      ctx.save() # store to DB
      return ctx


    def stop(vd):
      """
      markid で指示された対象区間での Mark-Sweep 終了を通知する. これを受けて ends_at
      に終了時刻を入れる. 従って ends_at が空欄であれば正常終了していないことを意味する.
      """
      ctx = SIContext.objects.get(uuid=vd['uuid'], host=vd['host'], markid=vd['markid'], active=True)
      now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      ctx.starts_at, ctx.lasts_at, ctx.ends_at, ctx.active = now, now, now, True  
      ctx.save() # store to DB
      return ctx


    def finalize(vd):
      """
      トレース終了を通知する.
      具体的には Initialize で生成された context の closed_at に時刻を登録する.
      """
      ctx = SIContext.objects.get(uuid=vd['uuid'], host=vd['host'], ends_at=None, active=True)
      now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      ctx.closed_at = now
      ctx.active    = False
      ctx.save() # store to DB
      return ctx



    if   actid == 1: # initialize
      ctx = initialize(vd)
    elif actid == 2: # mark
      ctx = mark(vd)
    elif actid == 3: # sweep
      ctx = sweep(vd)
      pass
    elif actid == 4: # stop
      ctx = stop(vd)
      pass
    elif actid == 5: # finalize
      ctx = finalize(vd)
      pass
    elif actid == 6: # collect
      # collect は RESTful API の GET メソッドなので本クラスでは呼び出されない. ./apiv1/views.py を参照.
      # DRF では DRF 用ビューを通り, その後 serializer を経てアプリ固有の model に逹する. (akiyoko rest1: P11)
      pass
    else:
      pass
    return ctx


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


    
