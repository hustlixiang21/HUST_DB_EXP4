import re
from tkinter import messagebox
from connection_pool import *
from main import logger


def check_params(sno, cno, grade) -> bool:
    """
    检查grade表各参数的取值范围，但只是初步判断，比如主键，外键冲突这类错误要交给数据库判断
    :param sno: 学号
    :param cno: 课程号
    :param grade: 成绩
    :return: 是否有效
    """

    if not sno and not cno and not grade:
        messagebox.showwarning("输入错误", "请输入成绩信息")
        return False

    if sno and not re.fullmatch(r'\d{9}', sno):
        messagebox.showwarning("输入错误", "学号应为9位数字")
        return False

    if cno and not re.fullmatch(r'\d+', cno):
        messagebox.showwarning("输入错误", "课程号应为数字")
        return False

    if grade:
        try:
            grade = int(grade)
            if grade < 0 or grade > 100:
                messagebox.showwarning("输入错误", "成绩应在0到100之间")
                return False
        except ValueError:
            messagebox.showwarning("输入错误", "成绩必须是数字")
            return False

    return True


def insert_grade_info(sno, cno, grade) -> bool:
    """
    插入成绩信息到数据库
    :param sno: 学号
    :param cno: 课程号
    :param grade: 成绩
    :return: 是否成功
    """
    if not sno or not cno:
        messagebox.showerror('错误', '学号和课程号不能为空！')
        return False
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sc (sno, cno, grade) 
                VALUES (%s, %s, %s)
            """, (sno if sno else None, cno if cno else None, grade if grade else None))
            conn.commit()
            cursor.close()
            release_connection(conn)
            logger.info(f"Successfully inserted grade info: sno={sno}, cno={cno}, grade={grade}")
            messagebox.showinfo("成功", "成绩信息已插入")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to insert grade info: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            messagebox.showerror("错误", f"插入成绩信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return False
    else:
        messagebox.showerror("错误", "无法连接数据库")
        logger.error("Failed to connect to the database for inserting grade info")
        return False
    return True


def update_grade_info(sno, cno, grade) -> bool:
    """
    更新成绩信息到数据库
    :param sno: 学号
    :param cno: 课程号
    :param grade: 成绩
    :return: 是否成功
    """
    if not sno or not cno:
        messagebox.showerror('错误', '学号和课程号不能为空！')
        return False

    update_fields = []
    update_values = []

    if grade:
        update_fields.append("grade = %s")
        update_values.append(grade)

    if not update_fields:
        messagebox.showerror('错误', '没有任何要更新的信息')
        return False

    update_query = f"UPDATE sc SET {', '.join(update_fields)} WHERE sno = %s AND cno = %s"
    update_values.extend([sno, cno])

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(update_query, update_values)
            if cursor.rowcount == 0:
                messagebox.showinfo("信息", "没有匹配的记录被更新")
                logger.info(f"No matching records were updated for grade info: sno={sno}, cno={cno}")
                release_connection(conn)
                return False
            conn.commit()
            cursor.close()
            release_connection(conn)
            logger.info(f"Successfully updated grade info: sno={sno}, cno={cno}, grade={grade}")
            messagebox.showinfo("成功", "成绩信息已更新")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to update grade info: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            messagebox.showerror("错误", f"更新成绩信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return False
    else:
        messagebox.showerror("错误", "无法连接数据库")
        logger.error("Failed to connect to the database for updating grade info")
        return False
    return True


def delete_grade_info(sno, cno, grade=None) -> bool:
    """
    从数据库删除成绩信息
    :param sno: 学号
    :param cno: 课程号
    :param grade: 成绩（可选）
    :return: 是否成功
    """
    if not sno or not cno:
        messagebox.showerror('错误', '学号和课程号不能为空！')
        return False

    delete_conditions = ["sno = %s", "cno = %s"]
    delete_values = [sno, cno]

    if grade:
        delete_conditions.append("grade = %s")
        delete_values.append(grade)

    delete_query = f"DELETE FROM sc WHERE {' AND '.join(delete_conditions)}"

    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(delete_query, delete_values)
            if cursor.rowcount == 0:
                messagebox.showinfo("信息", "没有匹配的记录被删除")
                logger.info(f"No matching records were deleted for grade info: sno={sno}, cno={cno}")
                release_connection(conn)
                return False
            conn.commit()
            cursor.close()
            release_connection(conn)
            logger.info(f"Successfully deleted grade info: sno={sno}, cno={cno}, grade={grade}")
            messagebox.showinfo("成功", "成绩信息已删除")
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to delete grade info: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            messagebox.showerror("错误", f"删除成绩信息时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return False
    else:
        messagebox.showerror("错误", "无法连接数据库")
        logger.error("Failed to connect to the database for deleting grade info")
        return False
    return True


def get_grade_info_group_by_sdept() -> list[tuple[any, ...]]:
    """
    按系统计学生平均成绩、最好成绩、最差成绩、优秀率、不及格人数
    :return: 查询结果
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                                SELECT
                                    s.sdept,
                                    AVG(g.grade) AS average_grade,
                                    MAX(g.grade) AS best_grade,
                                    MIN(g.grade) AS worst_grade,
                                    ROUND(SUM(CASE WHEN g.grade >= 85 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS excellent_rate,
                                    SUM(CASE WHEN g.grade < 60 THEN 1 ELSE 0 END) AS fail_count
                                FROM
                                    Student s
                                JOIN
                                    sc g ON s.sno = g.sno
                                GROUP BY
                                    s.sdept
                            """)
            results = cursor.fetchall()
            cursor.close()
            release_connection(conn)
            logger.info("Successfully retrieved grade statistics grouped by department")
            return results
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to retrieve grade statistics: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return [('ERROR', f"按系统计学生成绩时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")]
    else:
        logger.error("Failed to connect to the database for retrieving grade statistics")
        return [('ERROR', "无法连接数据库")]


def get_ranking_info_group_by_sdept() -> list[tuple[any, ...]]:
    """
    按系对学生成绩进行排名，同时显示出学生、课程和成绩信息
    :return: 查询结果或错误信息
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT
                    s.sdept,
                    s.sno,
                    s.sname,
                    g.cno,
                    c.cname,
                    g.grade
                FROM
                    Student s
                JOIN
                    sc g ON s.sno = g.sno
                JOIN
                    Course c ON g.cno = c.cno
                ORDER BY
                    s.sdept, g.grade DESC
            """)
            results = cursor.fetchall()
            cursor.close()
            release_connection(conn)
            logger.info("Successfully retrieved student ranking grouped by department")
            return results
        except Exception as e:
            logger.error(f"Failed to retrieve student ranking: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")
            release_connection(conn)
            return [('ERROR', f"按系对学生成绩排名时出错: {e.pgerror if hasattr(e, 'pgerror') else str(e)}")]
    else:
        logger.error("Failed to connect to the database for retrieving student ranking")
        return [('ERROR', "无法连接数据库")]
