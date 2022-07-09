from django.contrib import admin

from .models import SIContext

admin.site.site_title = 'アプリケーション' 
admin.site.site_header = 'アプリケーション' 
admin.site.index_title = 'メニュー'

class SIContextAdmin(admin.ModelAdmin):
  # 検索対象
  search_fields = [
#                   '_id',
                    'uuid',
#                   'actid',
                    'created_at',
                    'starts_at',
                    'lasts_at',
                    'ends_at',
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
                  ]

  # 一覧表示させるフィールド
  list_display =  [
#                   '_id',
                    'uuid',
#                   'actid',
                    'created_at',
                    'starts_at',
                    'lasts_at',
                    'ends_at',
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
                  ]

  # 検索フォームを設置する. かつ検索フィールドを指定する.
  list_filter =   [
#                   '_id',
                    'uuid',
#                   'actid',
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
                  ]

# Register your models here.
admin.site.register(SIContext, SIContextAdmin)

