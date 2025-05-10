import pyautogui
import time

pyautogui.FAILSAFE = False
print("Keeping screen awake...")
while True:
    pyautogui.moveRel(10, 10)  # 微小移动鼠标
    time.sleep(1000)  # 每 5 分钟执行
    pyautogui.moveRel(-10, -10)  # 移回原位
    time.sleep(1000)  # 每 5 分钟执行