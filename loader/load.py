from neo4j.v1 import GraphDatabase, basic_auth
import os

url = os.environ.get('GRAPHENEDB_BOLT_URL', 'bolt://localhost:7474')
user = os.environ.get('GRAPHENEDB_BOLT_USER','neo4j')
password = os.environ.get('GRAPHENEDB_BOLT_PASSWORD')

driver = GraphDatabase.driver(url, auth=basic_auth(user, password))

session = driver.session()

with open('setup.cql') as command_file :
    commands = command_file.read()
    print(commands)
    session.run(commands)

session.close()
