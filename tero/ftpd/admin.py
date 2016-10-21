from django.contrib import admin


from ftpd.models import FTPUser


class FTPUserAdmin(admin.ModelAdmin):

    list_display = ('username', 'useremail', 'ftpd_perm')
    list_display_links = ('username', 'useremail')

    search_fields = ['user__email', 'user__username']

    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('FTP Permissions', {
            'classes': ('collapse',),
            'fields': (('change_directory', 'list_files', 'retrieve_file'), ('append_data',
                       'delete', 'rename', 'create_dir', 'store', 'change_mode_perm')),
        }),
        )

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

    def useremail(self, obj):
        return obj.user.email
    useremail.short_description = 'Email'

    def ftpd_perm(self, obj):
        return obj.ftpd_perm
    ftpd_perm.short_description = 'FTP Permissions'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user',)
        return self.readonly_fields

admin.site.register(FTPUser, FTPUserAdmin)
