import time
from . import cypher


def state_result(res):
    return {"metadata": res["state_rel"].properties, "properties": res["entity_state"].properties}


def current_timestamp():
    return int(round(time.time() * 1000))


def link_result(res):
    return {"metadata": res["link_rel"].properties, "curie": res["labels"][0] + ":" + res["linked_public_id"]}


def get_states_map(public_id, entities_by_id):
    if public_id in entities_by_id:
        return entities_by_id[public_id]
    else:
        states_by_id = {}
        entities_by_id[public_id] = states_by_id
        return states_by_id


def get_links_map(public_id, entities_by_id):
    if public_id in entities_by_id:
        return entities_by_id[public_id]
    else:
        links_by_id = {}
        entities_by_id[public_id] = links_by_id
        return links_by_id


class RegistryService:
    def __init__(self, driver, redis_client):
        self.graphdb_driver = driver
        self.redis_client = redis_client

    def find_register(self, register, page_size):
        entity_query = cypher.register_query_template.format(register)
        entities_by_id = {}
        session = self.graphdb_driver.session()
        results = session.run(entity_query, {"page_size": page_size})
        for result in results:
            public_id = result["public_id"]
            states_by_id = get_states_map(public_id, entities_by_id)
            state_id = result["state_id"]
            state = state_result(result)
            states_by_id[state_id] = state
            link_id = result["link_id"]
            link = link_result(result)
            links_by_id = get_links_map(public_id, entities_by_id)
            links_by_id[link_id] = link
        session.close()
        return entities_by_id

    def find_record_by_id(self, register, public_id):
        entity_query = cypher.entity_query_template.format(register)
        states_by_id = {}
        links_by_id = {}
        session = self.graphdb_driver.session()
        results = session.run(entity_query, {"public_id": public_id})
        for result in results:
            state_id = result["state_id"]
            state = state_result(result)
            states_by_id[state_id] = state
            link_id = result["link_id"]
            link = link_result(result)
            links_by_id[link_id] = link
        session.close()
        states = list(states_by_id.values())
        links = list(links_by_id.values())
        if len(states) > 0:
            return {"public_id": public_id, "history": states, "links": links}
        else:
            return None

    def find_state_by_time(self, register, public_id, timestamp):
        state_query = cypher.state_by_time_query_template.format(register)
        states_by_id = {}
        links_by_id = {}
        session = self.graphdb_driver.session()
        results = session.run(state_query, {"public_id": public_id, "timestamp": timestamp})
        for result in results:
            state_id = result["state_id"]
            state = state_result(result)
            states_by_id[state_id] = state
            link_id = result["link_id"]
            link = link_result(result)
            links_by_id[link_id] = link
        session.close()
        states = list(states_by_id.values())
        links = list(links_by_id.values())
        if len(states) == 1:
            return {"public_id": public_id, "state": state, "links": links}
        elif len(states) == 0:
            return None
        else:
            raise RuntimeError.new("Multiple states found for timestamp " + str(timestamp))

    def find_state_by_entry_number(self, register, public_id, entry_number):
        state_query = cypher.state_by_entry_query_template.format(register)
        session = self.graphdb_driver.session()
        states = []
        results = session.run(state_query, {"public_id": public_id, "entry_number": entry_number})
        for result in results:
            states.append(state_result(result))
        session.close()
        if len(states) == 1:
            return {"public_id": public_id, "state": states[0]}
        elif len(states) == 0:
            return None
        else:
            raise RuntimeError.new("zzz")

    def create_state(self, register, public_id, state):
        state_query = cypher.create_state_query_template.format(register)
        entry_number = self.next_entry_number(register)
        created = current_timestamp()
        session = self.graphdb_driver.session()
        results = session.run(state_query, {"public_id": public_id, "from":
            state["from"], "to": state["to"], "created": created,
                                            "entry_number": entry_number, "properties": state["properties"]})
        results.consume()
        session.close()
        extra_state = {"entry_number": entry_number, "created": created}
        return {**state, **extra_state}

    def next_entry_number(self, register):
        return self.redis_client.incr(register + ':max_entry')
