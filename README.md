# registry-neo

## Requirements

But all are provided in the Vagrant file

- python3
- pip
- virtualenv + virtualenvwrapper
- java (for neo4j)
- neo4j
- redis-server


## Installing

    > git clone ...
    > cd registry-neo
    > vagrant up
    > vagrant ssh
    % workon registry-neo


## Tests

    python -m unittest test.test_merkletree

## Running locally

### Neo4j

Start an instance of neo4j. There are >1 ways to do this but the simplest is

    >cd [neo4j home]
    >bin/neo4j start

You can then browse the database at http://localhost:7474. The first time you do so, you will have to change the default user/password from neo4j/neo4j to something else.

If neo4j is installed on a remote machine including a Vagrant guest host, then remote connections must be enabled in the config.
For neo4j installed via apt on Ubuntu, the config file is at */etc/neo4j.conf* .

### Loading data

The *loader* directory has some simple scripts and test data for local authorities in the form of Cypher statements.

     python load.py la50.cql

To remove all data

    python drop-all.py


### Registry

The application can to be configured with the URL, username and password for neoj4, although they default to *localhost, neo4j and password*.

    >python run.py

It also needs the Host, Port and Credentials for the Redis server instance TODO.

### Current API

- /[register]/[public_id]

e.g. http://localhost:5000/local_authority_eng/wob

- /[register]/[public_id]/state?time=[timestamp]

e.g. http://localhost:5000/local_authority_eng/wob/state?time=123456


## Heroku

The applcation is deployed Heroku as https://infinite-mountain-41435.herokuapp.com

If you have access to the applcation on Heroku, you can get the neo4j details with

    >heroku config
