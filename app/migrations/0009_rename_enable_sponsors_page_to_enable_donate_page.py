# Generated manually to rename enable_sponsors_page to enable_donate_page

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_article_authors_names_article_country_of_publication_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitesettings',
            old_name='enable_sponsors_page',
            new_name='enable_donate_page',
        ),
    ]

