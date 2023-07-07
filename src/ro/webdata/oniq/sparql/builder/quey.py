from typing import List

from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_ENDPOINT
from ro.webdata.oniq.endpoint.namespace import NAMESPACE, NamespaceService
from ro.webdata.oniq.endpoint.query import QueryService
from ro.webdata.oniq.sparql.NLQuestion import NLQuestion, ANSWER_TYPE
from ro.webdata.oniq.sparql.NounEntity import NounEntity
from ro.webdata.oniq.sparql.filters.Filters import Filters
from ro.webdata.oniq.sparql.targets.Targets import Targets
from ro.webdata.oniq.sparql.triples.Triple import Triple
from ro.webdata.oniq.sparql.triples.Triples import Triples


class SPARQLQuery:
    @staticmethod
    def get_query(nl_question: NLQuestion, targets: Targets, triples: Triples, filters: Filters):
        target_list: List[NounEntity] = targets.values
        triple_list: List[Triple] = triples.values
        filter_list: List[str] = filters.values

        output = _extract_prefixes(triple_list)

        if nl_question.answer_type == ANSWER_TYPE.BOOL:
            output += "ASK"
        else:
            str_targets_list = [_target_to_str(nl_question, triple_list, target) for target in target_list]
            str_targets = "*" if len(str_targets_list) == 0 else ' '.join(str_targets_list)
            # E.g.: "Who is Dan Jurafsky?" => str_targets == "*"
            output += f"SELECT DISTINCT {str_targets}"

        str_triples = [f"\t{str(triple)}" for triple in triple_list]
        str_filters = [f"\t{str(f)}" for f in filter_list]
        str_where = str_triples + str_filters

        output += "\n"
        output += "WHERE {\n"
        output += " .\n".join(str_where) + "\n"
        output += "}"

        str_ordering_triples = list(
            set([
                f"{str(item.order_by)}"
                for item in triple_list
                if item.is_ordering_triple()
            ])
        )

        if len(str_ordering_triples) > 0:
            output += "\n"
            output += f"ORDER BY {' '.join(str_ordering_triples)}"

        return output


def _target_to_str(nl_question, triple_list: List[Triple], target: NounEntity):
    filtered_list = [triple for triple in triple_list if triple.s == target or triple.o == target]

    if nl_question.answer_type == ANSWER_TYPE.NUMBER:
        if len(filtered_list) > 0:
            triple = filtered_list[0]
            if isinstance(triple.p, PropertyMatcher):
                prop = str(triple.p.property)
            else:
                prop = triple.p

            ranges = QueryService.run_resource_type_range(DBP_ENDPOINT, prop)
            if _is_number(ranges):
                # E.g.: "How much is the population of Mexico City ?"
                return target.to_var()

        return f"COUNT({target.to_var()})"

    return target.to_var()


def _is_number(ranges: List[str]):
    if ranges is None:
        return False

    for range in ranges:
        if _is_single_number(range):
            return True

    return False


# https://help.nintex.com/en-US/k2blackpearl/userguide/4.6.10/XML_Data_Types.html
def _is_single_number(range: str):
    label = range.replace("http://www.w3.org/2001/XMLSchema#", "")

    return label in [
        "unsignedByte",
        "hexBinary",
        "positiveInteger",
        "nonNegativeInteger",
        "int",
        "long",
        "short",
        "decimal",
        "double",
        "byte",
        "hex64Binary",
        "integer",
        "negativeInteger",
        "nonPositiveInteger",
        "unsignedInt",
        "unsignedLong",
        "unsignedShort",
        "float"
    ]


def _extract_prefixes(triples: List[Triple]):
    namespaces = _extract_namespaces(triples)

    output = ""
    for ns in namespaces:
        label = NamespaceService.get_ns_label(ns)
        output += f"PREFIX {label}: <{ns}>\n"

    if len(output) > 0:
        output += "\n"

    return output


def _extract_namespaces(triples: List[Triple]):
    namespaces = []

    for triple in triples:
        if isinstance(triple.p, PropertyMatcher):
            prop = str(triple.p.property)
        else:
            prop = str(triple.p)

        prop_ns = NamespaceService.extract_namespace(prop)
        if prop_ns is not None:
            if prop_ns not in namespaces:
                namespaces.append(prop_ns)

        subject_ns = NamespaceService.extract_namespace(triple.s.to_var())
        if subject_ns is not None:
            if subject_ns not in namespaces:
                namespaces.append(subject_ns)

        obj_ns = NamespaceService.extract_namespace(triple.o.to_var())
        if obj_ns is not None:
            if obj_ns not in namespaces:
                namespaces.append(obj_ns)

    return sorted(
        namespaces,
        key=lambda ns: NamespaceService.get_ns_label(ns)
    )
