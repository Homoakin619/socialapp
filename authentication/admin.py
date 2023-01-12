from django.contrib import admin,auth

from authentication.models import Profile

User = auth.get_user_model()

# admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username','email','first_name','last_name']
    inlines = [ProfileInline]

# admin.site.register(User,UserAdmin)
admin.site.register(Profile)
