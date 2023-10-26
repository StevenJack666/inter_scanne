
create table tg_data
(
    id              bigint auto_increment
        primary key,
    message_id      varchar(64) null comment '消息id',
    chat_id         varchar(32)  not null comment '群id',
    chat_nick       varchar(32)  not null comment '群名称',
    user_id         varchar(20)  not null comment '用户id',
    user_name       varchar(20)  not null comment '用户名称',
    nick_name       varchar(20) null comment '用户昵称',
    user_photo_path varchar(20) null comment '用户头像路径',
    postal_time     varchar(64) null comment '消息发布时间',
    reply_to_msg_id varchar(20) null comment '回复的消息id',
    from_name       varchar(20) default null comment '',
    from_date       datetime     not null comment '',
    message         varchar(128) not null comment '消息内容',
    `create_time`   datetime     NOT NULL COMMENT '记录插入时间',
    `update_time`   datetime     NOT NULL COMMENT '记录更新时间'
)

    comment 'TG群消息' collate = utf8mb3_unicode_ci;



-- auto-generated definition
create table tg_channel_group
(
    id                  int auto_increment comment 'id'
        primary key,
    channel_id          varchar(20)  null comment '频道ID',
    title               varchar(200) null comment '频道标题',
    username            varchar(20)  null comment '频道名称',
    hex_url             varchar(20)  null comment '频道地址',
    megagroup           varchar(20)  null,
    member_count        int          not null comment '群组成员数',
    tenant_id           varchar(20)  null comment '租户id',
    offset_date         bigint null comment '爬虫起始时间',
    channel_description varchar(64)  null comment '频道描述',
    is_public           int          not null comment '是否公开',
    join_date           datetime     null comment '加入时间',
    last_message_id     int          not null comment '最后一条被读的消息记录',
    create_time         datetime     not null comment '记录插入时间',
    update_time         datetime     not null comment '记录更新时间'
)
    comment 'tg群组' collate = utf8mb3_unicode_ci;