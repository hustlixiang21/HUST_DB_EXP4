from tkinter import *
from tkinter import messagebox, ttk
from main import center_window
from postgresSQL import Manage_Student_Info  # 导入学生信息管理模块
from postgresSQL import Manage_Course_Info  # 导入课程信息管理模块
from postgresSQL import Manage_Grade_Info  # 导入成绩信息管理模块
from postgresSQL import DB_Info  # 导入数据库信息模块


def manage_student_info():
    """
    展示学生信息增、删、改的UI，并使用postgresSQL.Manage_Student_Info模块中的check_params、insert_student_info、update_student_info和delete_student_info方法进行SQL语句执行
    :return: None
    """
    # 清除 main_frame 的内容
    clear_main_frame()
    Label(main_frame, text="学生信息管理", font=('Arial', 16)).grid(row=0, column=0, columnspan=4, pady=20,
                                                                    padx=10, sticky='nsew')

    sno_var = StringVar()
    sname_var = StringVar()
    ssex_var = StringVar()
    sage_var = StringVar()
    sdept_var = StringVar()
    scholarship_var = StringVar()

    # 学号标签和输入框
    Label(main_frame, text="学号:", anchor='e').grid(row=1, column=0, pady=15, padx=10, sticky='e')
    sno_entry = Entry(main_frame, textvariable=sno_var)
    sno_entry.grid(row=1, column=1, pady=5, padx=10, sticky='we')

    # 姓名标签和输入框
    Label(main_frame, text="姓名:", anchor='e').grid(row=1, column=2, pady=15, padx=10, sticky='e')

    sname_entry = Entry(main_frame, textvariable=sname_var)
    sname_entry.grid(row=1, column=3, pady=5, padx=10, sticky='we')

    # 性别标签和输入框
    Label(main_frame, text="性别:", anchor='e').grid(row=2, column=0, pady=15, padx=10, sticky='e')
    ssex_options = ['男', '女']
    ssex_menu = OptionMenu(main_frame, ssex_var, *ssex_options)
    ssex_menu.config(bg='white')
    ssex_menu.grid(row=2, column=1, pady=5, padx=10, sticky='we')

    # 年龄标签和输入框
    Label(main_frame, text="年龄:", anchor='e').grid(row=2, column=2, pady=15, padx=10, sticky='e')
    sage_entry = Entry(main_frame, textvariable=sage_var)
    sage_entry.grid(row=2, column=3, pady=5, padx=10, sticky='we')

    # 系别标签和输入框
    Label(main_frame, text="系别:", anchor='e').grid(row=3, column=0, pady=15, padx=10, sticky='e')
    sdept_options = ['CS', 'IS', 'MA']
    sdept_menu = OptionMenu(main_frame, sdept_var, *sdept_options)
    sdept_menu.config(bg='white')
    sdept_menu.grid(row=3, column=1, pady=5, padx=10, sticky='we')

    # 奖学金标签和输入框
    Label(main_frame, text="奖学金:", anchor='e').grid(row=3, column=2, pady=15, padx=10, sticky='e')
    scholarship_options = ['是', '否']
    scholarship_menu = OptionMenu(main_frame, scholarship_var, *scholarship_options)
    scholarship_menu.config(bg='white')
    scholarship_menu.grid(row=3, column=3, pady=5, padx=10, sticky='we')

    def cancel():
        """
        清空所有输入框的内容
        :return: None
        """
        sno_var.set('')
        sname_var.set('')
        ssex_var.set('')
        sage_var.set('')
        sdept_var.set('')
        scholarship_var.set('')
        return

    def button_type(Btype) -> any:
        """
        根据点击不同Button调用不同的函数
        :param Btype: button编号
        :return: ANY
        """
        sno = sno_var.get()
        sname = sname_var.get()
        ssex = ssex_var.get()
        sage = sage_var.get()
        sdept = sdept_var.get()
        scholarship = scholarship_var.get()

        if not Manage_Student_Info.check_params(sno, sname, ssex, sage, sdept, scholarship):
            return None
        if Btype == 1:
            Manage_Student_Info.insert_student_info(sno, sname, ssex, sage, sdept, scholarship)
        elif Btype == 2:
            Manage_Student_Info.update_student_info(sno, sname, ssex, sage, sdept, scholarship)
        else:
            Manage_Student_Info.delete_student_info(sno, sname, ssex, sage, sdept, scholarship)
        return None

    # 创建一个新的框架来放置按钮
    button_frame = Frame(main_frame, bg='white')
    button_frame.grid(row=4, column=0, columnspan=4, pady=20, sticky='we')

    # 插入、更新、删除和重置按钮
    insert_button = Button(button_frame, text="插入", command=lambda: button_type(1))
    insert_button.grid(row=0, column=0, padx=20, sticky='we')

    update_button = Button(button_frame, text="更新", command=lambda: button_type(2))
    update_button.grid(row=0, column=1, padx=20, sticky='we')

    delete_button = Button(button_frame, text="删除", command=lambda: button_type(3))
    delete_button.grid(row=0, column=2, padx=20, sticky='we')

    cancel_button = Button(button_frame, text="重置", command=cancel)
    cancel_button.grid(row=0, column=3, padx=20, sticky='we')

    # 配置按钮框架的列权重，使按钮能够水平扩展以填满框架
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)
    button_frame.columnconfigure(3, weight=1)

    # 配置每列的权重，使输入框能够水平扩展以填满窗口
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)
    main_frame.columnconfigure(3, weight=1)


