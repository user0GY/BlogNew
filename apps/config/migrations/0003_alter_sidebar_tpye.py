# Generated by Django 4.2.1 on 2023-07-04 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_sidebar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='tpye',
            field=models.IntegerField(choices=[(0, 'HTML'), (1, '最新文章'), (2, '最热文章'), (3, '最热评论')], default=1, verbose_name='展示类型'),
        ),
    ]