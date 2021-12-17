# coding = utf8

import os

import pyautogui

os.path.abspath(".")

"""
    puautogui:控制鼠标和键盘操作
"""


# 获取当前屏幕分辨率
def getScreenResolution():
    screenWidth, screenHeight = pyautogui.size()
    return screenWidth, screenHeight


# 获取当前鼠标位置
def getMousePosition():
    currentMouseX, currentMouseY = pyautogui.position()
    return currentMouseX, currentMouseY


# 移动鼠标
def moveMouse():
    # moveTo绝对移动，移动到指定x、y坐标
    pyautogui.moveTo(x=200, y=200, duration=1, tween=pyautogui.linear)
    # pyautogui.click(x=100, y=100, clicks=1, interval=0.0, button="right", duration=0.0)
    # moveRel相对移动，相对当前坐标x、y offset
    # pyautogui.moveRel(xOffset=500, yOffset=500, duration=2, tween=pyautogui.linear)
    # pyautogui.doubleClick(x=None, y=None, interval=0.0, button="left", duration=0.0, tween=pyautogui.linear)
    # pyautogui.tripleClick(x=None, y=None, interval=0.0, button="left", duration=0.0, tween=pyautogui.linear)
    # pyautogui.rightClick()
    # pyautogui.middleClick()
    # pyautogui.moveTo(x=500, y=500, duration=2, tween=pyautogui.easeInOutQuad)
    # pyautogui.dragTo(x=427, y=535, duration=3, button="left")
    # pyautogui.dragRel(xOffset=100, yOffset=100, duration=1, button="left", mouseDownUp=False)
    # pyautogui.mouseDown(x=200, y=200, button="left")
    # pyautogui.mouseUp(x=300, y=300, button="left", duration=3)
    # pyautogui.scroll(100)
    # pyautogui.hscroll(100)
    pyautogui.vscroll(100)


# 键盘操作
def keyboard_operate():
    # pyautogui.typewrite(message="Hello world!", interval=0.5)
    # pyautogui.press("enter")
    # pyautogui.keyDown("shift")
    # pyautogui.keyUp("shift")
    # 模拟组合热键
    pyautogui.hotkey("ctrl", "c")


def alert_information():
    pyautogui.alert(text="This is an alert box.", title="Test")


def option_box():
    return pyautogui.confirm("enter option.", buttons=["a", "b", "c"])


def password_box():
    a = pyautogui.password("Enter your password(text will be hidden)")
    print(a)


def prompt_box():
    a = pyautogui.prompt("input message")
    print(a)


def screenshot_function():
    img_screenshot = pyautogui.screenshot()
    if not os.path.exists("./temp"):
        os.makedirs("./temp")
    else:
        img_screenshot.save("./seevision_pyqt5/screenshot_temp.png")
        img2 = pyautogui.screenshot("./seevision_pyqt5/screenshot_temp_2.png")


# 获取当前屏幕截图的中心点
def get_picture_center_point():
    screenshot_function()
    picture = pyautogui.locateOnScreen("./seevision_pyqt5/screenshot_temp.png")
    # (x, y) = pyautogui.center(picture)
    pyautogui.rightClick(pyautogui.center(picture))


def security_operate():
    # 保护措施，避免失控
    pyautogui.FAILSAFE = True
    # 为所有的pyautogui函数增加延时，默认0.1s
    pyautogui.PAUSE = 0.5


if __name__ == '__main__':
    security_operate()
    # print(getScreenResolution())
    # print(getMousePosition())
    # moveMouse()
    # print(getMousePosition())
    # keyboard_operate()
    # alert_information()
    # option_box()
    # password_box()
    # prompt_box()
    # screenshot_function()
    get_picture_center_point()
