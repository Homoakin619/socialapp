from django.contrib import admin
from django.contrib.auth.models import User
from core.models import Post,Comment,Notification,Notify


admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Notify)

# admin.site.unregister(User)

# class ProfileInline(admin.StackedInline):
#     model = Profile
#     max_num = 1

# class UserAdmin(admin.ModelAdmin):
#     model = User
#     fields = ['username','email']
#     inlines = [ProfileInline]

# admin.site.register(User,UserAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['user','tag'] 

    search_fields = ['tag','user__username']

admin.site.register(Post,PostAdmin)

