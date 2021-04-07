from typing import TYPE_CHECKING, Optional, Union, Iterable, Dict, Callable, Tuple
from functools import partial
from math import ceil
from jembe import Component
from flask_sqlalchemy import SQLAlchemy

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy, Model
    from jembe import RedisplayFlag, ComponentConfig, ComponentRef
    import sqlalchemy as sa

__all__ = ("CListRecords",)


class CListRecords(Component):
    class Config(Component.Config):
        default_template = "components/list_records.html"
        def __init__(
            self,
            db: "SQLAlchemy",
            query: "sa.orm.Query",
            search_filter: Optional[
                Callable[[str], "sa.sql.expression.Operators"]
            ] = None,
            actions: Iterable[
                Callable[["CListRecords"], Tuple[str, str]]
            ] = (),
            record_actions: Iterable[
                Callable[["CListRecords", "Model"], Tuple[str, str]]
            ] = (),
            page_size: int = 10,
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
            self.query = query
            self.search_filter = search_filter
            self.actions = actions
            self.record_actions = record_actions
            self.page_size = page_size

            if url_query_params is None:
                url_query_params = dict()
            if "page" not in url_query_params.values():
                url_query_params["p"] = "page"
            if "search" not in url_query_params.values():
                url_query_params["s"] = "search"

            if template is None:
                # if component specific template does not exist use default one
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

    def __init__(self, search: str = "", page: int = 0):
        super().__init__()

    def display(self):
        self.records = self._config.query.with_session(self._config.db.session())

        # apply search filter
        if self._config.search_filter is not None and self.state.search != "":
            self.records = self.records.filter(
                self._config.search_filter(self.state.search)
            )

        # apply pagination
        self.total_records = self.records.count()
        self.total_pages = ceil(self.total_records / self._config.page_size)
        if self.state.page > self.total_pages - 1:
            self.state.page = self.total_pages - 1
        if self.state.page < 0:
            self.state.page = 0
        self.start_record_index = self.state.page * self._config.page_size
        self.end_record_index = self.start_record_index + self._config.page_size
        if self.end_record_index > self.total_records:
            self.end_record_index = self.total_records
        self.columns = [cd.get("name", None) for cd in self.records.column_descriptions]
        self.records = self.records[self.start_record_index : self.end_record_index]

        # actions
        self.actions = [a(self) for a in self._config.actions]
        self.record_actions = [partial(a, self) for a in self._config.record_actions]

        return super().display()
