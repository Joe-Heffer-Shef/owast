// Set up database schema

// Mongo Shell scripting docs
// https://docs.mongodb.com/mongodb-shell/write-scripts/#std-label-mdb-shell-write-scripts

conn = Mongo();

db = conn.getDB("owast");

// Create unique index for experiment identifier
db.experiments.createIndex(
    {"experiment_id": 1},
    {unique: true}
)
