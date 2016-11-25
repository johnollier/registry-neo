from neo4j.v1 import GraphDatabase, basic_auth
import os

url = os.environ.get('GRAPHENEDB_BOLT_URL', 'bolt://localhost')
user = os.environ.get('GRAPHENEDB_BOLT_USER','neo4j')
password = os.environ.get('GRAPHENEDB_BOLT_PASSWORD', 'password')

driver = GraphDatabase.driver(url, auth=basic_auth(user, password))

session = driver.session()
session.run("match (n) detach delete n")
session.close()
	 
