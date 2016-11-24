import time
import datetime
import hashlib
import json
import os
import codecs

def print_err(s):
    print(s, file=sys.stderr)


def timestamp():
    return datetime.datetime.now().isoformat()


def extract_content_map(line, fields):
    content_map = {"meta:creation_date": timestamp() }
    parts = line.split("\t")
    for i in range(len(parts)):
        if len(parts[i].strip()) > 0:
            content_map[fields[i]] = parts[i]
    return content_map


def process_line(line, fields, reg_name):
    content_map = extract_content_map(line, fields)
    entity_id = content_map[reg_name]
    content_json = json.dumps(content_map)
    print(content_json)
    entity_line = 'CREATE (hod:local_authority_eng { public_id:"hod"})'
    state_line = "x"
    print(entity_line)
    print(state_line)


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
        for line in csv_file:
            process_line(line.strip("\n"), fields, reg_name)
            if line_num % 10000 == 0:
                print_err("lines processed: " + str(line_num))
            line_num += 1
        csv_file.close()

    print_err("finished: " + time.asctime(time.localtime(time.time())))


main()
