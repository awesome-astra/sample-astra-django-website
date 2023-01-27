# Sample Django app with Astra DB

This is a simple [Django](https://docs.djangoproject.com/en/4.1/) application to illustrate how to use Astra DB as database backend. The code is ready to run (provided you first go
through the setup).

_Note: Astra DB is a database-as-a-service in the cloud built on [Apache Cassandra™](https://cassandra.apache.org)._

The application uses the
[`django-cassandra-engine`](http://r4fek.github.io/django-cassandra-engine/)
package and shows how to use the models it
provides, but also how to access and directly work with the underlying
session object for more advanced, Cassandra-specific usages.

This example application has been developed as a companion to the
[Awesome Astra "Django" page](https://awesome-astra.github.io/docs/pages/develop/frameworks/django/), to which we refer for additional information, including a convenient description of
the steps necessary to migrate an existing Django app to using Astra DB as backend.



## Goal

#### Technical goals

This sample project is a vanilla Django application.
As such, it fully conforms to a "server-side rendering" philosophy,
so that each endpoint completely constructs and return a static HTML page.

The application uses Astra DB as its only storage backend, by means of the
[`django-cassandra-engine`](http://r4fek.github.io/django-cassandra-engine/)
plugin. In particular, the most "ordinary" data access is performed by using
the _model_ paradigm; but we also want to show how to access the underlying
"raw" database connection for more advanced (and Cassandra-specific) usages.
_This latter approach should be considered part of the idiomatic usage of
the plugin._

#### The "Partyfinder" application

The project (`parties`) is comprised of a single application,
called `partyfinder`. It is a very simple UI to browse, insert and delete
the upcoming parties for a given city.

For a given party, the UI lets you increase/decrease the number of
participants (a mockup of a "count me in" feature): this feature is built
with race conditions in mind, to avoid mistakes and inconsistencies
such as negative numbers of participants.

_What this application is **not**:_ a nice-looking frontend.



## Setup


### Database setup

You need an Astra DB instance to host your data. Once you have your DB,
you must provide connection parameters and secrets to the application: here's how.

First go to the Astra website and
[create an account](https://awesome-astra.github.io/docs/pages/astra/create-account/).
You can stay in the Free Tier
forever and still use a pretty generous amount of storage and monthly reads/writes.

Then
[create a database](https://awesome-astra.github.io/docs/pages/astra/create-instance/)
(at the time of writing, a newly-created Free Tier
account covers some regions on specific cloud providers). In the following we'll call the database `mydatabase` and the keyspace `mydjango`.

Go to your settings,
[create a **Database Administrator** token](https://awesome-astra.github.io/docs/pages/astra/create-token/)
and save it somewhere safe.
_In a production application you will want to limit your token's permissions more accurately according to the least-privilege principle, but this is a demo and it's convenient to let the command-line automation handle most of the setup for you._

You must now prepare a `.env` file for the Django application. the quickest way is using the
[Astra CLI](https://awesome-astra.github.io/docs/pages/astra/astra-cli/)
automation:

- install `Astra CLI` with xxx;
- re-open your shell;
- type `astra setup` and when prompted enter your token, the string starting with `AstraCS:...`;
- have the CLI download the [Secure Connect Bundle](https://awesome-astra.github.io/docs/pages/astra/download-scb/) and generate the dot-env for you: `astra db create-dotenv mydatabase -k mydjango`.

> Alternatively to using the CLI, you can (a) download the SCB to a known path location,
> (2) copy `cp .env.template .env`, and (3) manually edit the settings in `.env` with your values.


### Python and Django setup

#### Environment

You need Python 3.8+ (preferrably in a virtualenv).

Install the required dependencies with

```
pip install -r requirements.txt
```

_Note: the `django-cassandra-engine` installation in turn will bring `scylla-driver` along. The latter is functionally identical to `cassandra-driver` as far as a non-Scylla database is used, so you might as well remove the Scylla drivers, replace them with the mainstream Cassandra ones, and you won't notice any difference._

#### Sync with the database

Now issue the following commands to synchronize the database with the models
used in the application. This step will create the necessary table.

```
cd parties
python manage.py sync_cassandra
python manage.py syncdb
```

_Note: do not mind warnings about "unapplied migrations": the commands above
take care of what is needed at DB level. In fact, the `migrate` command is
not even supported by `django-cassandra-engine`.



## The application

### Run the application

Start the application in the `parties/` directory with

```
python manage.py runserver
```

You can visit the application at `http://127.0.0.1:8000/`:

- browse a city (you'll get no results);
- click "New" and insert a new party: fill the details and hit "Post";
- add other parties in this city and elsewhere;
- browse the city again;
- delete some items;
- view details of a party. There will be `+1` and `-1` buttons to alter the participant count: try them.

Now check the LWT at work: view details for the same party in two browser tabs at once and try to change the participant count in one, then the other without refreshing the page. The app will refuse to perform the update.

That's it! You should inspect the code to find out more, or visit the [Awesome Astra page](https://awesome-astra.github.io/docs/pages/develop/frameworks/django/) for more information.
