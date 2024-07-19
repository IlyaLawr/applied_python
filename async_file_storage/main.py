import os

from file_daemon import FileDaemon


if __name__ == "__main__":
    main_path = os.path.dirname(os.path.abspath(__file__))

    file_daemon_a = FileDaemon(f'{main_path}/configs/config_A.yaml')
    file_daemon_b = FileDaemon(f'{main_path}/configs/config_B.yaml')
    file_daemon_c = FileDaemon(f'{main_path}/configs/config_C.yaml')

    for fd in (file_daemon_a, file_daemon_b, file_daemon_c):
        fd.start()

    file_daemon_a.join()
    file_daemon_b.join()
    file_daemon_c.join()
