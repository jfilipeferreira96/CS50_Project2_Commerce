# Generated by Django 4.0.3 on 2022-03-19 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auction_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='auctions',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='auctions',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.auction'),
            preserve_default=False,
        ),
    ]