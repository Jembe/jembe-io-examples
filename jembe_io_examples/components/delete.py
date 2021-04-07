from functools import cached_property
from typing import TYPE_CHECKING, Optional, Type, Union, Iterable, Dict, Callable, Tuple
from jembe import Component, run_only_once, action

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy, Model
    from jembe import RedisplayFlag, ComponentConfig, ComponentRef
    import sqlalchemy as sa

__all__ = ("CDelete",)


class CDelete(Component):
    class Config(Component.Config):
        default_template = "components/delete.html"

        def __init__(
            self,
            db: "SQLAlchemy",
            model: "Model",
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["Component", "ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["RedisplayFlag", ...] = (),
            changes_url: bool = False,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
            self.db = db
            self.model = model

            if template is None:
                template = ("", self.default_template)

            super().__init__(
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    _config: Config

    def __init__(self, id: int):
        super().__init__()

    @cached_property
    def record(self) -> "Model":
        return self._config.db.session.query(self._config.model).get(self.state.id)

    @action
    def delete_record(self):
        try:
            self._config.db.session.delete(self.record)
            self._config.db.session.commit()
            self.emit("delete", record=self.record, id=self.record.id)
            self.emit(
                "pushNotification", message="{} deleted".format(str(self.record))
            )
        except sa.exc.SQLAlchemyError as error:
            self._config.db.session.rollback()
            self.emit(
                "pushNotification",
                message=str(getattr(error, "orig", error)),
                level="error",
            )
        # don't execute display after sucessfull or unsucessfull delete
        return False

    @action
    def cancel(self):
        self.emit("cancel")
        # force not redisplaying this Delete component
        return False

    @property
    def title(self):
        return str(self.record)
