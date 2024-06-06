import re
from tkinter import messagebox
from connection_pool import *
from main import logger


def check_params(cno, cname, cpno, ccredit) -> bool:
    """
    检查course表各参数的取值范围，但只是初步判断，比如主键，外键冲突这类错误要交给数据库判断
    :param cno: 课程号
    :param cname: 课程名
    :param cpno: 先修课
    :param ccredit: 学分
    :return: 是否有效
    """

    if not cno and not cname and not cpno and not ccredit:
        messagebox.showwarning("输入错误", "请输入课程信息")
        return False

    if cno and not re.fullmatch(r'\d+', cno):
        messagebox.showwarning("输入错误", "课程号应为数字")
        return False

    if cpno and not re.fullmatch(r'\d+', cpno):
        messagebox.showwarning("输入错误", "先修课程号应为数字")
        return False

    if ccredit:
        try:
            ccredit = int(ccredit)
            if ccredit <= 0 or ccredit > 10:
                messagebox.showwarning("输入错误", "学分应大于0且小于等于10")
                return False
        except ValueError:
            messagebox.showwarning("输入错误", "学分必须是数字")
            return False

    return True


def insert_course_info(cno, cname, cpno, ccredit) -> bool:
    """
    插入课程信息到数据库
    :param cno: 课程号
    :param cname: 课程名
    :param cpno: 先修课
    :param ccredit: 学分
    :return: 是否成功
    """
    if not cno or not cname:
        messagebox.showerror('错误', '课程号和课程名不能为空！')
        return False
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Course (cno, cname, cpno, ccredit) 
                VALUES (%s, %s, %s, %s)
            """, (cno if cno else None, cname if cname else None, cpno if cpno else None, ccredit if ccredit else None))
            conn.commit()
            cursor.close()
            release_connection(conn)
            logger.info(f"Successfully inserted course info: cno={cno}, cname={cname}, cpno={cpno}, ccredit={ccredit}")
            messagebox.showinfo("成功", "课程信息已插入")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to insert course info: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            messagebox.showerror("错误", f"插入课程信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return False
    else:
        messagebox.showerror("错误", "无法连接数据库")
        logger.error("Failed to connect to the database for inserting course info")
        return False
    return True


def update_course_info(cno, cname, cpno, ccredit) -> bool:
    """
    更新课程信息到数据库
    :param cno: 课程号
    :param cname: 课程名
    :param cpno: 先修课
    :param ccredit: 学分
    :return: 是否成功
    """
    if not cno:
        messagebox.showerror('错误', '课程号不能为空！')
        return False

    update_fields = []
    update_values = []

    if cname:
        update_fields.append("cname = %s")
        update_values.append(cname)
    if cpno:
        update_fields.append("cpno = %s")
        update_values.append(cpno)
    if ccredit:
        update_fields.append("ccredit = %s")
        update_values.append(ccredit)

    if not update_fields:
        messagebox.showerror('错误', '没有任何要更新的信息')
        return False

    update_query = f"UPDATE Course SET {', '.join(update_fields)} WHERE cno = %s"
    update_values.append(cno)

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(update_query, update_values)
            if cursor.rowcount == 0:
                messagebox.showinfo("信息", "没有匹配的记录被更新")
                logger.info(f"No matching records were updated for course cno={cno}")
                release_connection(conn)
                return False
            conn.commit()
            cursor.close()
            release_connection(conn)
            logger.info(f"Successfully updated course info: cno={cno}, fields={update_fields}")
            messagebox.showinfo("成功", "课程信息已更新")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to update course info: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            messagebox.showerror("错误", f"更新课程信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return False
    else:
        messagebox.showerror("错误", "无法连接数据库")
        logger.error("Failed to connect to the database for updating course info")
        return False
    return True


def delete_course_info(cno, cname=None, cpno=None, ccredit=None) -> bool:
    """
    从数据库删除课程信息
    :param cno: 课程号
    :param cname: 课程名（可选）
    :param cpno: 先修课（可选）
    :param ccredit: 学分（可选）
    :return: 是否成功
    """
    if not cno:
        messagebox.showerror('错误', '课程号不能为空！')
        return False

    delete_conditions = ["cno = %s"]
    delete_values = [cno]

    if cname:
        delete_conditions.append("cname = %s")
        delete_values.append(cname)
    if cpno:
        delete_conditions.append("cpno = %s")
        delete_values.append(cpno)
    if ccredit:
        delete_conditions.append("ccredit = %s")
        delete_values.append(ccredit)

    delete_query = f"DELETE FROM Course WHERE {' AND '.join(delete_conditions)}"

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(delete_query, delete_values)
            if cursor.rowcount == 0:
                messagebox.showinfo("信息", "没有匹配的记录被删除")
                logger.info(f"No matching records were deleted for course cno={cno}")
                release_connection(conn)
                return False
            conn.commit()
            cursor.close()
            release_connection(conn)
            logger.info(f"Successfully deleted course info: cno={cno}, cname={cname}, cpno={cpno}, ccredit={ccredit}")
            messagebox.showinfo("成功", "课程信息已删除")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to delete course info: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            messagebox.showerror("错误", f"删除课程信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return False
    else:
        messagebox.showerror("错误", "无法连接数据库")
        logger.error("Failed to connect to the database for deleting course info")
        return False
    return True


def delete_courses_without_enrollments() -> bool:
    """
    删除没有学生选课的课程信息
    :return: 是否成功
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM Course
                WHERE cno NOT IN (
                    SELECT DISTINCT cno FROM sc
                )
            """)
            if cursor.rowcount == 0:
                messagebox.showinfo("信息", "没有符合条件的课程被删除")
                logger.info("No courses without enrollments were deleted")
                release_connection(conn)
                return False
            conn.commit()
            cursor.close()
            release_connection(conn)
            logger.info("Successfully deleted courses without enrollments")
            messagebox.showinfo("成功", "没有学生选课的课程信息已删除")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to delete courses without enrollments: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            messagebox.showerror("错误", f"删除课程信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return False
    else:
        messagebox.showerror("错误", "无法连接数据库")
        logger.error("Failed to connect to the database for deleting courses without enrollments")
        return False
    return True
