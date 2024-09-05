# Metrica - a tool to keep track of data

This web app is designed to aid in the collection and presentation of values that change over time. Send a data point with an HTTP request, see what data you have stored and get how each value changes with a simple setup.

## Available features:
- Automatic data collection
- Manual data insertion
- Line graphs for every metric

## Requirements:
- Python 3.11+
- Django 5.0.3+
- MySQL 8.2.0+ (can be substituted for one of the following: PostgreSQL, MariaDB, Oracle, SQLite)

## Setting up a new MySQL database
1. Log into MySQL as admin user
2. Create a database named _'metricadb'_
3. Create a standard user and keep its credentials safe. Keep in mind the host restriction if MySQL is run on a different server
4. Grant the new user all priveleges on _'metricadb'_
5. In `metrica/metrica/settings.py` locate the `DATABASES` definition and replace the values for `'USER'` and `'PASSWORD'` with the user credentials from step 3
6. From the _'metrica'_ directory (the one that has _'manage.py'_ in it) run `python3 manage.py makemigrations` and `python3 manage.py migrate`

Note: Other database types suported by Django require similar procedures to set up. To reconfigure Django for a different DB refer to the following article:

https://docs.djangoproject.com/en/5.1/ref/databases/

To launch the application run

`python3 manage.py runserver <PORT>`

Replace PORT with the port you'd like the app to listen on. Will default to 80 if omitted

## Planned improvements
- Cascade deletion support
- Search and sort filters for the Product view and the Metric view
- Better looking modals
- Editable entry names