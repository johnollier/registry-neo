MATCH (e:local_authority_eng)-[sr:STATE]->(es)
  WHERE e.public_id = 'BAS'
WITH e, sr, es
MATCH (e)-[lr]->(le)
  WHERE type(lr) <> 'STATE'
RETURN id(es), sr, es, lr, le.public_id, labels(le)
  ORDER BY sr.from

MATCH (e:local_authority_eng)-[sr:STATE]->(es)
    OPTIONAL MATCH (e)-[lr]->(le)
    WHERE type(lr)<>'STATE'
    RETURN id(es) as state_id, sr as state_rel,es as entity_state, id(le) as link_id,lr as link_rel,
    le.public_id as linked_public_id, labels(le) as labels
    ORDER BY sr.from
    limit 10