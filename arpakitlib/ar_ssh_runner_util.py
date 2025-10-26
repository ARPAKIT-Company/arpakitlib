# arpakit

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

import asyncssh
import paramiko
from arpakitlib.ar_json_util import transfer_data_to_json_str
from pydantic import BaseModel, ConfigDict


class BaseSSHException(Exception):
    pass


class ConnectionSSHException(BaseSSHException):
    def __init__(self, ssh_runner: SSHRunner, base_exception: Exception | None = None):
        self.ssh_runner = ssh_runner
        self.base_exception = base_exception

    def __str__(self):
        parts = [
            f"Connection error",
            f"{self.ssh_runner.username}@{self.ssh_runner.hostname}:{self.ssh_runner.port}",
            f"{type(self.base_exception)=}",
            f"{self.base_exception=}"
        ]
        return ', '.join(parts)

    def __repr__(self):
        return str(self)


class ErrorInRunSSHException(BaseSSHException):
    def __init__(self, ssh_runner: SSHRunner, base_exception: Exception | None = None, message: str | None = None):
        self.ssh_runner = ssh_runner
        self.base_exception = base_exception
        self.message = message

    def __str__(self):
        parts = [
            f"Error in run",
            f"{self.ssh_runner.username}@{self.ssh_runner.hostname}:{self.ssh_runner.port}",
        ]
        if self.base_exception is not None:
            parts.append(f"{self.base_exception=}")
        if self.message is not None:
            parts.append(f"{self.message=}")
        return ', '.join(parts)

    def __repr__(self):
        return str(self)


class SSHRunResultHasErrorSSHException(BaseSSHException):
    def __init__(self, ssh_run_result: SSHRunResult, message: str | None = None):
        self.ssh_run_result = ssh_run_result
        self.message = message

    def __str__(self):
        parts = [
            f"SSHRunResult has error",
            f"{self.ssh_run_result.ssh_runner.username}@{self.ssh_run_result.ssh_runner.hostname}:{self.ssh_run_result.ssh_runner.port}",
            f"return_code={str(self.ssh_run_result.return_code)}",
            f"err={str(self.ssh_run_result.err)}"
        ]
        if self.message is not None:
            parts.append(f"message={self.message}")
        return ', '.join(parts)

    def __repr__(self):
        return str(self)


class SSHRunResult(BaseModel):
    out: str
    err: str
    return_code: int | None = None
    ssh_runner: SSHRunner

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    def simple_dict(self) -> dict[str, Any]:
        return {
            "out": self.out,
            "err": self.err,
            "return_code": self.return_code,
            "has_bad_return_code": self.has_bad_return_code,
            "has_err": self.has_err,
            "has_out": self.has_out,
            "username": self.ssh_runner.username,
            "hostname": self.ssh_runner.hostname,
            "port": self.ssh_runner.port,
        }

    def simple_json(self) -> str:
        return transfer_data_to_json_str(
            self.simple_dict(),
            beautify=True,
            fast=False
        )

    def __repr__(self) -> str:
        return self.simple_json()

    def __str__(self) -> str:
        return self.simple_json()

    @property
    def has_bad_return_code(self) -> bool:
        if self.return_code is None:
            return False
        return self.return_code != 0

    @property
    def has_err(self) -> bool:
        if self.err:
            return True
        return False

    @property
    def has_out(self) -> bool:
        if self.out:
            return True
        return False

    def raise_for_bad_return_code(self):
        if self.has_bad_return_code:
            raise SSHRunResultHasErrorSSHException(ssh_run_result=self)

    def raise_for_err(self):
        if self.has_err:
            raise SSHRunResultHasErrorSSHException(ssh_run_result=self)


