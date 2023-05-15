from typing import List

from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.final_triples.Triple import Triple
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class SPARQLQuery:
    def __init__(self, targets: List[NounEntity], triples: List[Triple]):
        self.targets = targets
        self.triples = triples

    def __str__(self):
        output = "SELECT"
        for target in self.targets:
            output += f" {target.to_var()}"

        output += "\nWHERE {"
        for triple in self.triples:
            output += f"\n\t{str(triple)} ."
        output += "\n}"

        return output


class SPARQLRawQuery:
    def __init__(self, targets: List[NounEntity], raw_triples: List[RawTriple]):
        self.targets = targets
        self.raw_triples = raw_triples

    def __str__(self):
        output = "target_nouns = [\n"
        for target in self.targets:
            output += f"\t{target.to_var()}\n"
        output += "]\n"

        output += "raw_triples = [\n"
        for raw_triple in self.raw_triples:
            output += f"\t<{str(raw_triple)}>\n"
        output += "]"

        return output
