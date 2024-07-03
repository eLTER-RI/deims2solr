CREATE TABLE IF NOT EXISTS site_data (
    id VARCHAR PRIMARY KEY,
    data JSONB,
    changed TIMESTAMP
);
