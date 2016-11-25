from neo4j.v1 import GraphDatabase, basic_auth
import os
import sys

url = os.environ.get('GRAPHENEDB_BOLT_URL', 'bolt://localhost')
user = os.environ.get('GRAPHENEDB_BOLT_USER','neo4j')
password = os.environ.get('GRAPHENEDB_BOLT_PASSWORD','password')

driver = GraphDatabase.driver(url, auth=basic_auth(user, password))

session = driver.session()

cypher_file = sys.argv[1]

with open(cypher_file) as command_file :
    commands = command_file.read()
    command_arr = commands.split(";")
    for c in command_arr:
        print(c)
        session.run(c)

session.close()
