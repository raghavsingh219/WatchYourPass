# Generated by Django 3.1.6 on 2021-02-15 12:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(db_index=True, max_length=100)),
                ('count', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='BreachedSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253)),
                ('title', models.CharField(blank=True, max_length=253)),
                ('logo', models.ImageField(default='static/breached_site_logos/default.png', upload_to='static/breached_site_logos/')),
                ('breach_description', models.TextField(blank=True)),
                ('date_added', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('breach_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('account_breach_count', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BreachSiteType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=253)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BreachType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=253)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=80, unique=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=100, unique=True)),
                ('count', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordAccountRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='api.account', verbose_name='account_id')),
                ('password', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='api.password', verbose_name='password_id')),
            ],
        ),
        migrations.AddIndex(
            model_name='password',
            index=models.Index(fields=['hash'], name='api_passwor_hash_e7b306_idx'),
        ),
        migrations.AddIndex(
            model_name='domain',
            index=models.Index(fields=['domain'], name='api_domain_domain_82ec1d_idx'),
        ),
        migrations.AddField(
            model_name='breachedsite',
            name='breach_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api.breachtype'),
        ),
        migrations.AddField(
            model_name='account',
            name='breached_site',
            field=models.ManyToManyField(to='api.BreachedSite'),
        ),
        migrations.AddField(
            model_name='account',
            name='domain',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api.domain'),
        ),
        migrations.AddField(
            model_name='account',
            name='passwords',
            field=models.ManyToManyField(through='api.PasswordAccountRelation', to='api.Password'),
        ),
        migrations.AlterUniqueTogether(
            name='passwordaccountrelation',
            unique_together={('account_id', 'password_id')},
        ),
        migrations.AddIndex(
            model_name='breachedsite',
            index=models.Index(fields=['domain'], name='api_breache_domain_ed2335_idx'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['email'], name='api_account_email_73f779_idx'),
        ),
        migrations.AddConstraint(
            model_name='account',
            constraint=models.UniqueConstraint(fields=('email', 'domain'), name='email_domain_unique'),
        ),
    ]
