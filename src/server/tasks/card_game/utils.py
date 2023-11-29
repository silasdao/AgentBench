import os
import platform
import signal
import subprocess


def run_cmd(cmd_string, timeout=600):
    print(f"命令为：{cmd_string}")
    p = subprocess.Popen(
        cmd_string,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True,
        close_fds=True,
        start_new_session=True,
    )
    print("created")
    encoding = "gbk" if platform.system() == "Windows" else "utf-8"
    try:
        print("trying")
        (msg, errs) = p.communicate(timeout=timeout)
        print("comed")
        ret_code = p.poll()
        print("polled")
        if ret_code:
            code = 1
            msg = f"[Error]Called Error ： {str(msg.decode(encoding))}"
        else:
            code = 0
            msg = str(msg.decode(encoding))
        print(ret_code)
    except subprocess.TimeoutExpired:
        p.kill()
        p.terminate()
        os.killpg(p.pid, signal.SIGTERM)

        code = 1
        msg = f"[ERROR]Timeout Error : Command '{cmd_string}' timed out after {str(timeout)} seconds"
    except Exception as e:
        code = 1
        msg = f"[ERROR]Unknown Error : {str(e)}"

    print("returning")

    return code, msg
