--BEGIN;
--    INSERT INTO api_account(email,domain_id,count)
--    (SELECT tmp.email,api_domain.id,count(tmp.email)
--        FROM tmp,api_domain
--        where tmp.domain=api_domain.domain
--        GROUP BY(email,api_domain.id))
--    ON CONFLICT On constraint email_domain_unique DO UPDATE SET count=(select count(email) FROM api_account WHERE email=excluded.email)+excluded.count;
--commit;
BEGIN;
    INSERT INTO tmp2_api_account(email,domain_id,count)
    SELECT api_account.email,api_account.domain_id,api_account.count FROM api_account INNER JOIN tmp_api_account
    ON tmp_api_account.email=api_account.email AND tmp_api_account.domain_id=api_account.domain_id;

    DELETE FROM api_account account
    USING tmp2_api_account tmp_account
    WHERE account.email=tmp_account.email AND account.domain_id=tmp_account.domain_id;

    --append tmp_api_account to tmp2_api_account
    INSERT INTO tmp2_api_account(email,domain_id,count)
    SELECT tmp_api_account.email,tmp_api_account.domain_id,tmp_api_account.count FROM tmp_api_account;

    CREATE INDEX IF NOT EXISTS account_email_domain ON tmp2_api_account(email,domain_id);

    INSERT INTO api_account(email,domain_id,count)
    SELECT email,domain_id,sum(count) as count FROM tmp2_api_account
    GROUP BY(email,domain_id);

    DROP INDEX account_email_domain;
COMMIT;
