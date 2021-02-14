--CREATE OR REPLACE PROCEDURE populate_tmp2(file_path text)
--    language plpgsql
--    as $$
--    begin
--        COPY tmp(email, domain, hash)
--        FROM :file_path
--        DELIMITER ';';
--
--        commit;
--    end;$$;


CREATE OR REPLACE PROCEDURE populate_tmp(file_path text)
    language plpgsql
    as $$
    DECLARE STATEMENT TEXT;
    begin
        STATEMENT := 'COPY tmp(email, domain, hash) FROM ''' || file_path ||  ''' DELIMITER '';''';
        EXECUTE STATEMENT;
        commit;
    end;$$;

