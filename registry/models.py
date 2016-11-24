from neo4j.v1 import GraphDatabase, basic_auth
from .cypher import state_query_template, link_query_template, state_by_time_query_template, link_by_time_query_template
import os

url = os.environ.get('GRAPHENEDB_BOLT_URL', 'bolt://localhost')
user = os.environ.get('GRAPHENEDB_BOLT_USER','neo4j')
password = os.environ.get('GRAPHENEDB_BOLT_PASSWORD')

driver = GraphDatabase.driver(url, auth=basic_auth(user, password))

def find_record_by_id(register, public_id):
    state_query = state_query_template.format(register)
    link_query = link_query_template.format(register)
    states = []
    links = []
    session = driver.session()
    state_results = session.run(state_query, {"public_id": public_id})
    for res in state_results:
        state = { "from": res["from"], "to": res["to"], "properties": res["entity_state"].properties }
        states.append(state)
    link_results = session.run(link_query, {"public_id": public_id})
    for res in link_results:
        link = { "from": res["from"], "to": res["to"], "curie": res["related_register"] + ":" + res["related_id"] }
        links.append(link)
    session.close()
    return {"public_id": public_id, "history": states, "links": links}


def find_record_by_year(register, public_id, year):
    state_query = state_by_time_query_template.format(register)
    link_query = link_by_time_query_template.format(register)
    states = []
    session = driver.session()
    results = session.run(state_query, {"public_id": public_id, "year": year})
    for res in results:
        state = { "from": res["from"], "to": res["to"], "properties": res["entity_state"].properties }
        states.append(state)
    session.close()
    return {"public_id": public_id, "current_state": states[0]}
