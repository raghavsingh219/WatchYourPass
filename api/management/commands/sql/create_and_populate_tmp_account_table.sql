CREATE TABLE IF NOT EXISTS tmp_api_account (
    id SERIAL,
    email character varying(100) NOT NULL,
    domain_id integer NOT NULL,
    count integer NOT NULL,
    CONSTRAINT tmp_api_account_fkey FOREIGN KEY(domain_id) REFERENCES api_domain(id),
    CONSTRAINT tmp_api_account_email_domain_unique UNIQUE(email,domain_id)
);
TRUNCATE TABLE tmp_api_account;

BEGIN;
    INSERT INTO tmp_api_account(email,domain_id,count)
    (SELECT tmp.email,api_domain.id,count(tmp.email)
        FROM tmp,api_domain
        where tmp.domain=api_domain.domain
        GROUP BY(email,api_domain.id));
commit;

