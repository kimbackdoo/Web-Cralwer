from django.contrib import admin

# Register your models here.

#models에서 Shop을 임폴트
from .models import Shop
from .models import Parsed_data
from .models import Img_data
from .models import Other
admin.site.register(Shop)
admin.site.register(Parsed_data)
admin.site.register(Img_data)
admin.site.register(Other)
