import os
import sys
import time
from subprocess import Popen
from shlex import quote
from fuzzing.config import DRIVER_TEMP


def sleep(sec):
    time.sleep(sec)
    return sec


def create_fuzz_dir(repo, succ_dict):
    if not os.path.exists(repo):
        os.mkdir(repo)
    os.chdir(repo)
    for mod in succ_dict:
        for fn in succ_dict[mod]:
            if not os.path.exists(fn):
                os.mkdir(fn)
            os.chdir(fn)
            if not os.path.exists('inputs'):
                os.mkdir('inputs')
            os.chdir('inputs')
            for i, args in enumerate(succ_dict[mod][fn]):
                with open(f'input_{i:03}.txt', mode='w', encoding='utf-8') as wf:
                    for arg in args:
                        wf.write(f'{arg}\n')
            os.chdir('..')
            if not os.path.exists('driver.py'):
                with open('driver.py', 'w', encoding='utf-8') as wf:
                    wf.write(DRIVER_TEMP % {"mod":mod, "func":fn})
            os.chdir('..')
    os.chdir('..')


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
