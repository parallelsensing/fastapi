-- Adminer 4.8.1 PostgreSQL 15.1 (Debian 15.1-1.pgdg110+1) dump
-- CREATE DATABASE "sensing";

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;


DROP TABLE IF EXISTS "article";
CREATE TABLE "article" (
  "id" bigserial PRIMARY KEY,
  "doi" character varying(200),
  "title" text NOT NULL,
  "abstract" text NOT NULL,
  "graphic" text,
  "status" smallint DEFAULT 0,
  "pay_status" smallint DEFAULT 0,
  "early_access" boolean DEFAULT 'f',
  "html_link" character varying(200),
  "show_html" boolean DEFAULT 'f',
  "pdf_link" character varying(200),
  "pdf_edition" character varying(200),
  "pdf_size" integer DEFAULT 0,
  "read_count" integer DEFAULT 0,
  "citation_count" integer DEFAULT 0,
  "download_count" integer DEFAULT 0,
  "order_id" bigint,
  "updated_at" timestamp DEFAULT NULL,
  "created_at" timestamp DEFAULT now() NOT NULL
);
COMMENT ON TABLE "article" IS '文章';
alter sequence article_id_seq restart with 100;

DROP TABLE IF EXISTS "keyword";
CREATE TABLE "keyword" (
  "id" bigserial PRIMARY KEY,
  "name" character varying(200) NOT NULL UNIQUE,
  "updated_user_id" bigint,
  "created_user_id" bigint,
  "updated_at" timestamp DEFAULT NULL,
  "created_at" timestamp DEFAULT now() NOT NULL
);
COMMENT ON TABLE "keyword" IS '关键词';
COMMENT ON COLUMN "keyword"."name" IS '关键词';

DROP TABLE IF EXISTS "author";
CREATE TABLE "author" (
  "id" bigserial PRIMARY KEY,
  "orcid" character varying(200),
  "email" character varying(200) NOT NULL UNIQUE,
  "first_name" character varying(200) NOT NULL,
  "last_name" character varying(200) NOT NULL,
  "updated_user_id" bigint,
  "created_user_id" bigint,
  "updated_at" timestamp DEFAULT NULL,
  "created_at" timestamp DEFAULT now() NOT NULL
);
COMMENT ON TABLE "author" IS '作者';
COMMENT ON COLUMN "author"."email" IS '作者邮箱';
COMMENT ON COLUMN "author"."first_name" IS '作者名';
COMMENT ON COLUMN "author"."last_name" IS '作者姓';


DROP TABLE IF EXISTS "author_keyword";
CREATE TABLE "author_keyword" (
  "author_id" bigint DEFAULT '0' NOT NULL,
  "keyword_id" bigint DEFAULT '0' NOT NULL,
  "sequence" smallint DEFAULT '0',
  CONSTRAINT "author_keyword_pkey" PRIMARY KEY ("author_id", "keyword_id")
) WITH (oids = false);
COMMENT ON TABLE "author_keyword" IS '作者领域';
COMMENT ON COLUMN "author_keyword"."author_id" IS '作者id';
COMMENT ON COLUMN "author_keyword"."keyword_id" IS '关键词id';
COMMENT ON COLUMN "author_keyword"."sequence" IS '关键词顺序';