def manage_course_info():
    """
    展示课程信息增、删、改的UI，使用postgresSQL.Manage_Course_Info模块中的check_params、insert_course_info、update_course_info、delete_course_info和delete_courses_without_enrollments方法进行SQL语句执行
    :return: None
    """
    # 清除 main_frame 的内容
    clear_main_frame()
    Label(main_frame, text="课程信息管理", font=('Arial', 16)).grid(row=0, column=0, columnspan=4, pady=20, padx=10,
                                                                    sticky='nsew')

    cno_var = StringVar()
    cname_var = StringVar()
    cpno_var = StringVar()
    ccredit_var = StringVar()

    # 课程号标签和输入框
    Label(main_frame, text="课程号:", anchor='e').grid(row=1, column=0, pady=15, padx=10, sticky='e')
    cno_entry = Entry(main_frame, textvariable=cno_var)
    cno_entry.grid(row=1, column=1, pady=5, padx=10, sticky='we')

    # 课程名标签和输入框
    Label(main_frame, text="课程名:", anchor='e').grid(row=1, column=2, pady=15, padx=10, sticky='e')
    cname_entry = Entry(main_frame, textvariable=cname_var)
    cname_entry.grid(row=1, column=3, pady=5, padx=10, sticky='we')

    # 先修课标签和输入框
    Label(main_frame, text="先修课:", anchor='e').grid(row=2, column=0, pady=15, padx=10, sticky='e')
    cpno_entry = Entry(main_frame, textvariable=cpno_var)
    cpno_entry.grid(row=2, column=1, pady=5, padx=10, sticky='we')

    # 学分标签和输入框
    Label(main_frame, text="学分:", anchor='e').grid(row=2, column=2, pady=15, padx=10, sticky='e')
    ccredit_entry = Entry(main_frame, textvariable=ccredit_var)
    ccredit_entry.grid(row=2, column=3, pady=5, padx=10, sticky='we')

    def cancel():
        """
        清空所有输入框的内容
        :return: None
        """
        cno_var.set('')
        cname_var.set('')
        cpno_var.set('')
        ccredit_var.set('')
        return

    def button_type(Btype) -> any:
        """
        根据点击不同Button调用不同的函数
        :param Btype: button编号
        :return: ANY
        """
        cno = cno_var.get()
        cname = cname_var.get()
        cpno = cpno_var.get()
        ccredit = ccredit_var.get()

        if not Manage_Course_Info.check_params(cno, cname, cpno, ccredit):
            return None
        if Btype == 1:
            Manage_Course_Info.insert_course_info(cno, cname, cpno, ccredit)
        elif Btype == 2:
            Manage_Course_Info.update_course_info(cno, cname, cpno, ccredit)
        elif Btype == 3:
            Manage_Course_Info.delete_course_info(cno, cname, cpno, ccredit)
        return None

    # 创建一个新的框架来放置按钮
    button_frame = Frame(main_frame, bg='white')
    button_frame.grid(row=3, column=0, columnspan=4, pady=20, sticky='we')

    # 插入、更新、删除和重置按钮
    insert_button = Button(button_frame, text="插入", command=lambda: button_type(1))
    insert_button.grid(row=0, column=0, padx=20, sticky='we')

    update_button = Button(button_frame, text="更新", command=lambda: button_type(2))
    update_button.grid(row=0, column=1, padx=20, sticky='we')

    delete_button = Button(button_frame, text="删除", command=lambda: button_type(3))
    delete_button.grid(row=0, column=2, padx=20, sticky='we')

    cancel_button = Button(button_frame, text="重置", command=cancel)
    cancel_button.grid(row=0, column=3, padx=20, sticky='we')

    # 创建一个新的框架来放置按钮
    delete_button_frame = Frame(main_frame, bg='white')
    delete_button_frame.grid(row=4, column=0, columnspan=4, pady=5, sticky='we')

    delete_not_choose_button = Button(delete_button_frame, text="删除没有学生选择的课程信息",
                                      command=Manage_Course_Info.delete_courses_without_enrollments)
    delete_not_choose_button.grid(row=0, column=1, columnspan=2, padx=20, sticky='we')

    # 配置按钮框架的列权重，使按钮能够水平扩展以填满框架
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)
    button_frame.columnconfigure(3, weight=1)

    # 配置按钮框架的列权重，使按钮能够水平扩展以填满框架
    delete_button_frame.columnconfigure(0, weight=1)
    delete_button_frame.columnconfigure(1, weight=1)
    delete_button_frame.columnconfigure(2, weight=1)
    delete_button_frame.columnconfigure(3, weight=1)

    # 配置每列的权重，使输入框能够水平扩展以填满窗口
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)
    main_frame.columnconfigure(3, weight=1)


