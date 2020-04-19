create_message_table = """
CREATE TABLE IF NOT EXISTS message (
  message TEXT
);
"""

create_processed_table = """
CREATE TABLE processed (
	id INTEGER PRIMARY KEY,
	address TEXT,
	latitude TEXT,
	longitude TEXT,
	entity TEXT,
	message TEXT NOT NULL
);
"""

drop_message_table = """
DROP TABLE IF EXISTS message
"""

drop_processed_table = """
DROP TABLE IF EXISTS processed
"""