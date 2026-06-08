/**
用户表的建表语句
 */
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

/**
项目表的建表语句
 */
-- auto-generated definition
create table project
(
    id             integer                 not null
        constraint project_pk
            primary key,
    name           varchar(50)
        constraint project_pk_2
            unique,
    description    text,
    repo_url       varchar(500)            not null,
    default_env_id integer                 not null,
    created_id     integer                 not null,
    updated_id     integer                 not null,
    is_active      boolean   default true  not null,
    created_at     timestamp default now() not null,
    updated_at     timestamp default now() not null
);

comment on table project is '项目表';

comment on column project.id is '自增主键';

comment on column project.name is '项目名称';

comment on column project.description is '项目描述';

comment on column project.repo_url is '代码仓库地址';

comment on column project.default_env_id is '默认环境id';

comment on column project.created_id is '创建人id';

comment on column project.updated_id is '最后修改人id';

comment on column project.is_active is '是否启用';

comment on column project.created_at is '创建时间';

comment on column project.updated_at is '最后更新时间';

alter table project
    owner to postgres;

