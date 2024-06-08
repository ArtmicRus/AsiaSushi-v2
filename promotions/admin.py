from django.contrib import admin

from promotions.models import Promotion, PromotionProducts, PromotionTerms

# Register your models here.
# admin.site.register(Promotion)
admin.site.register(PromotionProducts)
admin.site.register(PromotionTerms)