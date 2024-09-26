from typing import Any, List, Optional, Self, Tuple, Union, LiteralString

from pydantic import (
    AmqpDsn,
    BaseModel,
    Field,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_core import (
    MultiHostUrl,
    PydanticCustomError,
    Url,
)


class UriPassedToInitError:
    error_type: LiteralString = "uri_passed_to_args_on_init"
    message: LiteralString = (
        "'Uri' gets resolved from other args and should not be passed directly on init."
    )


class BaseConnectionString(BaseModel):
    user: str
    password: str
    host: str
    port: Union[int, str] = Field(coerce_numbers_to_str=True)
    uri: Optional[Union[PostgresDsn, Url, AmqpDsn, MultiHostUrl]] = Field(
        default=None, validate_default=False
    )

    @model_validator(mode="before")
    @classmethod
    def check_uri_omitted(cls, data: Any) -> Any:
        if isinstance(data, dict) and "uri" in data:
            raise PydanticCustomError(
                UriPassedToInitError.error_type, UriPassedToInitError.message
            )
        return data


class ConnectionStringTimescaleDb(BaseConnectionString):
    @model_validator(mode="after")
    def create_uri(self) -> Self:
        self.uri = MultiHostUrl.build(
            scheme="postgres",
            username=self.user,
            password=self.password,
            host=self.host,
            port=int(self.port),
        )
        return self


class EventStoreDBConnectionString(BaseConnectionString):
    tls: bool

    @model_validator(mode="after")
    def create_uri(self) -> Self:
        if self.tls:
            self.uri = Url.build(
                scheme="esdb",
                username=self.user,
                password=self.password,
                host=self.host,
                port=int(self.port),
                query="tls=true",
            )
        else:
            self.uri = Url.build(
                scheme="esdb",
                host=self.host,
                port=int(self.port),
                query="tls=false",
            )
        return self


class RabbitMQConnectionString(BaseConnectionString):
    @model_validator(mode="after")
    def create_uri(self) -> Self:
        self.uri = Url.build(
            scheme="amqp",
            username=self.user,
            password=self.password,
            host=self.host,
            port=int(self.port),
        )
        return self
