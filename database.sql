create table game_user
    ( user_ID			numeric(20, 0),
      pass_word			varchar(15) not null,
      user_name			varchar(20) not null unique,
      remark		 	varchar(20) default 'ordinary',
      user_level		int default 1,
      email			varchar(50),
      register_date		date not null,
      last_login_time   	timestamp(0),
      primary key (user_ID),
      check (user_level > 0) );

create table script
    ( script_ID			numeric(20, 0),
      title			varchar(50) not null,
      description		varchar(500) not null,
      truth			varchar(100) not null,
      primary key (script_ID),
      unique (title) );

create table game_role
    ( role_ID		numeric(20, 0),
      script_title	varchar(50) not null,
      role_name		varchar(50) not null,
      task		varchar(200) not null,
      role_description	varchar(500) not null,
      primary key (role_ID),
      foreign key (script_title) references script(title) 
		on update cascade
		on delete cascade );

create table game_clue
    ( clue_ID			numeric(20, 0),
      script_title		varchar(50) not null,
      clue_description		varchar(500) not null,
      primary key (clue_ID),
      foreign key (script_title) references script(title) 
		on update cascade
		on delete cascade );


create table game_room
    ( room_ID			numeric(20, 0),
      size			int,
      stage			varchar(50),
      script_title		varchar(50),
      primary key (room_ID),
      foreign key (script_title) references script(title) 
		on update cascade
		on delete cascade );

create table player
    ( player_ID		numeric(20, 0),
      user_id		numeric(20, 0),
      room_id           numeric(20, 0),
      role_id		numeric(20, 0),
      primary key (player_ID),
      foreign key (user_id) references game_user(user_ID) 
		on update cascade
		on delete cascade,
      foreign key (room_id) references game_room(room_ID) 
		on update cascade
		on delete cascade,
      foreign key (role_id) references game_role(role_ID) 
		on update cascade
		on delete cascade );

delimiter $


/*****		用户注册		*****/
create procedure register_user( in i_user_name		varchar(20),
							    in i_pass_word		varchar(15),
                                out msg				varchar(100),
                                out o_user_id		numeric(20, 0) )
	begin
		declare max_id numeric(20, 0);
		if ( i_user_name in ( select user_name
							  from game_user ) )
		then
			set o_user_id = 00000000000000000000;
			set msg = 'User name has already existed. ';
		else
			select max(user_id) into max_id
			from game_user;
			set o_user_id = max_id + 1;
			set msg = 'Register successfully. ';
			insert into game_user(user_ID, pass_word, user_name, register_date) values
				(o_user_id, i_pass_word, i_user_name, current_date());
		end if;
	end$


/*****		用户登录		*****/
create procedure login_user( in i_user_name		varchar(20), 
							 in i_pass_word		varchar(15), 
                             out state			bool, 
                             out msg			varchar(100) )
	begin
		if ( i_user_name not in ( select user_name
								  from game_user ) )
		then
			set state = 0;
            set msg = 'User name not found.';
		else
			if (i_pass_word not in ( select pass_word
									 from game_user
                                     where user_name = i_user_name ) )
			then
				set state = 0;
                set msg = 'Password error. ';
			else
				set state = 1;
                update game_user
                set last_login_time = localtimestamp()
                where user_name = i_user_name;
                set msg = 'Login successfully. ';
			end if;
		end if;
    end$


/*****		显示个人信息		*****/
create procedure visual_profile( in i_user_name varchar(20))
	begin
		select user_name, remark, user_level, email, last_login_time, register_date
        from game_user
        where user_name = i_user_name;
    end$


/*****      完善个人资料        *****/
create procedure profile_mail ( in i_user_id		numeric(20, 0),
								in i_mail			varchar(50),
                                out state			bool,
                                out msg				varchar(100) )
	begin
		if (i_mail like '_%@_%')
		then
			update game_user
			set email = i_mail
			where user_id = i_user_id;
			set state = 1;
			set msg = 'Update email successfully. ';
		else
			set state = 0;
			set msg = 'Email input is illegal. ';
		end if;
	end$ 
