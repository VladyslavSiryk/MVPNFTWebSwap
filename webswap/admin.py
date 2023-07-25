from django.contrib import admin
from .models import UserProfile as MyCustomUser, CollectionRanking

# Register your models here.
@admin.register(MyCustomUser)
class AdminMyCustomUser(admin.ModelAdmin):
    list_display = ("wallet_address",
                    "wallet_balance_eth",
                    "connect_date",
                    "user_email",
                    "user_sigh_contact",
                    "usd_value",)
    ordering = ("wallet_balance_eth", "user_sigh_contact", "user_email", "last_login","usd_value",)
    search_fields = ('wallet_address', 'wallet_balance_eth', 'user_sigh_contact', 'user_email',"usd_value,")

@admin.register(CollectionRanking)
class AdminMyCustomUser(admin.ModelAdmin):
    list_display = ("collect_rank",
                    "collect_name",
                    "collect_total_est_usd_value",
                    "collect_volume_24h_usd_value",
                    "collect_avg_price_24h_usd_value",
                    "collenct_buy_holder_count",
                    "collect_buy_holder_usd_value",
                    "collect_img_url",)
    ordering = ('collect_rank','collect_name', 'collect_volume_24h_usd_value')
    search_fields = ('collect_rank', 'collect_name')
