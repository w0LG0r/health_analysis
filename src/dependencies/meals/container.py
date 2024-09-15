from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Resource,
    Object,
    Dict,
    Factory,
)


from taskiq_aio_pika import AioPikaBroker

from src.adapters.databases import TimeScaleDatabase
from src.dependencies.meals.factories import InsertMealQueryFactory, MealQueryFactory
from src.domains.meals.events import DeleteMealEvent, InsertMealEvent, MealEvents


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    database = Resource(
        TimeScaleDatabase,
        config=config.dsn.timescaledb,
    )

    broker = Resource(AioPikaBroker, url=config.dsn.rabbitmq.url)

    events = Dict(
        {
            MealEvents.INSERT: Object(InsertMealEvent),
            MealEvents.DELETE: Object(DeleteMealEvent),
        }
    )

    query_factories = Dict(
        {
            MealQueryFactory.INSERT: Factory(
                InsertMealQueryFactory,
                table_name=config.dsn.timescaledb.tables.meals,
            )
        }
    )
