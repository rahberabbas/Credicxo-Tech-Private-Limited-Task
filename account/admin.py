from django.contrib import admin
from .models import User, Teacher, Student, Admin
from django.contrib.auth.admin import UserAdmin


class UserModelAdmin(UserAdmin):

    list_display = ('email', 'name', 'phone', 'address', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','phone', 'address',)}),
        ('Permissions', {'fields': ('is_admin','is_teacher','is_student')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'address', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserModelAdmin)
admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(Student)