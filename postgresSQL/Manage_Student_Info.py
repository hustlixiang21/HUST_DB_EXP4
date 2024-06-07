import re
from tkinter import messagebox
from connection_pool import *
from main import logger


def check_params(sno, sname, ssex, sage, sdept, scholarship) -> bool:
    """
    检查student表各参数的取值范围，但只是初步判断，比如主键，外键冲突这类错误要交给数据库判断
    :param sno: 学号
    :param sname: 姓名
    :param ssex: 性别
    :param sage: 年龄
    :param sdept: 系别
    :param scholarship: 奖学金
    :return:
    """

    if not sno and not sname and not ssex and not sage and not sdept and not scholarship:
        messagebox.showwarning("输入错误", "请输入学生信息")
        return False

    if sno and not re.fullmatch(r'\d{9}', sno):
        messagebox.showwarning("输入错误", "学号应为9位数字")
        return False

    # 姓名应为中文
    if sname and not re.fullmatch(r'[\u4e00-\u9fa5]+', sname):
        messagebox.showwarning("输入错误", "姓名应为中文")
        return False

    # 年龄应大于0且小于100
    if sage:
        try:
            sage = int(sage)
            if sage <= 0 or sage >= 100:
                messagebox.showwarning("输入错误", "年龄应大于0且小于100")
                return False
        except ValueError:
            messagebox.showwarning("输入错误", "年龄必须是数字")
            return False

    return True


def insert_student_info(sno, sname, ssex, sage, sdept, scholarship) -> bool:
    """
    插入学生信息到数据库
    :param sno: 学号
    :param sname: 姓名
    :param ssex: 性别
    :param sage: 年龄
    :param sdept: 系别
    :param scholarship: 奖学金
    :return: 是否成功
    """
    if not sno or not sname:
        messagebox.showerror('错误', '学号和姓名不能为空！')
        return False
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO Student (sno, sname, ssex, sage, sdept, scholarship) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (sno if sno else None, sname if sname else None, ssex if ssex else None, sage if sage else None,
                      sdept if sdept else None, scholarship if scholarship else None))
            conn.commit()
            cursor.close()
            release_connection(conn)
            logger.info(f"Successfully inserted student info: sno={sno}, sname={sname}, ssex={ssex}, sage={sage}, sdept={sdept}, scholarship={scholarship}")
            messagebox.showinfo("成功", "学生信息已插入")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to insert student info: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            messagebox.showerror("错误", f"插入学生信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return False
    else:
        messagebox.showerror("错误", "无法连接数据库")
        logger.error("Failed to connect to the database for inserting student info")
        return False
    return True


def update_student_info(sno, sname, ssex, sage, sdept, scholarship) -> bool:
    """
    更新学生信息到数据库
    :param sno: 学号
    :param sname: 姓名
    :param ssex: 性别
    :param sage: 年龄
    :param sdept: 系别
    :param scholarship: 奖学金
    :return: 是否成功
    """
    if not sno:
        messagebox.showerror('错误', '学号不能为空！')
        return False

    update_fields = []
    update_values = []

    if sname:
        update_fields.append("sname = %s")
        update_values.append(sname)
    if ssex:
        update_fields.append("ssex = %s")
        update_values.append(ssex)
    if sage:
        update_fields.append("sage = %s")
        update_values.append(sage)
    if sdept:
        update_fields.append("sdept = %s")
        update_values.append(sdept)
    if scholarship:
        update_fields.append("scholarship = %s")
        update_values.append(scholarship)

    if not update_fields:
        messagebox.showerror('错误', '没有任何要更新的信息')
        return False

    update_query = f"UPDATE Student SET {', '.join(update_fields)} WHERE sno = %s"
    update_values.append(sno)

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(update_query, update_values)
            if cursor.rowcount == 0:
                messagebox.showinfo("信息", "没有匹配的记录被更新")
                logger.info(f"No matching records were updated for student sno={sno}")
                release_connection(conn)
                return False
            conn.commit()
            cursor.close()
            release_connection(conn)
            logger.info(f"Successfully updated student info: sno={sno}, fields={update_fields}")
            messagebox.showinfo("成功", "学生信息已更新")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to update student info: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            messagebox.showerror("错误", f"更新学生信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return False
    else:
        messagebox.showerror("错误", "无法连接数据库")
        logger.error("Failed to connect to the database for updating student info")
        return False
    return True


def delete_student_info(sno, sname=None, ssex=None, sage=None, sdept=None, scholarship=None) -> bool:
    """
    从数据库删除学生信息
    :param sno: 学号
    :param sname: 姓名（可选）
    :param ssex: 性别（可选）
    :param sage: 年龄（可选）
    :param sdept: 系别（可选）
    :param scholarship: 奖学金（可选）
    :return: 是否成功
    """
    if not sno:
        messagebox.showerror('错误', '学号不能为空！')
        return False

    delete_conditions = ["sno = %s"]
    delete_values = [sno]

    if sname:
        delete_conditions.append("sname = %s")
        delete_values.append(sname)
    if ssex:
        delete_conditions.append("ssex = %s")
        delete_values.append(ssex)
    if sage:
        delete_conditions.append("sage = %s")
        delete_values.append(sage)
    if sdept:
        delete_conditions.append("sdept = %s")
        delete_values.append(sdept)
    if scholarship:
        delete_conditions.append("scholarship = %s")
        delete_values.append(scholarship)

    delete_query = f"DELETE FROM Student WHERE {' AND '.join(delete_conditions)}"

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(delete_query, delete_values)
            if cursor.rowcount == 0:
                messagebox.showinfo("信息", "没有匹配的记录被删除")
                logger.info(f"No matching records were deleted for student sno={sno}")
                release_connection(conn)
                return False
            conn.commit()
            cursor.close()
            release_connection(conn)
            logger.info(f"Successfully deleted student info: sno={sno}, sname={sname}, ssex={ssex}, sage={sage}, sdept={sdept}, scholarship={scholarship}")
            messagebox.showinfo("成功", "学生信息已删除")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to delete student info: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            messagebox.showerror("错误", f"删除学生信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return False
    else:
        messagebox.showerror("错误", "无法连接数据库")
        logger.error("Failed to connect to the database for deleting student info")
        return False
    return True


def query_student_info(sno) -> list[tuple[any, ...]]:
    """
    根据学号查询学生详细信息，包括基本信息和选课信息
    :param sno: 学号
    :return: 查询结果
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                    SELECT
                        s.sno, s.sname, s.ssex, s.sage, s.sdept, g.cno, c.cname, g.grade
                    FROM
                        Student s
                    LEFT JOIN
                        sc g ON s.sno = g.sno
                    LEFT JOIN
                        Course c ON g.cno = c.cno
                    WHERE
                        s.sno = %s
                """, (sno,))
            results = cursor.fetchall()
            cursor.close()
            release_connection(conn)
            logger.info(f"Successfully queried student info for sno={sno}")
            return results
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to query student info: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return [('ERROR', f"查询学生信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")]
    else:
        logger.error("Failed to connect to the database for querying student info")
        return [('ERROR', "无法连接数据库")]
