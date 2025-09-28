from __future__ import annotations

from dataclasses import is_dataclass, fields
from collections.abc import Iterable


class ClassHelper:

    @staticmethod
    def snapshot_state(
        obj: object,
        /,
        *,
        include_private: bool = False,
        include_dunder: bool = False,
        include_callables: bool = False,
        include_properties: bool = True,
    ) -> dict[str, object]:
        result: dict[str, object] = {}

        if is_dataclass(obj):
            result.update(ClassHelper._attrs_from_dataclass(obj))

        inst_attrs = ClassHelper._attrs_from_instance(
            obj,
            include_private=include_private,
            include_dunder=include_dunder,
            include_callables=include_callables,
        )
        result.update(inst_attrs)

        if include_properties:
            prop_vals = ClassHelper.property_values(
                obj,
                names=None,
                include_private=include_private,
                include_dunder=include_dunder,
            )
            result.update(prop_vals)

        return result

    @staticmethod
    def _attrs_from_dataclass(obj: object) -> dict[str, object]:
        out: dict[str, object] = {}
        # noinspection PyDataclass
        for f in fields(obj):  # type: ignore[arg-type]  # mypy: fields()
            fname = f.name
            try:
                out[fname] = getattr(obj, fname)
            except Exception:
                continue
        return out

    @staticmethod
    def _attrs_from_instance(
        obj: object,
        *,
        include_private: bool,
        include_dunder: bool,
        include_callables: bool,
    ) -> dict[str, object]:

        names: set[str] = set()

        if hasattr(obj, "__dict__"):
            for keys in vars(obj):
                names.add(keys)

        for slot_name in ClassHelper._slot_names(type(obj)):
            names.add(slot_name)

        out: dict[str, object] = {}
        for name in names:
            if not include_dunder and ClassHelper._is_dunder(name):
                continue
            if not include_private and ClassHelper._is_private(name):
                continue

            try:
                val = getattr(obj, name)
            except Exception:
                continue

            if not include_callables and callable(val):
                continue

            out[name] = val

        return out

    @staticmethod
    def _slot_names(type_obj: type[object]) -> set[str]:
        names: set[str] = set()
        for base in type_obj.__mro__:
            if "__slots__" not in base.__dict__:
                continue
            raw = base.__dict__["__slots__"]
            if isinstance(raw, str):
                names.add(raw)
            else:
                try:
                    for s in raw:
                        if isinstance(s, str):
                            names.add(s)
                except TypeError:
                    continue
        return names

    @staticmethod
    def property_names(
        type_obj: type[object],
        *,
        include_private: bool = False,
        include_dunder: bool = False,
    ) -> list[str]:
        found: list[str] = []
        seen: set[str] = set()
        for base in type_obj.__mro__:
            for name, attr in base.__dict__.items():
                if name in seen:
                    continue
                if not include_dunder and ClassHelper._is_dunder(name):
                    continue
                if not include_private and ClassHelper._is_private(name):
                    continue
                if isinstance(attr, property):
                    found.append(name)
                    seen.add(name)
        return found

    @staticmethod
    def property_values(
        obj: object,
        *,
        names: Iterable[str] | None = None,
        include_private: bool = False,
        include_dunder: bool = False,
    ) -> dict[str, object]:
        cls = type(obj)
        prop_names = (
            list(names)
            if names is not None
            else ClassHelper.property_names(
                cls,
                include_private=include_private,
                include_dunder=include_dunder,
            )
        )

        out: dict[str, object] = {}
        for name in prop_names:
            try:
                out[name] = getattr(obj, name)
            except Exception:
                continue
        return out

    @staticmethod
    def _is_dunder(name: str) -> bool:
        return name.startswith("__") and name.endswith("__")

    @staticmethod
    def _is_private(name: str) -> bool:
        return name.startswith("_") and not ClassHelper._is_dunder(name)
