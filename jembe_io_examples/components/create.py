from typing import TYPE_CHECKING, Optional, Type, Union, Iterable, Dict, Callable, Tuple, Any
from jembe import Component, run_only_once, action
from .form import FormBase
import sqlalchemy as sa

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy, Model
    from jembe import RedisplayFlag, ComponentConfig, ComponentRef

__all__ = ("CCreate",)

class CCreate(Component):
    class Config(Component.Config):
        default_template = "components/create.html"

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
    _config:Config

    def __init__(self, form: Optional[FormBase] = None):
        super().__init__()

    @classmethod
    def load_init_param(cls, config: "ComponentConfig", name: str, value: Any) -> Any:
        if name == "form":
            # otherwise it will use FormBase.load_init_param
            return config.form.load_init_param(value)
        return super().load_init_param(config, name, value)


    @run_only_once
    def mount(self):
        if self.state.form is None:
            self.state.form = self._config.form(obj=self._config.model())
        self.state.form.mount(self)

    @action
    def save(self):
        self.mount()
        if self.state.form.validate():
            try:
                record = self._config.model()
                self.state.form.populate_obj(record)
                self._config.db.session.add(record)
                self._config.db.session.commit()
                self.emit("save", record=record, id=record.id)
                self.emit(
                    "pushNotification", message="{} saved".format(str(record))
                )
                # don't execute display after sucessfull save
                return False
            except sa.exc.SQLAlchemyError as error:
                self.emit(
                    "pushNotification",
                    message=str(getattr(error, "orig", error)),
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
        return "Create {}".format(self._config.model.__name__)
