
create table tg_data
(
    id            bigint auto_increment
        primary key,
    message_id   varchar(64)         null comment '消息id',
    chat_id         varchar(32)         not null comment '群id',
    chat_nick     varchar(32)         not null comment '群名称',
    user_id         varchar(20)         not null comment '用户id',
    user_name         varchar(20)          not null comment '用户名称',
    nick_name          varchar(20)         null comment '用户昵称',
    user_photo_path          varchar(20)         null comment '用户头像路径',
    postal_time     varchar(64)          null comment '消息发布时间',
    reply_to_msg_id  varchar(20)         null comment '回复的消息id',
    from_name   varchar(20)    default null comment '',
    from_date   datetime             not null comment '',
    message   varchar(128)               not null comment '消息内容',
    `create_time` datetime NOT NULL COMMENT '记录插入时间',
    `update_time` datetime NOT NULL COMMENT '记录更新时间'

    comment 'TG群消息' collate = utf8mb3_unicode_ci;

