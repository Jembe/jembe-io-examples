from typing import TYPE_CHECKING, Callable, Dict, Iterable, Optional, Tuple, Union
from uuid import uuid4
from jembe import Component, listener
from jembe.common import ComponentRef

if TYPE_CHECKING:
    from jembe import ComponentConfig, ComponentRef, RedisplayFlag

__all__ = ("CNotifications",)


class CNotifications(Component):
    class Config(Component.Config):
        default_template = "components/notifications.html"

        def __init__(
            self,
            template: Optional[Union[str, Iterable[str]]] = None,
            components: Optional[Dict[str, "ComponentRef"]] = None,
            inject_into_components: Optional[
                Callable[["Component", "ComponentConfig"], dict]
            ] = None,
            redisplay: Tuple["RedisplayFlag", ...] = (),
            changes_url: bool = False,
            url_query_params: Optional[Dict[str, str]] = None,
        ):
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

    def __init__(self, notifications: Optional[Dict[str, Optional[Tuple[str, str]]]] = None) -> None:
        if notifications is not None:
            # remove notifications id where notification[id] == None
            self.state.notifications = {
                id: n for id, n in notifications.items() if n is not None
            }
        else:
            self.state.notifications = dict()

        super().__init__()

    @listener(event="pushNotification")
    def on_push_notification(self, event):
        self.state.notifications[str(uuid4())] = (
            event.params.get("message", ""),
            event.params.get("level", "info")
        )
