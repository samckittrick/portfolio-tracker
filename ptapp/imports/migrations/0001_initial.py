# Generated by Django 3.0.5 on 2020-07-18 23:56

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friendlyName', models.CharField(max_length=200)),
                ('account_id', models.CharField(max_length=22)),
                ('routing_number', models.CharField(max_length=9)),
                ('institution_name', models.CharField(max_length=200)),
                ('institution_id', models.CharField(max_length=32)),
                ('type', models.CharField(choices=[('cash', 'Cash Account'), ('cd', 'Certificate of Deposit'), ('bond', 'Bond'), ('stock', 'Stock')], default='cash', max_length=6)),
                ('currency_symbol', models.CharField(default='USD', max_length=3)),
                ('matched', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FileData',
            fields=[
                ('fileid', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=200)),
                ('expiration', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='CashAccountData',
            fields=[
                ('accountdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='imports.AccountData')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=13)),
                ('balance_date', models.DateTimeField()),
            ],
            bases=('imports.accountdata',),
        ),
        migrations.CreateModel(
            name='InvestmentAccountData',
            fields=[
                ('accountdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='imports.AccountData')),
                ('position_date', models.DateTimeField()),
            ],
            bases=('imports.accountdata',),
        ),
        migrations.AddField(
            model_name='accountdata',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='imports.FileData'),
        ),
        migrations.AddField(
            model_name='accountdata',
            name='matched_account_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='matched_account', to='main.Accounts'),
        ),
        migrations.CreateModel(
            name='InvestmentTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ftid', models.CharField(max_length=255)),
                ('type', models.IntegerField(choices=[(1, 'BUY_DEBT'), (2, 'BUY_MF'), (3, 'BUY_OPT'), (4, 'BUY_OTHER'), (5, 'BUY_STOCK'), (6, 'CLOSURE_OPT'), (7, 'INCOME'), (8, 'INV_EXPENSE'), (9, 'JRNL_FUND'), (10, 'JRNL_SEC'), (11, 'MARGIN_INTEREST'), (12, 'REINVEST'), (13, 'RET_OF_CAP'), (14, 'SELL_DEBT'), (15, 'SELL_MF'), (16, 'SELL_OPT'), (17, 'SELL_OTHER'), (18, 'SELL_STOCK'), (19, 'SPLIT'), (20, 'TRANSFER')], default=main.models.InvestmentTransaction.InvestmentTransactionTypes['BUY_OTHER'])),
                ('tradeDate', models.DateTimeField()),
                ('settleDate', models.DateTimeField()),
                ('memo', models.CharField(max_length=255)),
                ('CUSIP', models.CharField(max_length=16)),
                ('ticker', models.CharField(max_length=8)),
                ('income_type', models.IntegerField(choices=[(1, 'CGLONG'), (2, 'CGSHORT'), (3, 'DIV'), (4, 'INTEREST'), (5, 'MISC')])),
                ('units', models.FloatField()),
                ('unit_price', models.FloatField()),
                ('comission', models.FloatField()),
                ('fees', models.FloatField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='imports.InvestmentAccountData')),
            ],
        ),
        migrations.CreateModel(
            name='InvestmentPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=8)),
                ('CUSIP', models.CharField(max_length=16)),
                ('units', models.FloatField()),
                ('unit_price', models.FloatField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='imports.InvestmentAccountData')),
            ],
        ),
        migrations.CreateModel(
            name='CashTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('amount', models.FloatField()),
                ('memo', models.CharField(max_length=255)),
                ('ftid', models.CharField(max_length=255)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='imports.CashAccountData')),
            ],
        ),
    ]