ALTER TABLE ONLY "author_keyword" ADD CONSTRAINT "author_keyword_author_id_fkey" FOREIGN KEY (author_id) REFERENCES author(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "author_keyword" ADD CONSTRAINT "author_keyword_keyword_id_fkey" FOREIGN KEY (keyword_id) REFERENCES keyword(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;





DROP TABLE IF EXISTS "institution";
CREATE TABLE "institution" (
  "id" bigserial PRIMARY KEY,
  "institution" character varying(200) DEFAULT '' NOT NULL,
  "department" character varying(200),
  "address" character varying(200),
  "country" character varying(200),
  "province" character varying(200),
  "city" character varying(200),
  "postal_code" character varying(50),
  "phone" character varying(50),
  "fax" character varying(50),
  "updated_at" timestamp DEFAULT NULL,
  "created_at" timestamp DEFAULT now() NOT NULL
);
COMMENT ON TABLE "institution" IS '用户地址';
COMMENT ON COLUMN "institution".institution IS '机构';
COMMENT ON COLUMN "institution".department IS '部门';
COMMENT ON COLUMN "institution".address IS '地址';
COMMENT ON COLUMN "institution".country IS '国家';
COMMENT ON COLUMN "institution".province IS '省份';
COMMENT ON COLUMN "institution".city IS '城市';
COMMENT ON COLUMN "institution".postal_code IS '邮编';
COMMENT ON COLUMN "institution".phone IS '电话';
COMMENT ON COLUMN "institution".fax IS '传真';

DROP TABLE IF EXISTS "author_institution";
CREATE TABLE "author_institution" (
  "author_id" bigint DEFAULT '0' NOT NULL,
  "institution_id" bigint DEFAULT '0' NOT NULL,
  "sequence" smallint DEFAULT '0',
  CONSTRAINT "author_institution_pkey" PRIMARY KEY ("author_id", "institution_id")
) WITH (oids = false);
COMMENT ON TABLE "author_institution" IS '作者的机构';
COMMENT ON COLUMN "author_institution"."institution_id" IS 'institution表id';
COMMENT ON COLUMN "author_institution"."author_id" IS 'author表id';
COMMENT ON COLUMN "author_institution"."sequence" IS '作者顺序';



DROP TABLE IF EXISTS "article_author";
CREATE TABLE "article_author" (
  "article_id" bigint DEFAULT '0' NOT NULL,
  "author_id" bigint DEFAULT '0' NOT NULL,
  "sequence" smallint DEFAULT '0',
  CONSTRAINT "article_author_pkey" PRIMARY KEY ("article_id", "author_id")
) WITH (oids = false);
COMMENT ON TABLE "article_author" IS '文章的作者';
COMMENT ON COLUMN "article_author"."article_id" IS 'article表id';
COMMENT ON COLUMN "article_author"."author_id" IS 'author表id';
COMMENT ON COLUMN "article_author"."sequence" IS '作者顺序，0为通讯作者';


ALTER TABLE ONLY "article_author" ADD CONSTRAINT "article_author_article_id_fkey" FOREIGN KEY (article_id) REFERENCES article(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "article_author" ADD CONSTRAINT "article_author_author_id_fkey" FOREIGN KEY (author_id) REFERENCES author(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;



DROP TABLE IF EXISTS "article_keyword";
CREATE TABLE "article_keyword" (
  "article_id" bigint DEFAULT '0' NOT NULL,
  "keyword_id" bigint DEFAULT '0' NOT NULL,
  "sequence" smallint DEFAULT '0',
  CONSTRAINT "article_keyword_pkey" PRIMARY KEY ("article_id", "keyword_id")
) WITH (oids = false);
COMMENT ON TABLE "article_keyword" IS '文章关键词';
COMMENT ON COLUMN "article_keyword"."article_id" IS '文章id';
COMMENT ON COLUMN "article_keyword"."keyword_id" IS '关键词id';
COMMENT ON COLUMN "article_keyword"."sequence" IS '关键词顺序';

ALTER TABLE ONLY "article_keyword" ADD CONSTRAINT "article_keyword_article_id_fkey" FOREIGN KEY (article_id) REFERENCES article(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "article_keyword" ADD CONSTRAINT "article_keyword_keyword_id_fkey" FOREIGN KEY (keyword_id) REFERENCES keyword(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;



DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
  "id" bigserial PRIMARY KEY,
  "email" character varying(200) NOT NULL UNIQUE,
  "password" character varying(200) NOT NULL,
  "author_id" bigint,
  "role_id" bigint,
  "is_admin" boolean DEFAULT 'f',
  "is_active" boolean DEFAULT 'f',
  "updated_at" timestamp DEFAULT NULL,
  "created_at" timestamp DEFAULT now() NOT NULL
);
COMMENT ON COLUMN "user"."email" IS '注册邮箱';
COMMENT ON COLUMN "user"."password" IS '密码';
COMMENT ON COLUMN "user"."author_id" IS '作者id';
COMMENT ON COLUMN "user"."role_id" IS '角色id';
COMMENT ON COLUMN "user"."is_admin" IS '是否管理员';
COMMENT ON COLUMN "user"."is_active" IS '是否激活';
COMMENT ON COLUMN "user"."updated_at" IS '更新时间';
COMMENT ON COLUMN "user"."created_at" IS '创建时间';
ALTER TABLE ONLY "user" ADD CONSTRAINT "user_author_id_fkey" FOREIGN KEY (author_id) REFERENCES author(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE ONLY "user" ADD CONSTRAINT "user_role_id_fkey" FOREIGN KEY (role_id) REFERENCES role(id) ON UPDATE CASCADE ON DELETE SET NULL;


DROP TABLE IF EXISTS "user_article";
CREATE TABLE "user_article" (
  "user_id" bigint DEFAULT '0' NOT NULL,
  "article_id" bigint DEFAULT '0' NOT NULL,
  "updated_at" timestamp,
  "created_at" timestamp DEFAULT now() NOT NULL,
  CONSTRAINT "user_article_pkey" PRIMARY KEY ("article_id", "user_id")
);
COMMENT ON TABLE "user_article" IS '用户发表文章';
COMMENT ON COLUMN "user_article"."user_id" IS '用户id';
COMMENT ON COLUMN "user_article"."article_id" IS '文章id';
ALTER TABLE ONLY "user_article" ADD CONSTRAINT "user_article_article_id_fkey" FOREIGN KEY (article_id) REFERENCES article(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "user_article" ADD CONSTRAINT "user_article_user_id_fkey" FOREIGN KEY (user_id) REFERENCES "user"("id") ON DELETE SET NULL ON UPDATE CASCADE;

