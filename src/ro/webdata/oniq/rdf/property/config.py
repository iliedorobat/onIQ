from ro.webdata.oniq.rdf.namespace.constants import NS_DC, NS_DC_TERMS

PROPERTIES_TYPE = {
    "AGE": [],
    "PLACE": [],
    "TIMESPAN": [
        {"ns_name": NS_DC, "prop_name": "date"},
        {"ns_name": NS_DC_TERMS, "prop_name": "issued"}
    ]
}
