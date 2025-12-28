import MySQLdb
from django.conf import settings

def get_connection():
    return MySQLdb.connect(
        host = settings.DATABASES['default']['HOST'],
        user = settings.DATABASES['default']['USER'],
        password = settings.DATABASES['default']['PASSWORD'],
        db = settings.DATABASES['default']['NAME'],
    )