import warnings

from ro.webdata.oniq.endpoint.namespace import NamespaceService


class Namespace:
    # TODO: remove
    warnings.warn("Deprecated in favour or RDFClass", PendingDeprecationWarning)

    def __init__(self, uri):
        self.name = NamespaceService.get_namespace(uri)
        self.label = NamespaceService.get_ns_label(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            # only equality tests to other 'Namespace' instances are supported
            return NotImplemented
        return self.name == other.name
