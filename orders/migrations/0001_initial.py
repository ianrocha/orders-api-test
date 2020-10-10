# Generated by Django 3.1.2 on 2020-10-10 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(blank=True, max_length=120, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('cancelled', 'Cancelled')], default='created', max_length=120)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.cart')),
            ],
        ),
    ]
