from functools import cached_property
from typing import TYPE_CHECKING, Optional, Tuple

from jembe import listener
from .list_records import CListRecords
from .edit import CEdit
from .view import CView
from .create import CCreate
from .delete import CDelete

if TYPE_CHECKING:
    from jembe import Event


__all__ = ("CCrudListRecords",)


class CCrudListRecords(CListRecords):
    class Config(CListRecords.Config):
        default_template = "components/crud_list_records.html"
        super_default_template = CListRecords.Config.default_template

        @cached_property
        def supported_display_modes(self) -> Tuple[str, ...]:
            return tuple(
                name
                for name, cclass in self.components_classes.items()
                if issubclass(cclass, (CEdit, CCreate, CView))
                and not name.startswith("_")
            )

        @cached_property
        def default_view_display_mode(self) -> Optional[str]:
            return next(
                (
                    name
                    for name, cclass in self.components_classes.items()
                    if issubclass(cclass, CView) and not name.startswith("_")
                ),
                None,
            )

        @cached_property
        def delete_names(self) -> Tuple[str, ...]:
            return tuple(
                name
                for name, cclass in self.components_classes.items()
                if issubclass(cclass, CDelete)
            )

    _config: Config

    def __init__(
        self, search: str = "", page: int = 0, display_mode: Optional[str] = None
    ):
        super().__init__(search=search, page=page)

        self.goto_id: Optional[int] = None
        self.display_delete: Optional[Tuple[str, int]] = None

        if (
            display_mode is not None
            and display_mode not in self._config.supported_display_modes
        ):
            self.state.display_mode = None

    @listener(event="_display", source="./*")
    def on_display_child(self, event: "Event"):
        if event.source_name in self._config.supported_display_modes:
            self.state.display_mode = event.source_name
        elif event.source_name in self._config.delete_names:
            self.display_delete = (event.source_name, event.source.state.id)
            return True

    @listener(event="cancel", source="./*")
    def on_cancel_child(self, event: "Event"):
        if event.source_name in self._config.supported_display_modes:
            self.state.display_mode = None
        elif event.source_name in self._config.delete_names:
            # force redisplay in order to remove delete dialog
            return True

    @listener(event="delete", source="./*")
    def on_delete_child(self, event: "Event"):
        if event.source_name in self._config.delete_names:
            # force redisplay in order to remove delete dialog and redisplay list
            # without deleted record
            return True

    @listener(event="save", source="./*")
    def on_save_child(self, event: "Event"):
        if event.source_name in self._config.supported_display_modes:
            if event.params.get("id", None):
                self.goto_id = event.id
                self.state.display_mode = self._config.default_view_display_mode
            else:
                self.state.display_mode = None

    def display(self):
        if self.state.display_mode is None:
            return super().display()
        else:
            # skip quering database for list if
            # list is not displayed
            return self.render_template()
