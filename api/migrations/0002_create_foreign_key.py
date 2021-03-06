# Generated by Django 3.1.6 on 2021-02-15 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                (
                "ALTER TABLE api_passwordaccountrelation ADD CONSTRAINT api_account_account_id_fkey FOREIGN KEY (account_id) references api_account(id) ON DELETE CASCADE"),
                (
                "ALTER TABLE api_passwordaccountrelation ADD CONSTRAINT api_account_password_id_fkey FOREIGN KEY (password_id) references api_password(id) ON DELETE CASCADE")
            ],
            reverse_sql=[
                ("ALTER TABLE api_passwordaccountrelation DROP CONSTRAINT api_account_account_id_fkey"),
                ("ALTER TABLE api_passwordaccountrelation DROP CONSTRAINT api_account_password_id_fkey"),
            ]
        ),
    ]