def manage_grade_entry():
    """
    展示学生成绩增、删、改的UI，使用postgresSQL.Manage_Grade_Info模块中的insert_grade_info、update_grade_info和delete_grade_info方法进行SQL语句执行
    :return: None
    """
    # 清除 main_frame 的内容
    clear_main_frame()
    Label(main_frame, text="学生成绩管理", font=('Arial', 16)).grid(row=0, column=0, columnspan=4, pady=20, padx=10,
                                                                    sticky='nsew')

    sno_var = StringVar()
    cno_var = StringVar()
    grade_var = StringVar()

    # 学号标签和输入框
    Label(main_frame, text="学号:", anchor='e').grid(row=1, column=0, pady=15, padx=10, sticky='e')
    sno_entry = Entry(main_frame, textvariable=sno_var)
    sno_entry.grid(row=1, column=1, pady=5, padx=10, sticky='we')

    # 课程号标签和输入框
    Label(main_frame, text="课程号:", anchor='e').grid(row=1, column=2, pady=15, padx=10, sticky='e')
    cno_entry = Entry(main_frame, textvariable=cno_var)
    cno_entry.grid(row=1, column=3, pady=5, padx=10, sticky='we')

    # 成绩标签和输入框
    Label(main_frame, text="成绩:", anchor='e').grid(row=2, column=0, pady=15, padx=10, sticky='e')
    grade_entry = Entry(main_frame, textvariable=grade_var)
    grade_entry.grid(row=2, column=1, pady=5, padx=10, sticky='we')

    def cancel():
        """
        清空所有输入框的内容
        :return: None
        """
        sno_var.set('')
        cno_var.set('')
        grade_var.set('')
        return

    def button_type(Btype) -> any:
        """
        根据点击不同Button调用不同的函数
        :param Btype: button编号
        :return: ANY
        """
        sno = sno_var.get()
        cno = cno_var.get()
        grade = grade_var.get()

        if not Manage_Grade_Info.check_params(sno, cno, grade):
            return None
        if Btype == 1:
            Manage_Grade_Info.insert_grade_info(sno, cno, grade)
        elif Btype == 2:
            Manage_Grade_Info.update_grade_info(sno, cno, grade)
        else:
            Manage_Grade_Info.delete_grade_info(sno, cno, grade)
        return None

    # 创建一个新的框架来放置按钮
    button_frame = Frame(main_frame, bg='white')
    button_frame.grid(row=3, column=0, columnspan=4, pady=20, sticky='we')

    # 插入、更新和删除按钮
    insert_button = Button(button_frame, text="插入", command=lambda: button_type(1))
    insert_button.grid(row=0, column=0, padx=20, sticky='we')

    update_button = Button(button_frame, text="更新", command=lambda: button_type(2))
    update_button.grid(row=0, column=1, padx=20, sticky='we')

    delete_button = Button(button_frame, text="删除", command=lambda: button_type(3))
    delete_button.grid(row=0, column=2, padx=20, sticky='we')

    cancel_button = Button(button_frame, text="重置", command=cancel)
    cancel_button.grid(row=0, column=3, padx=20, sticky='we')

    # 配置按钮框架的列权重，使按钮能够水平扩展以填满框架
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)
    button_frame.columnconfigure(3, weight=1)

    # 配置每列的权重，使输入框能够水平扩展以填满窗口
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)
    main_frame.columnconfigure(3, weight=1)


