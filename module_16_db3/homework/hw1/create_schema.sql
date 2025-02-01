
create table 'actors' (
    act_id integer primary key autoincrement,
    act_first_name varchar(50) not null,
    act_last_name varchar(50) not null,
    act_gender varchar(1) not null
);

create table 'movie' (
    mov_id integer primary key autoincrement,
    mov_title varchar(50) not null
);

create table 'director' (
    dir_id integer primary key autoincrement,
    dir_first_name varchar(50) not null,
    dir_last_name varchar(50) not null
);

create table 'movie_cast' (
    mov_id integer not null,
    act_id integer not null,
    role varchar(50) not null,
    FOREIGN KEY (act_id) REFERENCES actors(act_id) ON DELETE CASCADE,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
);

create table 'oscar_awarded' (
    award_id integer primary key autoincrement,
    mov_id integer not null,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE
);

create table 'movie_direction' (
    mov_id integer not null,
    dir_id integer not null,
    FOREIGN KEY (mov_id) REFERENCES movie(mov_id) ON DELETE CASCADE,
    FOREIGN KEY (dir_id) REFERENCES director(dir_id) ON DELETE CASCADE
);

