from .logger import Logger

class ResourceManager:
    def __init__(self, resource_wrapper, resources):
        self._resource_wrapper = resource_wrapper
        self._resource_map = {}
        for k, r in resources.items():
            Logger.log(f"Loading resource {repr(k)}")
            self.add_resource(k, r)

    def add_resource(self, key, resource):
        self._resource_map[key] = self._resource_wrapper(resource)

    def get(self, key):
        result = self._resource_map.get(key)
        if result is None:
            raise ValueError(f"could not find resource of ID #{repr(key)}")
        else:
            return result
