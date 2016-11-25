import time
from datetime import datetime
import os
import sys
import codecs

def end_of_time():
    return "32472144000"

def beginning_of_time():
    return "1"

def print_err(s):
    print(s, file=sys.stderr)


def timestamp():
    return datetime.now().isoformat()

def timestamp_millis():
    return int(round(time.time() * 1000))


def process_line(line, line_num):
    parts = line.split("\t")

    query_line = "MATCH (lat:local_authority_type) WHERE lat.public_id='{0}'".format(parts[1])
    entity_line = 'MERGE ({0}:local_authority_eng {{ public_id:"{0}"}})'.format( parts[0])
    state_line = 'MERGE ({0}0:local_authority_eng_state {{ `name`:"{1}", `official_name`:"{2}" }})'.format(
            parts[0], parts[2], parts[3] )
    relation_line = 'MERGE ({0})-[:STATE {{`from`: {3}, `to`: {4}, `created`: {1}, `entry_number`: {2} }}]->({0}0)'.format(
         parts[0], timestamp_millis(), line_num, beginning_of_time(), end_of_time())
    link_line = 'MERGE ({2})-[r:LOCAL_AUTHORITY_TYPE {{ `from`: {0}, `to`: {1} }} ]->(lat)'.format(
        beginning_of_time(), end_of_time(), parts[0])

    print(query_line)
    print(entity_line)
    print(state_line)
    print(relation_line)
    print(link_line)
    print("; \n")

def process_line_local_auth_type(line, line_num):
    parts = line.split("\t")
    entity_line = 'CREATE ({0}:local_authority_type {{ public_id:"{0}"}})'.format( parts[0])
    state_line = 'CREATE ({0}0:local_authority_type_state {{ `name`:"{1}"}})'.format(parts[0], parts[1] )
    relation_line = 'CREATE ({0})-[:STATE {{`from`: {1}, `to`: {2} }}]->({0}0)'.format(
        parts[0], beginning_of_time(), end_of_time())
    print(entity_line)
    print(state_line)
    print(relation_line)

def local_auth_types():
    entity_line = 'CREATE (NMD:local_authority_type { public_id:"NMD"})'
    state_line = 'CREATE (NMD0:local_authority_type_state { `name`:"non-metropolian district"})'
    relation_line = 'CREATE (NMD)-[:STATE {{`from`: {0}, `to`: {1} }}]->(NMD0)'.format(
        beginning_of_time(), end_of_time())
    print(entity_line)
    print(state_line)
    print(relation_line)

def main():
    print_err("starting: " + time.asctime(time.localtime(time.time())))
    csv_file_path = sys.argv[1]
    reg_name = sys.argv[2]
    if not os.path.isfile(csv_file_path):
        print_err("error: csv file specified does not exist")
    else:
        csv_file = codecs.open(csv_file_path, "r", "utf-8")
        fields = csv_file.readline().strip("\n").split("\t")
        line_num = 1
        if reg_name == 'local_authority_eng':
            line_processor = process_line
        elif reg_name == 'local_authority_type' :
            line_processor = process_line_local_auth_type
        else:
            print_err("register name not recognised")
            return 1
        for line in csv_file:
            line_processor(line.strip("\n"), line_num)
            line_num += 1
        csv_file.close()

    print_err("finished: " + time.asctime(time.localtime(time.time())))


main()
