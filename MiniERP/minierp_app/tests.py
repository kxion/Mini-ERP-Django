from django.test import TestCase

# ### create customize condition of query
# from autofixture import AutoFixture
# from random import randint
# from minierp_app.models import Customer, Supply, Product, Stock, Order, Purchase, Profit
# fixture = AutoFixture(Customer)
# fixture = AutoFixture(Supply, field_values={'phone': 6265867123, 'fax':7142657890, 'zip_code':92831})
# entries = fixture.create(10)


# ### example of date calculation
# yesterday = datetime.date.today() - datetime.timedelta(days=1)

# ### how to filtering only the day of creat_time:
# from django.utils import timezone
# now = timezone.now()
# Gig.objects.filter(create_time__day=now.day)

# ### delete example:
# Customer.objects.get(id = id).delete()
# Customer.objects.all().delete()
# Gig.objects.filter(create_time__month=now.month).delete()