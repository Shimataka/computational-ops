class Resources:
    def __init__(self, resource_name: str) -> None:
        self.resource_name: str = resource_name


class SetResources(Resources):
    def __init__(self, resource_name: str) -> None:
        super().__init__(resource_name)


class ListenResources(Resources):
    def __init__(self, resource_name: str) -> None:
        super().__init__(resource_name)
