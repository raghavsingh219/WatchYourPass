--INSERT INTO api_account_passwords(account_id,password_id)
--SELECT DISTINCT x.account_id,api_password.id FROM
--(SELECT  api_account.id as account_id,tmp.hash from api_account,tmp where tmp.email=api_account.email) as x,api_password
--WHERE x.hash=api_password.hash


BEGIN;
    INSERT INTO api_account_passwords(password_id,account_id)
    SELECT DISTINCT x.password_id,y.account_id FROM
    (SELECT api_password.id as password_id,tmp.email as email,domain FROM tmp,api_password WHERE tmp.hash=api_password.hash) as x,
    (SELECT api_account.id as account_id,api_account.email as email,domain FROM api_domain,api_account WHERE api_domain.id=api_account.domain_id) as y
    WHERE x.email=y.email AND x.domain=y.domain
    ON CONFLICT(account_id,password_id) DO NOTHING;
    --ON CONFLICT On constraint api_email_passwords_email_id_password_id_8e9a8617_uniq DO NothING;
commit;