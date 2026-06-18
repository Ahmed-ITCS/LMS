from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Book, BookTransaction, Member


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'title', 'author', 'copies')
    search_fields = ('isbn', 'title', 'author')


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (MemberInline,)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'user', 'user_email')
    search_fields = ('member_id', 'user__username', 'user__email')

    @admin.display(description='Email')
    def user_email(self, obj):
        return obj.user.email


@admin.register(BookTransaction)
class BookTransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'issue_date', 'return_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('book__title', 'member__member_id', 'member__user__username')
