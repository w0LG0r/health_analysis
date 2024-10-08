import asyncio
import logging
from pprint import pformat
from esdbclient import EventStoreDBClient
from src.adapters.brokers import TaskiqBroker
from src.domains.meals.events import MealEvents
from src.config.config import setup_logging
from src.tasks.meal_tasks import MealsTasks, MealTaskPath

setup_logging()
logger = logging.getLogger(__name__)


class EventBusClient(EventStoreDBClient):
    def __init__(self, uri: str, stream_name: str, from_end: bool):
        super().__init__(uri)
        self.stream_name = stream_name
        self.from_end = from_end

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, tasks):
        self._tasks = tasks

    # @property
    # def subscription(self):
    #     return self.subscribe_to_stream(
    #         stream_name=self.stream_name, from_end=self.from_end
    #     )

    async def handle_events(self):
        try:
            subscription = self.subscribe_to_stream(
                stream_name=self.stream_name, from_end=self.from_end
            )
        except Exception as e:
            print(e)
            return

        try:
            # subscription = self.subscribe_to_stream(
            #     stream_name=self.stream_name, from_end=self.from_end
            # )

            logger.info(f"Subscribed to stream {subscription}:{self.stream_name}")

            while True:
                for event in subscription:
                    logger.info(
                        f"Received event from subscription {id(subscription)}:\n{pformat(event, indent=2)}"
                    )

                    match event.type:
                        case MealEvents.INSERT.value:
                            task = self.tasks.get(MealTaskPath.INSERT.value)
                            # process(event.data.decode("utf-8"))
                        case _:
                            pass

                    if task:  # type: ignore
                        task = await task.kiq(event)
                        res = await task.wait_result()
                        print("res: ", res)

        except KeyboardInterrupt as e:
            logger.error(f"Error in handle_events:{e}")
            raise e

        except Exception as e:
            logger.error(f"Error in handle_events:{e}")
            raise e

        finally:
            if subscription:  # type: ignore
                logger.info(f"Stopping subscription: {subscription}")
                subscription.stop()