def show_statistics():
    """
    显示按系统计学生成绩信息的UI，使用Manage_Grade_Info模块中的get_grade_info_group_by_sdept方法执行SQL获取返回数据
    :return: None
    """
    clear_main_frame()
    Label(main_frame, text="按系统计学生成绩", font=('Arial', 16)).grid(row=0, column=0, columnspan=4, pady=20, padx=10,
                                                                        sticky='nsew')

    def fetch_statistics():
        try:
            results = Manage_Grade_Info.get_grade_info_group_by_sdept()
            if results and results[0][0] == 'ERROR':
                messagebox.showerror("错误", results[0][1])
                return

            # 创建一个新的窗口来显示查询结果
            result_window = Toplevel()
            result_window.title("统计结果")

            # 创建Treeview表格
            tree = ttk.Treeview(result_window,
                                columns=('系别', '平均成绩', '最好成绩', '最差成绩', '优秀率', '不及格人数'),
                                show='headings')
            tree.heading('系别', text='系别')
            tree.heading('平均成绩', text='平均成绩')
            tree.heading('最好成绩', text='最好成绩')
            tree.heading('最差成绩', text='最差成绩')
            tree.heading('优秀率', text='优秀率')
            tree.heading('不及格人数', text='不及格人数')

            tree.column('系别', anchor='center', width=100)
            tree.column('平均成绩', anchor='center', width=100)
            tree.column('最好成绩', anchor='center', width=100)
            tree.column('最差成绩', anchor='center', width=100)
            tree.column('优秀率', anchor='center', width=100)
            tree.column('不及格人数', anchor='center', width=100)

            for data in results:
                tree.insert('', 'end', values=data)

            tree.pack(expand=True, fill='both')

        except Exception as e:
            messagebox.showerror("错误", f"统计成绩时出错: {str(e)}")

    search_button = Button(main_frame, text="统计学生成绩", command=fetch_statistics)
    search_button.grid(row=1, column=1, columnspan=2, pady=5, padx=10, sticky='we')

    # 配置每列的权重，使按钮能够水平扩展以填满窗口
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)
    main_frame.columnconfigure(3, weight=1)


