NEO_HOME=/home/john/apps/neo4j-community-3.0.7
DB_DIR="$NEO_HOME/data/databases/graph2.db"
DATA_DIR="$HOME/projects/registry-neo/loader"

$NEO_HOME/bin/neo4j-import --into $DB_DIR --nodes:local_authority_type "$DATA_DIR/local-authority-type-headers.csv,$DATA_DIR/local-authority-type-data.csv" --nodes:local_authority_type_state "$DATA_DIR/local-authority-type-state-headers.csv,$DATA_DIR/local-authority-type-state-data.csv" --relationships:STATE "$DATA_DIR/local-authority-type-state-rel-headers.csv,$DATA_DIR/local-authority-type-state-rel-data.csv"
