from django.db import models
from django.utils import timezone
from django import forms
import uuid as uuid_lib
import textwrap, time
import traceapiconfig as cfg

from logging import basicConfig, getLogger, DEBUG, ERROR
logger = getLogger(__name__)  # これはすべてのファイルに書く

YN = ((True, 'Yes'), (False, 'No'))
ACTs = tuple({v: k for k, v in cfg.ACT_INT.items()}.items()) # dict の k, v を入れ変えてから tuple に変換する

class SIContext(models.Model):
  _id                   = models.UUIDField(verbose_name='id',         default=uuid_lib.uuid4, editable=False)
  # for Context by Design.md
  uuid                  = models.CharField(verbose_name='uuid',       max_length=64,   blank=True,   null=True)
  actid                 = models.PositiveSmallIntegerField(verbose_name='actid',       choices=ACTs, null=True)
  created_at            = models.DateTimeField(verbose_name='created',blank=True,      null=True)
  closed_at             = models.DateTimeField(verbose_name='closed', blank=True,      null=True)
  host                  = models.CharField(verbose_name='host',       max_length=64,   blank=True, null=True)
  ip                    = models.CharField(verbose_name='ip',         max_length=64,   blank=True, null=True)
  active                = models.BooleanField(verbose_name='active',  choices=YN,      default=False)
  # for Chunk by Design.md
  markid                = models.CharField(verbose_name='markid',     max_length=64,   blank=True, null=True)
  service               = models.CharField(verbose_name='service',    max_length=64,   blank=True, null=True)
  file                  = models.CharField(verbose_name='file',       max_length=64,   blank=True, null=True)
  cls                   = models.CharField(verbose_name='cls',        max_length=64,   blank=True, null=True)
  func                  = models.CharField(verbose_name='func',       max_length=64,   blank=True, null=True)
  tags                  = models.CharField(verbose_name='tags',       max_length=1024, blank=True, null=True)
  verbose               = models.CharField(verbose_name='verbose',    max_length=128,  blank=True, null=True)
  worker                = models.CharField(verbose_name='worker',     max_length=64,   blank=True, null=True)
  starts_at             = models.DateTimeField(verbose_name='start',  blank=True,      null=True)
  lasts_at              = models.DateTimeField(verbose_name='last',   blank=True,      null=True)
  ends_at               = models.DateTimeField(verbose_name='end',    blank=True,      null=True)


