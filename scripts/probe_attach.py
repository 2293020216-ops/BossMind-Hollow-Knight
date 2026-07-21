import pymem

process_name = "pycharm64.exe"

# 获取pid
try:
    pm = pymem.Pymem(process_name)
    # 获取pid
    pid = pm.process_id
    print("已获取到pycharm的pid，pid为：",pid)
    # 获取进程句柄
    print("进程句柄为：",pm.process_handle)
    # 关闭句柄
    pm.close_process()
except pymem.exception.ProcessNotFound:
    print("未找到进程")
except pymem.exception.CouldNotOpenProcess:
    print("打开进程失败")