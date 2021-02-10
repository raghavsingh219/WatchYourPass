INSERT INTO api_account(email,domain_id,count)
(SELECT tmp.email,api_domain.id,count(tmp.email)
    FROM tmp,api_domain
    where tmp.domain=api_domain.domain
    GROUP BY(email,api_domain.id))
ON CONFLICT On constraint email_domain_unique DO UPDATE SET count=(select count(email) FROM api_account WHERE email=excluded.email)+excluded.count;
commit;