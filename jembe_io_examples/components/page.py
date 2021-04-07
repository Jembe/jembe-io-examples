from typing import TYPE_CHECKING, Callable, Dict, Iterable, Optional, Tuple, Union
from functools import cached_property
from jembe import Component, listener
from .notifications import CNotifications

if TYPE_CHECKING:
    from jembe import ComponentRef, ComponentConfig, RedisplayFlag, Event

__all__ = ("CPage",)


class CPage(Component):
    class Config(Component.Config):
        def __init__(
            self,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["Component", "ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["RedisplayFlag", ...] = (),
            changes_url: bool = True,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
            self.default_template = "components/page.html"
            if template is None:
                template = ("", self.default_template)

            if components is None:
                components = dict()

            if "_notifications" not in components:
                components["_notifications"] = CNotifications

            super().__init__(
                template=template,
                components=components,
                inject_into_components=inject_into_components,
                redisplay=redisplay,
                changes_url=changes_url,
                url_query_params=url_query_params,
            )

        @cached_property
        def supported_display_modes(self) -> Tuple[str, ...]:
            return tuple(
                name
                for name in self.components_configs.keys()
                if not name.startswith("_")
            )

        @cached_property
        def default_display_mode(self) -> Optional[str]:
            try:
                return self.supported_display_modes[0]
            except IndexError:
                return None

    _config: Config

    def __init__(self, display_mode: Optional[str] = None):
        if (
            display_mode is None
            or display_mode not in self._config.supported_display_modes
        ):
            self.state.display_mode = self._config.default_display_mode
        super().__init__()

    @listener(event="_display", source="./*")
    def on_child_display(self, event:"Event"):
        if event.source_name in self._config.supported_display_modes:
            self.state.display_mode = event.source_name
