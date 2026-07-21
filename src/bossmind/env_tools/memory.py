import pymem
import yaml
from bossmind.paths import GAME_VERSION_FILE

def get_pid():
    # 校验配置文件是否存在
    if not GAME_VERSION_FILE.exists():
        raise FileNotFoundError(f"配置文件不存在: {GAME_VERSION_FILE}")

    # 读取配置文件，获取进程名
    with open(GAME_VERSION_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        process_name = config["process_name"]

    # 获取pid
    try:
        pm = pymem.Pymem(process_name)
        # 获取pid
        pid = pm.process_id
        # 关闭句柄
        pm.close_process()
        return pid
    except pymem.exception.ProcessNotFound:
        raise ValueError(f"未找到进程: {process_name}")
    except pymem.exception.CouldNotOpenProcess:
        raise ValueError(f"打开进程失败: {process_name}")

if __name__ == "__main__":
    print(get_pid())