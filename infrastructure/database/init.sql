CREATE TABLE IF NOT EXISTS PERMISSION(
    id serial primary key,
    read_services boolean not null,
    write_service boolean not null,
    invite_users boolean not null
);

CREATE TABLE IF NOT EXISTS USERGROUP(
    id serial primary key,
    usergroup_name varchar(64) not null,
    permission int references PERMISSION(id) on delete restrict
);

CREATE TABLE IF NOT EXISTS USERS(
    id serial primary key,
    username varchar(32) not null,
    passw varchar(128) not null,
    register_date date not null default CURRENT_DATE,
    full_name text not null,
    job_role varchar(64),
    department varchar(128)
);

CREATE TABLE IF NOT EXISTS SERVICEGROUP(
    id serial primary key,
    servicegroup_name varchar(64) not null
);

CREATE TABLE IF NOT EXISTS SERVICES(
    id serial primary key,
    servicename varchar(64) not null,
    passw varchar(128),
    token varchar(64),
    token_expired_time date,
    servicegroup_id int references SERVICEGROUP(id) on delete restrict
);

CREATE TABLE IF NOT EXISTS SERVICES_TO_USERGROUP(
    id serial primary key,
    service_id int references SERVICES(id),
    usergroup_id int references USERGROUP(id),
    permissions_id int references PERMISSION(id)
);

CREATE TABLE IF NOT EXISTS USER_TO_USERGROUP(
    id serial primary key,
    user_id int references USERS(id),
    usergroup_id int references USERGROUP(id)
);