def show_ranking():
    """
    显示按系统计学生成绩排名的UI，使用Manage_Grade_Info模块中的get_ranking_info_group_by_sdept方法执行SQL获取返回数据
    :return: None
    """
    clear_main_frame()
    Label(main_frame, text="按系对学生成绩排名", font=('Arial', 16)).grid(row=0, column=0, columnspan=4, pady=20,
                                                                          padx=10, sticky='nsew')

    def fetch_ranking():
        try:
            results = Manage_Grade_Info.get_ranking_info_group_by_sdept()
            if results and results[0][0] == 'ERROR':
                messagebox.showerror("错误", results[0][1])
                return

            # 创建一个新的窗口来显示查询结果
            result_window = Toplevel()
            result_window.title("排名结果")

            # 创建Treeview表格
            tree = ttk.Treeview(result_window, columns=('系别', '学号', '姓名', '课程号', '课程名', '成绩'),
                                show='headings')
            tree.heading('系别', text='系别')
            tree.heading('学号', text='学号')
            tree.heading('姓名', text='姓名')
            tree.heading('课程号', text='课程')
            tree.heading('课程名', text='课程名')
            tree.heading('成绩', text='成绩')

            tree.column('系别', anchor='center', width=100)
            tree.column('学号', anchor='center', width=100)
            tree.column('姓名', anchor='center', width=100)
            tree.column('课程号', anchor='center', width=100)
            tree.column('课程名', anchor='center', width=100)
            tree.column('成绩', anchor='center', width=100)

            for data in results:
                tree.insert('', 'end', values=data)

            tree.pack(expand=True, fill='both')

        except Exception as e:
            messagebox.showerror("错误", f"查询排名时出错: {str(e)}")

    # 查询按钮
    search_button = Button(main_frame, text="查询排名", command=fetch_ranking)
    search_button.grid(row=1, column=1, columnspan=2, pady=5, padx=10, sticky='we')

    # 配置每列的权重，使按钮能够水平扩展以填满窗口
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)
    main_frame.columnconfigure(3, weight=1)


def show_student_details():
    """
    显示查询学生详细信息的UI，使用Manage_Student_Info模块中的query_student_info方法进行SQL查询获取返回数据
    :return: None
    """
    clear_main_frame()
    Label(main_frame, text="根据学号查询学生详细信息", font=('Arial', 16)).grid(row=0, column=0, columnspan=4, pady=20,
                                                                                padx=10, sticky='nsew')

    sno_var = StringVar()

    Label(main_frame, text="学号:", anchor='e').grid(row=1, column=0, pady=10, padx=10, sticky='e')
    sno_entry = Entry(main_frame, textvariable=sno_var)
    sno_entry.grid(row=1, column=1, pady=5, padx=10, sticky='we')

    def search_student():
        sno = sno_var.get()
        if not sno:
            messagebox.showerror('错误', '学号不能为空！')
            return

        try:
            results = Manage_Student_Info.query_student_info(sno)

            # 如果没有找到该学号的学生信息
            if not results:
                messagebox.showinfo("信息", "没有找到该学号的学生信息")
                return

            # 有返回结果但是是错误信息
            if results and results[0][0] == 'ERROR':
                messagebox.showerror("错误", results[0][1])
                return

            result_window = Toplevel()
            result_window.title("查询结果")

            # 创建Treeview表格
            tree = ttk.Treeview(result_window,
                                columns=('学号', '姓名', '性别', '年龄', '系别', '课程号', '课程名', '成绩'),
                                show='headings')
            tree.heading('学号', text='学号')
            tree.heading('姓名', text='姓名')
            tree.heading('性别', text='性别')
            tree.heading('年龄', text='年龄')
            tree.heading('系别', text='系别')
            tree.heading('课程号', text='课程号')
            tree.heading('课程名', text='课程名')
            tree.heading('成绩', text='成绩')

            tree.column('学号', anchor='center', width=100)
            tree.column('姓名', anchor='center', width=100)
            tree.column('性别', anchor='center', width=100)
            tree.column('年龄', anchor='center', width=100)
            tree.column('系别', anchor='center', width=100)
            tree.column('课程号', anchor='center', width=100)
            tree.column('课程名', anchor='center', width=100)
            tree.column('成绩', anchor='center', width=100)

            # 插入查询结果
            for data in results:
                tree.insert('', 'end', values=data)

            tree.pack(expand=True, fill='both')

        except Exception as e:
            messagebox.showerror("错误", f"查询学生信息时出错: {str(e)}")

    search_button = Button(main_frame, text="查询", command=search_student)
    search_button.grid(row=1, column=2, pady=5, padx=10, sticky='we')

    # 配置每列的权重，使输入框能够水平扩展以填满窗口
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)
    main_frame.columnconfigure(3, weight=1)


