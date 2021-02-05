INSERT INTO api_account(email,domain_id,count)(
    SELECT tmp.email,api_domain.id,count(tmp.email)
    FROM tmp,api_domain
    where tmp.domain=api_domain.domain
    GROUP BY(email,api_domain.id)
);
commit;