class SSHRunner:

    def __init__(
            self,
            *,
            username: str = "root",
            hostname: str,  # ipv4, ipv6, domain
            port: int = 22,
            password: str | None = None,
            base_timeout: float | None = None,
            check_if_already_connected: bool | None = True
    ):
        self.username = username
        self.hostname = hostname
        self.port = port
        self.password = password

        if base_timeout is None:
            base_timeout = timedelta(seconds=10).total_seconds()
        self.base_timeout = base_timeout

        if check_if_already_connected is None:
            check_if_already_connected = True
        self.check_if_already_connected = check_if_already_connected

        self._logger = logging.getLogger(
            f"{logging.getLogger(self.__class__.__name__)} - {self.username}@{self.hostname}:{self.port}"
        )

        self.async_conn: asyncssh.SSHClientConnection | None = None

        self.sync_client: paramiko.SSHClient | None = None

    """SYNC"""

    def sync_connect(
            self,
            *,
            common_timeout: float | None = None,
            connect_kwargs: dict[str, Any] | None = None,
            check_if_already_connected: bool | None = None
    ) -> SSHRunner:
        if check_if_already_connected is None:
            check_if_already_connected = self.check_if_already_connected

        if check_if_already_connected and self.sync_client is not None:
            self._logger.info("already connected")
            return self

        if connect_kwargs is None:
            connect_kwargs = {}
        if common_timeout is None:
            common_timeout = self.base_timeout

        connect_kwargs["hostname"] = self.hostname
        connect_kwargs["username"] = self.username
        connect_kwargs["password"] = self.password
        connect_kwargs["port"] = self.port

        if connect_kwargs.get("timeout") is None:
            connect_kwargs["timeout"] = common_timeout
        if connect_kwargs.get("auth_timeout") is None:
            connect_kwargs["auth_timeout"] = common_timeout
        if connect_kwargs.get("banner_timeout") is None:
            connect_kwargs["banner_timeout"] = common_timeout
        if connect_kwargs.get("channel_timeout") is None:
            connect_kwargs["channel_timeout"] = common_timeout

        self._logger.info("connecting")

        self.sync_client = paramiko.SSHClient()
        self.sync_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.sync_client.connect(**connect_kwargs)
        except Exception as exception:
            self._logger.error(f"not connected, {exception=}", exc_info=True)
            raise ConnectionSSHException(ssh_runner=self, base_exception=exception)

        self._logger.info("connected")

        return self

    def sync_check_connection(self):
        self.sync_connect()

    def sync_is_conn_good(self) -> bool:
        try:
            self.sync_check_connection()
        except ConnectionSSHException:
            return False
        except Exception:
            return False
        return True

    def sync_run(
            self,
            command: str,
            *,
            timeout: float | None = timedelta(seconds=10).total_seconds(),
            raise_for_bad_return_code: bool = True
    ) -> SSHRunResult:
        if not command or not command.strip():
            raise ValueError("command must be a non-empty string")

        if timeout is None:
            timeout = self.base_timeout

        self.sync_connect()

        self._logger.info(command)

        try:
            stdin, stdout, stderr = self.sync_client.exec_command(
                command=command,
                timeout=timeout
            )
            return_code = stdout.channel.recv_exit_status()
            stdout = stdout.read().decode()
            stderr = stderr.read().decode()
        except Exception as exception:
            raise ErrorInRunSSHException(ssh_runner=self, base_exception=exception)

        ssh_run_result = SSHRunResult(
            out=stdout,
            err=stderr,
            return_code=return_code,
            ssh_runner=self
        )

        if raise_for_bad_return_code:
            ssh_run_result.raise_for_bad_return_code()

        return ssh_run_result

    def sync_close(self):
        if self.sync_client is not None:
            self.sync_client.close()
            self.sync_client = paramiko.SSHClient()
            self.sync_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sync_client = None

    """ASYNC SYNC"""

    async def async_connect(
            self,
            *,
            common_timeout: float | None = None,
            connect_kwargs: dict[str, Any] | None = None,
            check_if_already_connected: bool | None = None
    ) -> SSHRunner:
        if check_if_already_connected is None:
            check_if_already_connected = self.check_if_already_connected

        if check_if_already_connected and self.async_conn is not None:
            self._logger.info("already connected")
            return self

        if connect_kwargs is None:
            connect_kwargs = {}
        if common_timeout is None:
            common_timeout = self.base_timeout

        connect_kwargs["host"] = self.hostname
        connect_kwargs["username"] = self.username
        connect_kwargs["password"] = self.password
        connect_kwargs["port"] = self.port

        if connect_kwargs.get("connect_timeout") is None:
            connect_kwargs["connect_timeout"] = common_timeout
        if connect_kwargs.get("login_timeout") is None:
            connect_kwargs["login_timeout"] = common_timeout

        connect_kwargs["known_hosts"] = None

        self._logger.info("connecting")

        try:
            self.async_conn = await asyncssh.connect(**connect_kwargs)
        except Exception as exception:
            self._logger.error(f"not connected, {exception=}", exc_info=True)
            raise ConnectionSSHException(ssh_runner=self, base_exception=exception)

        self._logger.info("connected")

        return self

    async def async_check_connection(self):
        await self.async_connect()

    async def async_is_conn_good(self) -> bool:
        try:
            await self.async_check_connection()
        except ConnectionSSHException:
            return False
        return True

    async def async_run(
            self,
            command: str,
            *,
            timeout: float | None = timedelta(seconds=10).total_seconds(),
            raise_for_bad_return_code: bool = True
    ) -> SSHRunResult:
        if not command or not command.strip():
            raise ValueError("command must be a non-empty string")

        if timeout is None:
            timeout = self.base_timeout

        await self.async_connect()

        self._logger.info(command)

        try:
            result: asyncssh.SSHCompletedProcess = await self.async_conn.run(
                command,
                check=False,
                timeout=timeout
            )
        except Exception as exception:
            raise ErrorInRunSSHException(ssh_runner=self, base_exception=exception)

        ssh_run_result = SSHRunResult(
            out=result.stdout,
            err=result.stderr,
            return_code=result.returncode,
            ssh_runner=self
        )

        if raise_for_bad_return_code:
            ssh_run_result.raise_for_bad_return_code()

        return ssh_run_result

    async def async_close(self):
        if self.async_conn is not None:
            self.async_conn.close()
            self.async_conn = None


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
