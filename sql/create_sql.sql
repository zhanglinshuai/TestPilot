-- auto-generated definition
create table "user"
(
    id            serial
        constraint user_pk
            primary key,
    username      varchar(50)                                     not null
        constraint user_pk_2
            unique,
    safe_password varchar(255)                                    not null,
    email         varchar(255),
    role          varchar(20) default 'tester'::character varying not null,
    is_active     boolean     default true                        not null,
    created_at    timestamp   default now()                       not null,
    updated_at    timestamp   default now()                       not null
);

comment on table "user" is '用户表';

comment on column "user".id is '用户id 自增主键';

comment on column "user".username is '登录名';

comment on column "user".safe_password is '安全的密码（加密后的）';

comment on column "user".email is '邮箱';

comment on column "user".role is '用户角色';

comment on column "user".is_active is '是否启用';

comment on column "user".created_at is '创建时间';

comment on column "user".updated_at is '更新时间';

alter table "user"
    owner to postgres;

