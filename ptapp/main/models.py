from django.db import models

# Create your models here.

#Describes a particular account being tracked.
class Accounts(models.Model):
    name = models.CharField(max_length=200)
    bank = models.CharField(max_length=200)

    def __str__(self):
        return "%s at %s" % (self.name, self.bank)

#Store any aliases that an account might have
class AccountAliases(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    alias = models.CharField(max_length=200)
