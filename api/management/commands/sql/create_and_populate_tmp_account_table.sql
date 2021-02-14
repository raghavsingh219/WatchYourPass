CREATE TABLE IF NOT EXISTS tmp_api_account (
    id SERIAL,
    email character varying(100) UNIQUE NOT NULL,
    domain_id integer NOT NULL,
    count integer NOT NULL,
    CONSTRAINT tmp_api_account_fkey FOREIGN KEY(domain_id) REFERENCES api_domain(id)
);
TRUNCATE TABLE tmp_api_account;
BEGIN;
    INSERT INTO tmp_api_account(email,domain_id)
    SELECT email,count(domain_id) as cnt
    FROM tmp group by(email,domain_id);
commit;