from __future__ import annotations

from typing import Any

from sentry.plugins.providers import IntegrationRepositoryProvider, RepositoryProvider


class ProviderManager:
    type: type[Any] | None = None

    def __init__(self):
        self._items = {}

    def __iter__(self):
        return iter(self._items)

    def add(self, item, id):
        if self.type and not issubclass(item, self.type):
            raise ValueError(f"Invalid type for provider: {type(item)}")

        self._items[id] = item

    def get(self, id):
        return self._items[id]

    def all(self):
        return self._items.items()


class RepositoryProviderManager(ProviderManager):
    type = RepositoryProvider


class IntegrationRepositoryProviderManager(ProviderManager):
    type = IntegrationRepositoryProvider


class BindingManager:
    BINDINGS = {
        "repository.provider": RepositoryProviderManager,
        "integration-repository.provider": IntegrationRepositoryProviderManager,
    }

    def __init__(self):
        self._bindings = {k: v() for k, v in self.BINDINGS.items()}

    def add(self, name, binding, **kwargs):
        self._bindings[name].add(binding, **kwargs)

    def get(self, name):
        return self._bindings[name]
