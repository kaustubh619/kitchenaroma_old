from django.contrib import admin
from .models import Kitchen, Category, MenuItem, Cart, KitchenRatingsAndReviews, KitchenGallery, Timing, Order, Contact, OrderTotal

# Register your models here.
class KitchenCategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    show_change_link = True


class KitchenGalleryInline(admin.TabularInline):
    model = KitchenGallery
    extra = 1
    show_change_link = True    


class CategoryMenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    show_change_link = True


class KitchenAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    inlines = [KitchenCategoryInline, KitchenGalleryInline] 


class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryMenuItemInline]


admin.site.register(Kitchen, KitchenAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(KitchenRatingsAndReviews)
admin.site.register(KitchenGallery)
admin.site.register(Timing)
admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(OrderTotal)