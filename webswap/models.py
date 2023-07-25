from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

from web3 import Web3
from time import sleep
import json
import requests
import unicodedata
import time
import calendar

class NFTUserManager(BaseUserManager):
    def create_user(self, wallet_address, public_address):
        if not wallet_address:
            raise ValueError('Wallet address is required')
        wallet_balance = WalletsInfo.get_balance(address=wallet_address)
        user = self.model(
            wallet_address = wallet_address,
            public_addres = public_address,
            wallet_balance_eth = wallet_balance,
        )
        user.save(using=self._db)
        return user


    def create_superuser(self, wallet_address, password=None):
        user=self.create_user(
            wallet_address=wallet_address,
            password=password
        )
        user.set_password(password)
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(usenig=self._db)
        return user


class UserProfile(AbstractBaseUser):
    wallet_address = models.CharField(verbose_name = 'walelt address', max_length=42, unique=True, null=True)
    public_addres = models.CharField(verbose_name = 'short address', max_length=20, unique=True, null=True)
    wallet_balance_eth = models.DecimalField(verbose_name = 'user balance', max_digits=10, decimal_places=5,  null=True, unique=False)
    connect_date = models.DateTimeField(verbose_name = 'user created', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    user_email = models.EmailField(verbose_name = 'email', max_length=254, unique=True, null=True)
    user_sigh_contact = models.IntegerField(verbose_name='sigh contract', default=0)
    last_collection_update = models.IntegerField(default=0, null=True, blank=True)
    usd_value = models.CharField(max_length=50, null=True, blank=True)
    
    USERNAME_FIELD = 'wallet_address'

    REQUIRED_FIELDS = []
    
    objects = NFTUserManager()

    def __str__(self):
        return self.wallet_address
 
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return 


class CollectionRanking(models.Model):
    collect_rank = models.IntegerField(default=0, null=True, unique=True)
    collect_name = models.CharField(max_length=50, null=True, blank=True)
    collect_total_est_usd_value = models.CharField(max_length=50, null=True, blank=True)
    collect_volume_24h_usd_value = models.CharField(max_length=50, null=True, blank=True)
    collect_avg_price_24h_usd_value = models.CharField(max_length=50, null=True, blank=True)
    collenct_buy_holder_count= models.CharField(max_length=50, null=True, blank=True)
    collect_buy_holder_usd_value = models.CharField(max_length=50, null=True, blank=True)
    collect_img_url = models.CharField(max_length=15, null=True, unique=True, blank=True)
    def __str__(self):
        return self.collect_name

class UserCollectionsList(models.Model):
    token_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.URLField(max_length = 250, null=True, unique=False)
    thumbnail_img = models.URLField(max_length = 250, null=True, unique=False)
    collection_name = models.CharField(max_length=150, null=True, blank=True)
    token_name = models.CharField(max_length=50, null=True, blank=True)
    token_id = models.CharField(max_length=50, null=True, blank=True, unique=False) #### MAST BE =True #####
    avg_price_24 = models.CharField(max_length=50, null=True, blank=True)
    token_usd_price = models.CharField(max_length=50, null=True, blank=True)
    detail_url = models.URLField(max_length = 250, null=True, unique=False)
    collection_logo_url = models.URLField(max_length=250, null=True, unique=False)
    contract_id = models.CharField(max_length=50, null=True, blank=True, unique=False)
    inner_id = models.CharField(max_length=50, null=True, blank=True, unique=False)


class WalletsInfo:
    def get_balance(address):
        try:
            infura = 'https://mainnet.infura.io/v3/a26bd1095ed547f9accf6bbb20156b52'
            web3 = Web3(Web3.HTTPProvider(infura))
            correct_address = Web3.toChecksumAddress(address)
            balance = web3.eth.getBalance(correct_address)
            balance_format = (web3.fromWei(balance, 'ether'))
            return balance_format
        except requests.exceptions.SSLError:
            rpc_ankr = 'https://rpc.ankr.com/eth'
            web3 = Web3(Web3.HTTPProvider(rpc_ankr))
            correct_address = Web3.toChecksumAddress(address)
            balance = web3.eth.getBalance(correct_address)
            balance_format = (web3.fromWei(balance, 'ether'))
            return balance_format

    
    def get_token_list(address):
        user = UserProfile.objects.get(wallet_address=address)
        url = 'https://api.debank.com/nft/collection_list?user_addr=0x4e023205cFa50e4F0E6b7527BBef57C92Db3ece4&chain=eth'#f'https://api.debank.com/nft/collection_list?user_addr={address}&chain=eth'
        request = requests.get(url)
        response = request.json()
        total_usd_values = 0
        try:
            for resonse_data in response['data']['result']['data']:
                data_collection_name = resonse_data['name']
                data_avg_price_24 = resonse_data['avg_price_24h']
                collection_url = resonse_data['logo_url']
                for collection_item in resonse_data['nft_list']:
                    data_image = collection_item['content']
                    data_thumbnail_img = collection_item['thumbnail_url']
                    token_name  = collection_item['name']
                    data_name = unicodedata.normalize('NFKD', token_name).encode('ascii', 'ignore').decode()
                    data_detail_url = collection_item['detail_url']
                    data_token_id = collection_item['id']
                    data_inner_id = collection_item['inner_id']
                    data_contract_id = collection_item['contract_id']
                    try:
                        all_data = json.dumps(collection_item).encode('utf-8')
                        token_price = json.loads(all_data)
                        data_price = round(token_price['usd_price'], 2)
                    except KeyError:
                        data_price = None
                    data_add_user_collection = UserCollectionsList(
                        token_owner = user,
                        image = data_image,
                        thumbnail_img = data_thumbnail_img,
                        collection_name = data_collection_name,
                        token_name = data_name,
                        token_id = data_token_id,
                        avg_price_24 = round(data_avg_price_24, 3),
                        token_usd_price = data_price,
                        detail_url = data_detail_url,
                        collection_logo_url = collection_url,
                        inner_id = data_inner_id,
                        contract_id = data_contract_id
                        )
                    data_add_user_collection.save()
                    try:
                        total_usd_values += data_price
                    except TypeError:
                        pass
            
        except TypeError as ex:
            sleep(3)
            return WalletsInfo.get_token_list(address)
        now = time.gmtime()
        user_profile = UserProfile.objects.get(wallet_address=address)
        user_profile.last_collection_update = calendar.timegm(now)
        user_profile.usd_value = total_usd_values
        user_profile.save()
        print(total_usd_values)
        #update_user_info.usd_value = total_usd_values


    def update_collections():
        CollectionRanking.objects.all().delete()
        request = requests.get('https://api.debank.com/collection/list?limit=120&chain_id=eth&start=0&q=')
        response = request.json()
        for data in response['data']['collections']:
            rank = int(data['rank_at'])
            name = str(data['name'])
            total_est_usd_value = round(data['total_est_usd_value'], 2)
            volume_24h_usd_value = int(data['volume_24h_usd_value'])
            avg_price_24h_usd_value = round(data['avg_price_24h_usd_value'], 2)
            buy_holder_count = int(data['buy_holder_count'])
            buy_holder_usd_value = round(data['buy_holder_usd_value'], 2)
            image_url = data['logo_url']
            collect_image_url = f'{rank}.png'
            add_collection = CollectionRanking(
                collect_rank = rank,
                collect_name = name,
                collect_total_est_usd_value = f'{total_est_usd_value:,}',
                collect_volume_24h_usd_value = f'{volume_24h_usd_value:,}',
                collect_avg_price_24h_usd_value = f'{avg_price_24h_usd_value:,}',
                collenct_buy_holder_count = buy_holder_count, 
                collect_buy_holder_usd_value = f'{buy_holder_usd_value:,}',
                collect_img_url = collect_image_url
            )
            add_collection.save()
            try:
                logo = requests.get(image_url).content
                logo_name = r'static/icon/collections_logo/' + f"{str(rank)}.png"
                with open(logo_name, 'wb') as file:
                    file.write(logo)
            except OSError as os_ex:
                logo_name = r'static/icon/collections_logo/' + f"{str(rank)}.png"
                with open(logo_name, 'wb') as file:
                    file.write(logo)