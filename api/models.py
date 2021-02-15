from datetime import datetime

from django.db import models, migrations


class Domain(models.Model):
    domain = models.CharField(max_length=80, unique=True, db_index=True)
    count = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return self.domain

    def save(self, *args, **kwargs):
        self.domain = self.domain.lower()
        return super(Domain, self).save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['domain']),
        ]


class BreachSiteType(models.Model):
    type = models.CharField(max_length=253)
    count = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return self.type


class BreachType(models.Model):
    type = models.CharField(max_length=253)
    count = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return self.type


class BreachedSite(models.Model):
    domain = models.CharField(max_length=253, db_index=True)
    title = models.CharField(blank=True, max_length=253)
    logo = models.ImageField(upload_to='static/breached_site_logos/', default='static/breached_site_logos/default.png')
    breach_description = models.TextField(blank=True)
    date_added = models.DateTimeField(default=datetime.now, blank=True)
    breach_date = models.DateTimeField(default=datetime.now, blank=True)
    breach_type = models.ForeignKey(BreachType, on_delete=models.CASCADE, default=0)
    account_breach_count = models.BigIntegerField(blank=False, default=0)

    def __str__(self):
        return self.domain

    def save(self, *args, **kwargs):
        self.domain = self.domain.lower()
        return super(BreachedSite, self).save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['domain']),
        ]


class Password(models.Model):
    hash = models.CharField(max_length=100, unique=True, db_index=False)
    count = models.IntegerField(blank=False, default=1)

    def __str__(self):
        return self.hash

    class Meta:
        indexes = [
            models.Index(fields=['hash']),
        ]


class Account(models.Model):
    email = models.CharField(max_length=100, blank=False, db_index=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, default=0)
    breached_site = models.ManyToManyField(BreachedSite)
    passwords = models.ManyToManyField(Password,through='PasswordAccountRelation')
    count = models.IntegerField(blank=False, default=1)

    def __str__(self):
        return self.email

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['email', 'domain'], name='email_domain_unique')
        ]

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(Account, self).save(*args, **kwargs)


class PasswordAccountRelation(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name='account_id',db_constraint=False)
    password = models.ForeignKey(Password, on_delete=models.CASCADE,verbose_name='password_id',db_constraint=False)

    class Meta:
        unique_together = ['account_id', 'password_id']

