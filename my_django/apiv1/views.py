import sys; sys.dont_write_bytecode = True
import os, json, time, copy, requests, textwrap, socket, pickle, base64, sh
from datetime import datetime
from pprint import pprint

from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters # !! akiyoko rest2: P181
 
from sitrace.models import SIContext
from .serializers import SIContextSerializer

from logging import basicConfig, getLogger, DEBUG, ERROR, CRITICAL
basicConfig(level=ERROR)      # これはメインのファイルにのみ書く
logger = getLogger(__name__)  # これはすべてのファイルに書く
 
# akiyoko rest2: P181
class   SIContextFilter(filters.FilterSet): # !!
  """
  SIContext フィルタクラス
  ref. https://qiita.com/okoppe8/items/77f7f91f6878e3f324cc 
  """
  # 次の(1)〜のように各型ごとに完全一致 と 部分一致 での検索を可能にしている
  # (1)の場合 http://localhost:8000/api/v1/si/tracer/svc/?uuid=AutoRelease_20200412-140027
  # (2)の場合 http://localhost:8000/api/v1/si/tracer/svc/?uuid_c=AutoRelease_20200412-140027
  # (3)の場合 http://localhost:8000/api/v1/si/tracer/svc/?created_at=2020-04-12 14:00:27
  # (4)の場合 http://localhost:8000/api/v1/si/tracer/svc/?created_at=2020-04-12 14:00:27,2020-04-12 15:00
  # (5)の場合 http://localhost:8000/api/v1/si/tracer/svc/?active=True
  for i in ['uuid', 'host', 'ip', 'markid', 'service', 'file', 'cls', 'func', 'tags', 'verbose', 'worker',]:
    setattr(SIContext, i,                 filters.CharFilter(field_name='{}'.format(i))) # (1) eq. uuid = filters.CharFilter(field_name='uuid')
    setattr(SIContext, '{}__c'.format(i), filters.CharFilter(field_name='{}'.format(i))) # (2)
  for i in ['created_at', 'closed_at', 'starts_at', 'lasts_at', 'ends_at',]:
    setattr(SIContext, i,                 filters.DateTimeFilter(field_name='{}'.format(i)))        # (3)
    setattr(SIContext, '{}__r'.format(i), filters.DateFromToRangeFilter(field_name='{}'.format(i))) # (4)
  for i in ['active']:
    setattr(SIContext, i, filters.BooleanFilter(field_name='{}'.format(i)))   # (5)

  class Meta:
    model = SIContext
    exclude = [ '_id' ]


class SIContextViewSet(viewsets.ModelViewSet):
  """
  list:
    全カテゴリーの取得

  create:
    context の生成をする.

  update:
    {id} で指定した context の一部更新. ただし {id} は非公開にしているので, 本 API は使用できない.

  retrieve:
    {id} で指定した context の取得. ただし {id} は非公開にしているので, 本 API は使用できない.

  partial_update:
    {id} で指定した context の一部更新. ただし {id} は非公開にしているので, 本 API は使用できない.

  delete:
    {id} で指定した context の削除. ただし {id} は非公開にしているので, 本 API は使用できない.
  """
  queryset = SIContext.objects.all()    # queryset[0] などとすると個々のオブジェクトが取り出せる
  serializer_class = SIContextSerializer
  # 次の 2つにより http://localhost:8000/api/v1/si/tracer/svc/?host=001 という検索ができるになる.
  filter_backends = [filters.DjangoFilterBackend]  # !! akiyoko rest2: P181
  filterset_fileds = '__all__'                     # !! akiyoko rest2: P181
  filterset_class  = SIContextFilter               # !! Browsable API に「フィルタ」ボタンができる

  def list(self, request):
    """
    GET リソース名/ のオーバライド処理.
    DRF 用ビューを通り, その後 serializer を経てアプリ固有の model に逹する. (akiyoko rest1: P11)
    """
    if('cltopt' in request.GET) and (request.GET['cltopt']):
      opt = self.to_des(request.GET['cltopt'])
      L, O, OB, EV = opt['limit'], opt['order'], opt['order_by'], opt['mevent']
      ctx_list   = self.queryset.order_by('-lasts_at').filter(uuid=request.GET['uuid'])[:L] # T.B.D
      serializer = self.get_serializer(ctx_list, many=True)
    else:
      serializer = self.get_serializer(self.queryset, many=True)
    return Response(serializer.data)


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


    
