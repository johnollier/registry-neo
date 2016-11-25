from neo4j.v1 import GraphDatabase, basic_auth
import redis
from flask import Flask, jsonify, make_response, request, url_for, abort
import time
import os
from .registry import RegistryService

app = Flask(__name__)

max_page_size = 500

url = os.environ.get('GRAPHENEDB_BOLT_URL', 'bolt://localhost')
user = os.environ.get('GRAPHENEDB_BOLT_USER', 'neo4j')
password = os.environ.get('GRAPHENEDB_BOLT_PASSWORD', 'password')
driver = GraphDatabase.driver(url, auth=basic_auth(user, password))

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', '6379')
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

registry_service = RegistryService(driver, redis_client)


@app.route('/<register>', methods=['GET'])
def find_register(register):
    page_size = request.args.get("page-size")
    if page_size is None or page_size > max_page_size:
        page_size = 100
    register = registry_service.find_register(register, page_size)
    if register is None:
        abort(404)
    return jsonify(register)


@app.route('/<register>/state', methods=['GET'])
def find_register_state(register):
    page_size = request.args.get("page-size")
    if page_size is None or page_size > max_page_size:
        page_size = 100
    timestamp = request.args.get("time")
    if timestamp is None:
        timestamp = current_timestamp()
    register = registry_service.find_register_state(register, page_size, timestamp)
    if register is None:
        abort(404)
    return jsonify(register)


@app.route('/<register>/<public_id>', methods=['GET'])
def find_record(register, public_id):
    record = registry_service.find_record_by_id(register, public_id)
    if record is None:
        abort(404)
    return jsonify(record)


@app.route('/<register>/<public_id>/state', methods=['GET'])
def find_state_by_time(register, public_id):
    timestamp = request.args.get("time")
    if timestamp is None:
        timestamp = current_timestamp()
    entity_state = registry_service.find_state_by_time(register, public_id, int(timestamp))
    if entity_state is None:
        abort(404)
    return jsonify(entity_state)


@app.route('/<register>/<public_id>/state/<int:entry>', methods=['GET'])
def find_state_by_entry(register, public_id, entry):
    entity_state = registry_service.find_state_by_entry_number(register, public_id, entry)
    if entity_state is None:
        abort(404)
    return jsonify(entity_state)


@app.route('/<register>/<public_id>/state', methods=['POST'])
def create_state(register, public_id):
    # TODO validation
    if not request.json:
        abort(400)
    state = {
        'from': request.json['from'],
        'to': request.json['to'],
        'properties': request.json['properties'],
    }
    state_url = url_for("find_record_by_entry", register=register, public_id=public_id, entry=0)
    full_state = registry_service.create_state(register, public_id, state)
    return jsonify(full_state), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def current_timestamp():
    return int(round(time.time()))
