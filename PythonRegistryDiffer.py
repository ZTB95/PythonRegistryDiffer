from platform import system, release
import PythonRegistryDiffer.userfunctions as exec


def get_command():
    exec.prd_help()
    return False


def main():
    while True:
        if get_command():
            continue
        else:
            return


if __name__ == '__main__':
    if 'windows' not in system().lower():
        print('This program must be run on a Windows host. Detected \'{} {}\'. Quitting...'.format(system(), release()))
    else:
        main()
