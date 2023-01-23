import uuid

from django.utils import timezone

from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

# A model for this app
class Party(DjangoCassandraModel):
  city = columns.Text(
    primary_key=True,
  )
  id = columns.UUID(
    primary_key=True,
    clustering_order='asc', # (allowed: 'asc' , 'desc', lowercase)
    default=uuid.uuid4,
  )
  name = columns.Text()
  date = columns.DateTime(default=timezone.now)

  class Meta:
    get_pk_field='id'
