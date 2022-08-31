import typing
import os
import subprocess
import time
import functools
from loguru import logger
import psutil


def proc_output(cmd: str, decode=True):
    """subprocess.check_output()
    """
    try:
        res = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        logger.error(e)
        raise
    if decode:
        return res.decode()
    return res


def proc(cmd: str):
    """subprocess
    """
    return subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def start(proc_name: str, cmd: str, pre_kill: bool = True):
    """start a proc

    proc_name: proc_name keywords
    cmd: cmd
    pre_kill: before start whether kill or not, default True
    """
    if pre_kill:
        kill(proc_name)
    logger.info(f'========= START RECORD ==========')
    return proc(cmd)


def stop(proc_name: str, _proc: subprocess.Popen):
    """stop a proc

    proc_name: proc_name keywords
    """
    try:
        assert _proc.poll() is None, f"run command failed"
        _proc.terminate()
        kill_pid(_proc)
        logger.info(f'========== STOP RECORD ==========')
    except Exception as e:
        logger.error(e)
        kill(proc_name)


def process_is_exist(process_name: str):
    cmd = "ps -ef | grep '%s' | grep -v 'grep' | awk '{print $2}'" % process_name
    if proc_output(cmd):
        return True
    else:
        return False


def kill_pid(_proc: subprocess.Popen):
    """
    kill pid
    """
    pobj = psutil.Process(_proc.pid)
    for c in pobj.children(recursive=True):
        c.kill()
    pobj.kill()


def kill(process_name: str):
    """kill a specified proc by `kill -9 pid`

    """
    if process_is_exist(process_name):
        kill_cmd = "ps -ef | grep '%s' | grep -v 'grep' | awk '{print $2}' | xargs kill -9" % process_name
        proc(kill_cmd)
        time.sleep(1)
        logger.info(f'=== KILL PROCESS: {process_name} ===')


def xrecord_path():
    return os.path.join(os.path.dirname(__file__), 'xrecord')


def _cmd(platform: str, high_dfn: bool, **kwargs):
    """build cmd according to platform
    """
    platform = platform.lower()
    assert platform in ('a', 'android', 'i', 'ios'), f"platform should in ('a', 'android', 'i', 'ios')"
    if platform in ('a', 'android'):
        if high_dfn:
            cmd_str = 'scrcpy -s "{device}" --render-expired-frames -Nr "{fp}"'
        else:
            cmd_str = 'scrcpy -s "{device}" -Nr "{fp}"'
        cmd = cmd_str.format(**kwargs)
        proc_name = 'scrcpy'
    else:
        if high_dfn:
            cmd_str = '"{xrecord}" -q -i "{device}" -o "{fp}" -f'
        else:
            cmd_str = '"{xrecord}" -q -i "{device}" -o "{fp}" -u medium -f'
        kwargs['xrecord'] = xrecord_path()
        cmd = cmd_str.format(**kwargs)
        proc_name = 'xrecord'
    logger.info(
        f'\n===== CMD INFO ====='
        f'\nplatform: {platform}'
        f'\ncmd: {cmd}'
        f'\n===================='
    )
    return proc_name, cmd


def _update_offset(offset):
    assert isinstance(offset, tuple), 'offset type should be tuple'
    assert len(offset) <= 2, 'len(offset) should <= 2'
    offset = offset or (1, 1)
    offset = offset if len(offset) == 2 else (offset[0], 0)
    logger.info(f'current case offset: {offset}')
    return offset


def record(platform: str, device: str,
           file_path: typing.Union[str, os.PathLike],
           offset: tuple = (1, 1),
           pre_kill: bool = True,
           high_dfn: bool = True
           ):
    """record wrapper

    platform: 'a', 'android', 'i', 'ios'
    device: android device id or iOS udid
    file_path: mp4 file path
    offset: default (1, 1), mean of: before record sleep 1s and after record sleep 1s
    pre_kill: before start whether kill or not, default True
    high_dfn: record video in high definition
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ofs = _update_offset(offset)
            proc_name, cmd = _cmd(platform, high_dfn, device=device, fp=file_path)
            p = start(proc_name, cmd, pre_kill)
            try:
                time.sleep(ofs[0])
                func(*args, **kwargs)
                time.sleep(ofs[1])
            except Exception as e:
                logger.error(e)
            finally:
                stop(proc_name, p)

        return wrapper

    return decorator
