from typing import Any, TYPE_CHECKING
from abc import ABCMeta
from wtforms.form import Form, FormMeta
from jembe import JembeInitParamSupport

if TYPE_CHECKING:
    from jembe import Component


__all__ = ("FormBase",)

class FormBaseMeta(FormMeta, ABCMeta):
    pass

class FormBase(JembeInitParamSupport, Form, metaclass=FormBaseMeta):
    """Add support for using form as jembe component init/state param"""
    @classmethod
    def dump_init_param(cls, value: Any) -> Any:
        return value.data if value is not None else dict()

    @classmethod
    def load_init_param(cls, value: Any) -> Any:
        return cls(data=value)

    def mount(self, component:"Component") -> "FormBase":
        """Runs after form is initialised by CEdit compoent"""
        return self 