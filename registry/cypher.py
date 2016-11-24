
state_query_template = '''
    MATCH (entity: {0} {{public_id: {{public_id}} }})-[state_rel:STATE]->(entity_state)
    RETURN state_rel.from AS from, state_rel.to AS to, entity_state
    ORDER BY state_rel.from'''

link_query_template = '''MATCH (entity: {0} {{public_id: {{public_id}} }})-[rel]->(related_entity)
    WHERE NOT type(rel) = 'STATE'
    RETURN rel.from AS from, rel.to AS to, related_entity.public_id AS related_id,
    labels(related_entity)[0] AS related_register
    ORDER BY rel.from'''


state_by_time_query_template = '''MATCH (entity: {0} {{public_id: {{public_id}} }})-[state_rel:STATE]->(entity_state)
    WHERE state_rel.from < {{year}} AND state_rel.to > {{year}}
    RETURN state_rel.from AS from, state_rel.to AS to, entity_state ORDER BY state_rel.from '''


link_by_time_query_template = '''MATCH (entity: {0} {{public_id: {{public_id}} }})-[rel]->(related_entity)
    WHERE NOT type(rel) = 'STATE' AND  rel.from < {{year}} AND rel.to > {{year}}
    RETURN rel.from AS from, rel.to AS to, related_entity.public_id AS related_id,
    labels(related_entity)[0] AS related_register
    ORDER BY rel.from'''
