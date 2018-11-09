import os
import sys
import time
from subprocess import Popen
from shlex import quote


def sleep(sec):
    time.sleep(sec)
    return sec


def fuzz_one_func(repo, fn):
    os.chdir(repo)
    os.chdir(fn)
    with open('/dev/null', 'wb')  as devnull:
        with open('stdout.txt', 'wb') as stdout:
            input_dir = 'inputs'
            output_dir = 'outputs'
            memory_size = '1000'
            target = 'driver.py'
            cmdline = ['py-afl-fuzz', '-i', input_dir, '-o', output_dir, '-m', memory_size, '--', sys.executable, target]
            print('$', ' '.join(quote(arg) for arg in cmdline))
            afl = Popen(
                cmdline,
                stdout=stdout,
                stdin=devnull
            )
    try:
        timeout = 6 * 3600
        timeout = 20
        while timeout > 0:
            if afl.poll() is not None:
                break
            timeout -= sleep(10)
        if afl.returncode is None:
            afl.terminate()
            afl.wait()
    except:
        afl.kill()
        raise
    os.chdir('..')
    os.chdir('..')