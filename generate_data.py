import sys
import random
from tqdm import tqdm

names = ['Abbott', 'Abel', 'Abraham', 'Adair', 'Aldrich', 'Angel', 'Abernathy', 'Abrams', 'Acker', 'Ackerman', 'Adamson', 'Adcock', 'Adler', 'Alonso', 'Ali', 'Alonzo', 'Angle', 'Alger', 'Archibald', 'Bill', 'Brian', 'Billy', 'Baber', 'Bader', 'Baily', 'Bainbridge', 'Clifford', 'Cornelius', 'Christy', 'Christie', 'Duncan', 'Dunn', 'Daniel', 'David', 'Emma', 'Ellis', 'Frederick', 'Felix', 'Hayes', 'Hale', 'Haley', 'Hardy', 'Irwin', 'Israel', 'Ivory', 'Ivy', 'James', 'Jeanne', 'Joyce', 'Jarvis', 'Jefferson', 'Jacob', 'Kyle', 'Kay', 'Kearney', 'Lester', 'Lora', 'Lang', 'Mitchell', 'Morris', 'Moon', 'Noah', 'Natasha', 'Newman', 'Norman', 'Owen', 'Osborn', 'Olga', 'Odom', 'Perry', 'Porter', 'Palmer', 'Quennel', 'Quintion', 'Queenie', 'Randolph', 'Raymond', 'Regan', 'Richard', 'Roy', 'Sophia', 'Stewart', 'Samantha', 'Talbot', 'Tatum', 'Teague', 'Victoria', 'Viola', 'Vicente', 'Van', 'William', 'Waller', 'Walton', 'Ware',' Xavier', 'Xenia', 'Yolanda', 'Yvette', 'Yilia', 'Zoey']


def generate_for_user():
    random.shuffle(names)
    commands = []
    command_head = 'insert into User (_id, name, password, email, register_date, group_id, friend_num) values ('
    command_tail = ');'
    for i in tqdm(range(100)):
        names[i] = names[i].strip()
        specific = ', '.join([str(i), "'"+names[i]+"'", "'ps"+names[i]+"wd'", "'"+names[i].lower()+"@pku.edu.cn'", 'localtimestamp()', '0', '0'])
        commands.append(command_head + specific + command_tail)
    specific = ', '.join(['100', "'管理员'", "'psManagerwd'", "'manager@pku.edu.cn'", 'localtimestamp()', '1', '0'])
    commands.append(command_head + specific + command_tail)
    return commands


if __name__ == '__main__':
    tag, filename = sys.argv[1], sys.argv[2]
    if tag == 'user':
        sql_commands = generate_for_user()
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_commands))