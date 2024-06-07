import logging
import tkinter
import tkinter.messagebox
import atexit
from connection_pool import *
from manage import *
from tkinter import *
from PIL import ImageTk, Image

users = {
    'gaussdb': 'Lixiang@123',
    'admin': '123456'
}

# 设置日志输出格式和级别
logging.basicConfig(
    filename="output.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def login():
    """
    点击登录按钮调用函数
    :return:
    """
    username = str1.get()
    password = str2.get()
    pwd = users.get(username)
    if pwd is None or pwd != password:
        logger.error("Login failed")
        tkinter.messagebox.showerror("登录失败", "用户名或密码错误！")
        return None

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")  # 简单查询测试连接
            cursor.close()
            release_connection(conn)
            logger.info("Database connection test successful")
            open_main_window(win)
            tkinter.messagebox.showinfo("登录成功", "欢迎，管理员！")
        except Exception as error:
            release_connection(conn)
            logger.error(f"Database connection test failed: {error}")
            tkinter.messagebox.showerror("登录失败", f"数据库连接测试失败: {error}")
    else:
        logger.error("Database connection failed")
        tkinter.messagebox.showerror("登录失败", "数据库无法连接")
    return None


def cancel():
    """
    清空输入框
    :return:
    """
    str1.set("")
    str2.set("")
    return None


def center_window(window, width, height):
    """
    将win窗口放置到屏幕中央
    :param window: 窗口
    :param width: 窗口宽度
    :param height: 窗口高度
    :return: null
    """
    # 获取屏幕宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 计算窗口的x和y坐标
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # 设置窗口的尺寸和位置
    window.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == '__main__':

    # 设置登录窗口样式
    win = tkinter.Tk()
    win.withdraw()  # 先隐藏窗口
    win.geometry("500x400")
    win.title("用户登录界面")
    win.wm_iconbitmap('resources/icon.ico')
    win.iconbitmap('resources/icon.ico')

    # 放置屏幕中央
    center_window(win, 500, 400)

    # 创建顶部框架
    frma = tkinter.Frame(win)
    frma.pack(side="bottom")

    frmc = tkinter.Frame(win)
    frmc.pack(side="left")  # 左
    frmd = tkinter.Frame(win)
    frmd.pack(side="top")   # 右

    # 创建用户名输入框
    str1 = tkinter.StringVar(value="")
    Username = tkinter.Entry(frma, textvariable=str1, width=20)
    Username.grid(row=0, column=1, padx=10, pady=5)
    Ulabel = tkinter.Label(frma, text="用户名：")
    Ulabel.grid(row=0, column=0, pady=5, padx=10)

    # 创建密码输入框
    str2 = tkinter.StringVar(value="")
    Password = tkinter.Entry(frma, textvariable=str2, width=20, show="*")
    Password.grid(row=1, column=1, pady=5, padx=10)
    PLabel = tkinter.Label(frma, text="密码：")
    PLabel.grid(row=1, column=0, padx=10, pady=5)

    # 创建重置按钮和登录按钮
    resbtn = tkinter.Button(frma, text="重置", command=cancel)
    resbtn.grid(row=2, column=0, padx=10, pady=5)
    logbtn = tkinter.Button(frma, text="登录", command=login)
    logbtn.grid(row=2, column=1, padx=10, pady=5)

    # 创建底部框架
    frmb = tkinter.Frame(win)
    frmb.pack(side="top")

    # 打开指定的图片文件，缩放至指定尺寸
    def get_image(filename, width, height):
        im = Image.open(filename).resize((width, height))
        return ImageTk.PhotoImage(im)

    # 创建画布，设置要显示的图片，把画布添加至应用程序窗口
    canvas_root = tkinter.Canvas(frmb, width=560, height=300)
    im_root = get_image("resources/login_cover.jpg", 560, 300)
    canvas_root.create_image(216, 150, image=im_root)
    canvas_root.pack()

    win.resizable(False, False)

    # 确保所有布局和图像加载完成
    win.update_idletasks()
    win.deiconify()  # 显示窗口

    # 进入主循环
    win.mainloop()

    # 应用退出时关闭所有连接
    atexit.register(close_all_connections)
    logger.info("Application shut down")
