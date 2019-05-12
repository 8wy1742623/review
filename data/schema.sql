drop table if exists cards;
drop table if exists plans;
drop table if exists mark_plan;

create table cards (
  id integer primary key autoincrement,
  type text not null,
  front text not null,
  back text not null,
  in_plan boolean default 0,
  created text not null
);

create table plans (
  id integer primary key autoincrement,
  card_id integer not null,
  known integer default 0
);

create table mark_plan (
  id integer primary key autoincrement,
  ct text not null,
  mark integer default 1
);

INSERT INTO
    mark_plan (ct)
VALUES
    ('2000-01-01' );