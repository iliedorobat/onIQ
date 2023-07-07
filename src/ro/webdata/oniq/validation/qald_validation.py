import json

from ro.webdata.oniq.endpoint.common.path_utils import get_questions_file_path
from ro.webdata.oniq.endpoint.dbpedia.sparql_query import DBP_ENDPOINT
from ro.webdata.oniq.endpoint.query import QueryService
from ro.webdata.oniq.sparql.builder.builder import SPARQLBuilder


def load_questions(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["questions"]


def create_entry(qald_entry, query, result):
    return {
        "id": qald_entry["id"],
        "question": qald_entry["question"],
        "query": {
            "sparql": query
        },
        "answers": [result]
    }


def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_qald_8_test():
    entries = []
    filepath = get_questions_file_path("qald-8-test-multilingual")
    questions = load_questions(filepath)

    for qald_entry in questions:
        en_question = qald_entry["question"][0]["string"]
        query = ""
        result = []
        print(f"en_question:   <id: {qald_entry['id']}>   <{en_question}>")

        try:
            builder = SPARQLBuilder(DBP_ENDPOINT, en_question, False)
            query = builder.to_sparql_query()
            result = QueryService.run_query(DBP_ENDPOINT, query)
            print(f"QUESTION <{qald_entry['id']}> PASSED")
        except:
            print(f"QUESTION <{qald_entry['id']}> FAILED")

        entry = create_entry(qald_entry, query, result)
        entries.append(entry)

    return {
        "questions": entries
    }


def run_qald_8_test():
    filePath = get_questions_file_path("qald-8-test-multilingual_results")
    data = get_qald_8_test()
    save_data(filePath, data)
