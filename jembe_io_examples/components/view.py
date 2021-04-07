from functools import cached_property
from typing import TYPE_CHECKING, Optional, Type, Union, Iterable, Dict, Callable, Tuple
from jembe import Component, run_only_once, action
from .form import FormBase

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy, Model
    from jembe import RedisplayFlag, ComponentConfig, ComponentRef
    import sqlalchemy as sa

__all__ = ("CView",)


class CView(Component):
    class Config(Component.Config):
        default_template = "components/view.html"

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

    _config: Config

    def __init__(self, id: int):
        super().__init__()

    @cached_property
    def record(self) -> "Model":
        return self._config.db.session.query(self._config.model).get(self.state.id)

    @action
    def cancel(self):
        self.emit("cancel")
        # force not redisplaying this edit component
        return False

    def display(self):
        self.form = self._config.form(obj=self.record).mount(self)
        return super().display()

    @property
    def title(self):
        return "View: {}".format(self.record)
