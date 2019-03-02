from platform import system
from PythonRegistryDiffer import user_functions


def get_command():
    pass


def main():
    while True:
        if get_command():
            continue
        else:
            return


if __name__ == '__main__':
    if 'windows' not in system().lower():
        print('This program must be run on a windows host.')
    else:
        main()
