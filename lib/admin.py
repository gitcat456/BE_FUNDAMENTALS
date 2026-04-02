from django.contrib.sessions.models import Session
from django.contrib import admin

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date', 'get_user']
    readonly_fields = ['session_key', 'expire_date', 'get_decoded']
    
    def get_user(self, obj):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        data = obj.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                return user.username
            except User.DoesNotExist:
                return 'Deleted User'
        return 'Anonymous'
    
    get_user.short_description = 'User'