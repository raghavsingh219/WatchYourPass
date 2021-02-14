create table api_passwordaccountrelation(
id serial,
account_id int not null,
password_id int not null,
constraint acct foreign key(account_id) references api_account(id) on delete cascade,
constraint pwd foreign key(password_id) references api_password(id) on delete cascade
);