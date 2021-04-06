from functools import cached_property
from typing import TYPE_CHECKING, Optional, Type, Union, Iterable, Dict, Callable, Tuple
from jembe import Component, run_only_once, action

if TYPE_CHECKING:
    from .form import FormBase
    from flask_sqlalchemy import SQLAlchemy, Model
    from jembe import RedisplayFlag, ComponentConfig, ComponentRef
    import sqlalchemy as sa

__all__ = ("CEdit",)


class CEdit(Component):
    class Config(Component.Config):
        def __init__(
            self,
            db: "SQLAlchemy",
            form: Type["FormBase"],
            model: "Model",
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["Component", "ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["RedisplayFlag", ...] = (),
            changes_url: bool = True,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
            self.db = db
            self.form = form
            self.model = model

            super().__init__(
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

    def __init__(self, id: int, form: Optional["FormBase"] = None):
        super().__init__()

    @cached_property
    def record(self) -> "Model":
        return self._config.db.session.query(self._config.model).get(self.state.id)

    @run_only_once
    def mount(self):
        if self.state.form is None:
            self.state.form = self._config.form(obj=self.record)
        self.state.form.mount(self)

    @action
    def save(self):
        self.mount()
        if self.state.form.validate():
            try:
                self.state.form.populate_obj(self.record)
                self._config.db.session.commit()
                self.emit("save", record=self.record, id=self.record.id)
                self.emit(
                    "pushNotification", notification="{} saved".format(str(self.record))
                )
                # don't execute display after sucessfull save
                return False
            except sa.exc.SQLAlchemyError as error:
                self.emit(
                    "pushNotification",
                    notification=str(getattr(error, "orig", error)),
                    level="error",
                )

        self._config.db.session.rollback()
        # force redisplay of this edit component
        return True

    @action
    def cancel(self):
        self.emit("cancel")
        # force not redisplaying this edit component
        return False

    def display(self):
        self.mount()
        return super().display()

    @property
    def title(self):
        return str(self.record)
