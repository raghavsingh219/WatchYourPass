
CREATE TABLE IF NOT EXISTS tmp(
    id SERIAL,
    email VARCHAR(100) NOT NULL,
    domain VARCHAR(80) NOT NULL,
    hash VARCHAR(80) NOT NULL
);
CREATE INDEX IF NOT EXISTS abc
ON tmp(domain, email, hash);
TRUNCATE TABLE tmp;