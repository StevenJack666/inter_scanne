create database vcrawl;
use vcrawl;

CREATE TABLE `crawl_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `docid` varchar(128) NOT NULL COMMENT '文档唯一标识编码',
  `title` varchar(512) NOT NULL COMMENT '标题',
  `dtype` varchar(32) NOT NULL COMMENT '文档类型',
  `href` varchar(512) DEFAULT NULL COMMENT '文档链接',
  `publisher` varchar(64) DEFAULT NULL COMMENT '发布者',
  `publish_time` varchar(128) DEFAULT NULL COMMENT '发布时间',
  `send_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '告警是否发送:0:未发送1:已发送',
  `create_time` datetime NOT NULL COMMENT '记录插入时间',
  `update_time` datetime NOT NULL COMMENT '记录更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_docid` (`docid`),
  KEY `idx_title` (`title`),
  KEY `idx_publish_time` (`publish_time`),
  KEY `idx_dtype` (`dtype`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

alter table crawl_info add column `doc_page_tag` varchar(32) DEFAULT NULL COMMENT '文档页面标签:xx页xx行';
alter table crawl_info add column `description` varchar(1024) DEFAULT NULL COMMENT '文档描述';