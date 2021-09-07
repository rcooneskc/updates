#!/usr/bin/env python3
from subprocess import run
from subprocess import SubprocessError
import sys


class Updater:
    __package_manager = {
        "apt-get": [
            ['update'],
            ['upgrade', '-y'],
            ['autoclean', '-y'],
            ['autoremove', '-y']
        ],
        "yum": [
            ['update', '-y']
        ]
    }

    __elevate = 'sudo'
    __separator = '\n***********************\n'

    def __init__(self, pkg_manager='apt-get'):
        self.pkg_manager = pkg_manager
        self.commands = self.__package_manager[pkg_manager]

    def execute_update(self) -> None:

        try:
            for command in self.commands:
                run([self.__elevate, self.pkg_manager, *command], check=True)

            return 0
        except SubprocessError:
            return 1

    def deliver_result(self, result: int) -> None:
        print(self.__separator)

        if result == 0:
            print('Updates completed successfully')
        else:
            print('Updates failed for some reason')

        print(self.__separator)


if len(sys.argv) > 1:
    upd = Updater(sys.argv[1])
else:
    upd = Updater()

RESULT = upd.execute_update()
upd.deliver_result(RESULT)
