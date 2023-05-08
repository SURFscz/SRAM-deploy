#!/usr/bin/env python3

# from https://gist.githubusercontent.com/panzi/81892af865a4818e9ccf578ab5766d36/raw/9d1f162bbe41b86b76a6dd51f3d4c016073d1f44/rekey.py
# derived from https://stackoverflow.com/a/67161907/277767
# Changes to the StackOverflow version:
# * delete temporary files that contain vaults!
# * prompt for passwords instead of passing them as program argument
# * more precise vault replacement
# * a bit nicer error messages that points at the line where re-keying failed

from typing import Optional

import sys
import re
import os

from os.path import join as join_path
from tempfile import gettempdir
from ansible.parsing.vault import VaultEditor, VaultLib, VaultSecret
from ansible.constants import DEFAULT_VAULT_IDENTITY
from ansible.errors import AnsibleError
from getpass import getpass

VAULT_REGEX = re.compile(r'(?P<vault>^(?P<indent>\s*)\$ANSIBLE_VAULT\S*\n(?:\s*\w+\n)*)', re.MULTILINE)

temp_count = 0


class ReKeyError(Exception):
    __slots__ = 'lineno', 'cause'

    lineno: int
    cause: Optional[Exception]

    def __init__(self, lineno: int, cause: Optional[Exception] = None) -> None:
        super().__init__()
        self.lineno = lineno
        self.cause = cause

    def __str__(self) -> str:
        return f'at line {self.lineno}: {self.cause if self.cause is not None else "an error occured"}'


def rekey(content: str, old_secret: VaultSecret, new_secret: VaultSecret) -> str:
    global temp_count

    temp_name = join_path(gettempdir(), f'ansible-rekey-{os.getpid()}-{temp_count}.tmp')
    temp_count += 1

    prev_index = 0
    new_content: list[str] = []
    while True:
        match = VAULT_REGEX.search(content, prev_index)
        if match is None:
            new_content.append(content[prev_index:])
            break

        indentation = match.group('indent')
        old_vault = match.group('vault')

        index = match.start()
        if index > prev_index:
            new_content.append(content[prev_index:index])
        new_content.append(indentation)

        string_content = old_vault.replace(indentation, '')

        try:
            with open(temp_name, 'w') as fout:
                fout.write(string_content)

            editor = VaultEditor(VaultLib([(DEFAULT_VAULT_IDENTITY, old_secret)]))
            editor.rekey_file(temp_name, new_secret)

            with open(temp_name) as fin:
                lines = fin.readlines()
        except Exception as exc:
            lineno = content.count('\n', 0, index) + 1
            if isinstance(exc, AnsibleError):
                exc.message = exc.message.replace(temp_name, f'line {lineno}')
            raise ReKeyError(lineno, exc)
        finally:
            os.unlink(temp_name)

        new_content.append(indentation.join(lines))
        prev_index = match.end()

    return ''.join(new_content)


def rekey_files(old_password: str, new_password: str, files: list[str]) -> None:
    for file_name in files:
        with open(file_name) as f:
            content = f.read()

        try:
            new_content = rekey(content, VaultSecret(old_password.encode()), VaultSecret(new_password.encode()))
        except ReKeyError as exc:
            print(f'{file_name}:{exc.lineno}: {exc.cause if exc.cause is not None else "an error occured"}', file=sys.stderr)
        else:
            with open(file_name, 'w') as f:
                f.write(new_content)

            print('rekeyed', file_name)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: rekey.py <file...>", file=sys.stderr)
        sys.exit(1)

    old_password = getpass('Vault password: ')
    new_password = getpass('New Vault password: ')
    new_password_confirmation = getpass('Confirm New Vault password: ')

    if new_password != new_password_confirmation:
        print('ERROR! Passwords do not match', file=sys.stderr)
        sys.exit(1)

    rekey_files(old_password, new_password, sys.argv[1:])


if __name__ == '__main__':
    main()
