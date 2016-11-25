CREATE (UA:local_authority_type { public_id:"UA"})
CREATE (UA0:local_authority_type_state { `name`:"Unitary authority"})
CREATE (UA)-[:STATE {`from`: 1, `to`: 32472144000 }]->(UA0)
;

MATCH (lat:local_authority_type) WHERE lat.public_id='UA'
MERGE (BAS:local_authority_eng { public_id:"BAS"})
MERGE (BAS0:local_authority_eng_state { `name`:"Bath and North East Somerset", `official_name`:"Bath and North East Somerset Council" })
MERGE (BAS)-[:STATE {`from`: 1, `to`: 32472144000, `created`: 1486144591151, `entry_number`: 1 }]->(BAS0)
MERGE (BAS)-[r:LOCAL_AUTHORITY_TYPE { `from`: 1, `to`: 32472144000 } ]->(lat)
;

MATCH (lat:local_authority_type) WHERE lat.public_id='UA'
MERGE (BBD:local_authority_eng { public_id:"BBD"})
MERGE (BBD0:local_authority_eng_state { `name`:"Blackburn with Darwen", `official_name`:"Blackburn with Darwen Borough Council" })
MERGE (BBD)-[:STATE {`from`: 1, `to`: 32472144000, `created`: 1486144591151, `entry_number`: 2 }]->(BBD0)
MERGE (BBD)-[r:LOCAL_AUTHORITY_TYPE { `from`: 1, `to`: 32472144000 } ]->(lat)
 
