from django.contrib import admin
from .models import Banner, user_client, category_master, contact_us, franchise, tbl_product, address


# Register your models here.
class BannerAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'desk_image', 'mob_image', 'uploaded_at', 'alt_text')


admin.site.register(Banner, BannerAdmin)


class ClientReview(admin.ModelAdmin):
    list_display = ('title', 'image', 'client_desc')


admin.site.register(user_client, ClientReview)


class category_admin(admin.ModelAdmin):
    list_display = ('cat_name', 'status', 'create_date', 'image')


admin.site.register(category_master, category_admin)


class contact_admin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')


admin.site.register(contact_us, contact_admin)


class franchise_admin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address')


admin.site.register(franchise, franchise_admin)

class product_admin(admin.ModelAdmin):
    list_display = ('productname', 'category', 'mrp')


admin.site.register(tbl_product, product_admin)

admin.site.register(address)