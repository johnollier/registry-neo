from .models import find_record_by_id, find_record_by_year
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/<register>/<public_id>')
def find_record(register, public_id):
    entity_states = find_record_by_id(register, public_id)
    return jsonify(entity_states)


@app.route('/<register>/<public_id>/current')
def find_current_record(register, public_id):
    year = time.localtime(time.time()).tm_year
    entity_states = find_record_by_year(register, public_id, year)
    return jsonify(entity_states)


@app.route('/<register>/<public_id>/<int:year>')
def find_record_by_date(register, public_id, year):
    entity_states = find_record_by_year(register, public_id, year)
    return jsonify(entity_states)
