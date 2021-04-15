from django.contrib import admin
from .models import *


admin.site.register(Post)
admin.site.register(Band)
admin.site.register(Album)
admin.site.register(Review)
admin.site.register(MusicStyle)
admin.site.register(MusicLabel)
admin.site.register(Tag)

admin.site.site_title = 'Metalnews'
admin.site.site_header = 'Metalnews'
