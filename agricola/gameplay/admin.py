from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(Account)
admin.site.register(Player)
admin.site.register(PlayerBoardStatus)
admin.site.register(BoardPosition)
admin.site.register(FencePosition)
admin.site.register(Resource)
admin.site.register(PlayerResource)
admin.site.register(PeriodCard)
admin.site.register(ActivationCost)