def clear_main_frame():
    """
    清空主界面内容用于加载新的界面
    :return:
    """
    for widget in main_frame.winfo_children():
        widget.destroy()


def on_closing(login_window):
    """
    关系系统主界面关闭时调用
    :param login_window:
    :return:
    """
    login_window.destroy()  # 销毁主窗口


def open_main_window(login_window):
    """
    打开管理系统主界面
    :param login_window: 登录窗口
    :return:
    """
    global main_frame
    login_window.withdraw()  # 隐藏主窗口
    main_win = Toplevel()
    main_win.geometry("600x400")
    main_win.title("管理系统")
    main_win.wm_iconbitmap('resources/icon.ico')
    main_win.iconbitmap('resources/icon.ico')
    center_window(main_win, 600, 400)

    # 绑定关闭事件
    main_win.protocol("WM_DELETE_WINDOW", lambda: on_closing(login_window))

    sidebar = Frame(main_win, width=150, bg='lightgrey', height=400, relief='sunken', borderwidth=2)
    sidebar.pack(expand=False, fill='both', side='left', anchor='nw')
    sidebar.pack_propagate(False)  # 阻止 sidebar 调整大小

    main_frame = Frame(main_win, bg='white', width=450, height=400)
    main_frame.pack(expand=True, fill='both', side='right')

    Button(sidebar, text="学生信息维护", command=manage_student_info).pack(fill=X)
    Button(sidebar, text="课程信息维护", command=manage_course_info).pack(fill=X)
    Button(sidebar, text="学生成绩维护", command=manage_grade_entry).pack(fill=X)
    Button(sidebar, text="统计学生成绩", command=show_statistics).pack(fill=X)
    Button(sidebar, text="学生成绩排名", command=show_ranking).pack(fill=X)
    Button(sidebar, text="学生信息查询", command=show_student_details).pack(fill=X)

    def show_database_info():
        """
        显示数据库的相关信息
        """
        clear_main_frame()

        # 设置标题
        Label(main_frame, text="数据库详情", font=('Arial', 16)).pack(anchor='n', pady=10)

        info = DB_Info.fetch_database_info()

        if "error" in info:
            Label(main_frame, text=f"获取表时出错: {info['error']}", wraplength=500, bg='white').pack(anchor='w',
                                                                                                      padx=10, pady=5)
        else:
            Label(main_frame, text=f"数据库版本: {info['db_version']}", wraplength=447, bg='white').pack(anchor='w',
                                                                                                         padx=10,
                                                                                                         pady=5)
            Label(main_frame, text=f"当前用户: {info['current_user']}", wraplength=447, bg='white').pack(anchor='w',
                                                                                                         padx=10,
                                                                                                         pady=5)
            Label(main_frame, text=f"已连接数据库: {info['current_database']}", wraplength=447, bg='white').pack(
                anchor='w', padx=10, pady=5)
            Label(main_frame, text="数据库中的表:", wraplength=447, bg='white').pack(anchor='w', padx=10, pady=5)

            for table in info['tables']:
                Label(main_frame, text=f" - {table[0]}", wraplength=447, bg='white').pack(anchor='w', padx=20, pady=2)

    show_database_info()
