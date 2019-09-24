from django.contrib import admin
from django.core.cache import cache
from goods.models import GoodsType,Goods,GoodsSKU,GoodsImage,IndexGoodsBanner,IndexPromotionBanner,IndexTypeGoodsBanner
# Register your models here.

class IndexPromotionBannerAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,form,change):
        '''更新表中数据时调用'''
        super().save_model(request,obj,form,change)

        # 发出任务，让celery worker重新生成首页静态页面
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页缓存数据
        cache.delete('index_page_data')

    def delete_model(self, request, obj):
        '''删除表中的数据时调用'''
        super().delete_model(request, obj)
        # 发出任务，让celery worker重新生成首页静态页面
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页缓存数据
        cache.delete('index_page_data')


admin.site.register(IndexTypeGoodsBanner)
admin.site.register(GoodsSKU)
admin.site.register(Goods)
admin.site.register(GoodsImage)
admin.site.register(IndexGoodsBanner)
admin.site.register(GoodsType)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)