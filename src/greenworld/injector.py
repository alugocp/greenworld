from typing import Dict

# This class registers service instances and handles dependency injection.
class Injector:
    services: Dict[str, object] = {}

    def register_service(self, name: str, service) -> None:
        if name in self.services:
            raise RuntimeError(f'Service \'{name}\' is already registered')
        self.services[name] = service

    def remove_service(self, name: str) -> None:
        if name not in self.services:
            raise RuntimeError(f'Service \'{name}\' is not registered')
        del self.services[name]

    def get_service(self, name: str) -> object:
        if name not in self.services:
            raise RuntimeError(f'Service \'{name}\' is not registered')
        return self.services[name]