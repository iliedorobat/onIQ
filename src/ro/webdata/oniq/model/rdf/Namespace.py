from ro.webdata.oniq.common.rdf_ns_utils import get_ns_label, get_ns_name


class Namespace:
    def __init__(self, uri):
        self.name = get_ns_name(uri)
        self.label = get_ns_label(self.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            # only equality tests to other 'Namespace' instances are supported
            return NotImplemented
        return self.name == other.name
