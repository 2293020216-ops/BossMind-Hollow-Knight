import logging
import time

from bossmind.env_tools.memory import PlayerInfo

logging.basicConfig(level=logging.WARNING)

player = PlayerInfo()
try:
    player.attach()
    while True:
        print(player.get_player_hp())
        time.sleep(0.2)
except KeyboardInterrupt:
    print("退出")
except ValueError as e:
    print(f"错误: {e}")
finally:
    player.detach()
