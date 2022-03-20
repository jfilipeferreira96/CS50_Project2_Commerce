# Generated by Django 4.0.3 on 2022-03-20 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auction_current_bidder_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='current_bidder_user',
        ),
        migrations.AddField(
            model_name='auction',
            name='current_bidder_user_id',
            field=models.IntegerField(blank=True, default=2),
            preserve_default=False,
        ),
    ]
