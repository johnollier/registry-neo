register_query_template = '''
    MATCH (e: {0})-[sr:STATE]->(es)
    OPTIONAL MATCH (e)-[lr]->(le)
    WHERE type(lr)<>'STATE'
    RETURN e.public_id as public_id, id(es) as state_id, sr as state_rel, es as entity_state, id(le) as link_id,
    lr as link_rel, le.public_id as linked_public_id, labels(le) as labels
    ORDER BY public_id
    LIMIT {{page_size}}'''

entity_query_template = '''
    MATCH (e: {0})-[sr:STATE]->(es)
    WHERE e.public_id={{public_id}}
    OPTIONAL MATCH (e)-[lr]->(le)
    WHERE type(lr)<>'STATE'
    RETURN id(es) as state_id, sr as state_rel,es as entity_state, id(le) as link_id,lr as link_rel,
    le.public_id as linked_public_id, labels(le) as labels
    ORDER BY sr.from'''

state_by_time_query_template = '''
    MATCH (e: {0})-[sr:STATE]->(es)
    WHERE e.public_id={{public_id}}
    AND sr.from < {{timestamp}} AND sr.to > {{timestamp}}
    OPTIONAL MATCH (e)-[lr]->(le)
    WHERE type(lr)<>'STATE'
    AND lr.from < {{timestamp}} AND lr.to > {{timestamp}}
    RETURN id(es) as state_id, sr as state_rel,es as entity_state, id(le) as link_id,lr as link_rel,
    le.public_id as linked_public_id, labels(le) as labels
    ORDER BY sr.from'''

state_by_entry_query_template = '''
    MATCH (entity: {0} {{public_id: {{public_id}} }})-[state_rel:STATE]->(entity_state)
    WHERE state_rel.entry_number = {{entry_number}}
    RETURN state_rel, entity_state'''

create_state_query_template = '''
    MATCH (entity: {0} {{public_id: {{public_id}} }})
    CREATE (entity_state: {0}_state {{ properties }})
    CREATE (entity)-[:STATE {{`from`: {{from}}, `to`: {{to}}, `created`: {{created}},
    `entry_number`: {{entry_number}} }}]->(entity_state)'''
