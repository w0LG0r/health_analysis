from asyncpg import connect
from esdbclient import EventStoreDBClient

from src.adapters.spi.events.event_store_db.client import EventStoreDbClient


async def init_and_shutdown_time_scale_db_connection(**kwargs):
    dsn = "/".join(list(kwargs.values()))
    resource = await connect(dsn=dsn)
    yield resource
    await resource.close()


def init_and_shutdown_event_client(**kwargs):
    resource = EventStoreDBClient(**kwargs)
    yield resource
    resource.close()
