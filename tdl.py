# coding=utf-8
from views import tdl_client
import sys

try:
    from colorama import Fore
except ImportError as e:
    class Fore(object):
        GREEN = ''
        RED = ''

USAGE = r'''USAGE:
    命令行执行: python tdl.py -u username -p password 进入交互环境, 输入 'q' 退出;
    命令行执行: python tdl.py -h 查看此帮助'''

COMMAND = r'''
    ls  --list all valid todos;
    la  --list all todos;
    ld  --list done todos;
    lu  --list undone todos;
    find tag  --search todo;
    rm n  --remove nth todo;
    do n  --mark nth todo as done;
    ud n  --mark nth todo as undone;
    add todo  --add a todo;
    ed n todo  --edit nth todo.'''


def check_input():
    if len(sys.argv) == 5:
        user_flag = sys.argv[1]
        password_flag = sys.argv[3]
        if (user_flag == '-u' or user_flag == '--user') and (password_flag == '-p' or password_flag == '--password'):
            username = sys.argv[2]
            password = sys.argv[4]
            tdl = tdl_client.Client(username, password)
            if tdl.check_user():
                return tdl
            else:
                print '用户名或密码错误'
                exit()
        else:
            print USAGE
    else:
        print USAGE
    exit()


def display(todos):
    for todo in todos:
        if todo.is_done:
            print Fore.GREEN + '{} | {} | {} | 已完成'.format(todo.id, todo.content,
                                                           todo.updated_time.strftime('%y-%m-%d %H:%M')) + Fore.RESET
        else:
            print Fore.RED + '{} | {} | {} | 未完成'.format(todo.id, todo.content,
                                                         todo.updated_time.strftime('%y-%m-%d %H:%M')) + Fore.RESET


def tdl_operation():
    tdl = check_input()
    print COMMAND
    command = raw_input('>')
    while command != 'q' and command != 'quit' and command != 'exit':
        command = ' '.join(command.split())
        if command == 'ls':
            todos = tdl.ls()
            display(todos)
        elif command == 'la':
            todos = tdl.la()
            display(todos)
        elif command == 'ld':
            todos = tdl.ld()
            display(todos)
        elif command == 'lu':
            todos = tdl.lu()
            display(todos)
        elif command[:4] == 'find':
            todos = tdl.search(command[5:])
            display(todos)
        elif command[:2] == 'do' and command[3:].isdigit():
            tdl.done(command[3:])
        elif command[:2] == 'ud' and command[3:].isdigit():
            tdl.undone(command[3:])
        elif command[:2] == 'rm' and command[3:].isdigit():
            tdl.remove(command[3:])
        elif command[:2] == 'ed' and command.split()[1].isdigit():
            tdl.edit(command.split()[1], ' '.join(command.split()[2:]))
        elif command[:3] == 'add':
            tdl.add(command[4:])
        else:
            print Fore.RED + '无效的命令' + Fore.RESET
            print COMMAND
        command = raw_input('>')


if __name__ == '__main__':
    tdl_operation()
