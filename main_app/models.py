from django.db import models
import pymysql
import re
import datetime

# 校验输入的是否是手机号


def phone(n):
    if len(n) != 11:
        return 0
    if re.match(r'1[3,4,5,7,8]\d{9}', n):
        print("您输入的的手机号码是：\n", n)
    # 中国联通：
    # 130，131，132，155，156，185，186，145，176
    if re.match(r'13[0,1,2]\d{8}', n) or \
            re.match(r"15[5,6]\d{8}", n) or \
            re.match(r"18[5,6]", n) or \
            re.match(r"145\d{8}", n) or \
            re.match(r"176\d{8}", n):
        return 1
    # 中国移动
    # 134, 135 , 136, 137, 138, 139, 147, 150, 151,
    # 152, 157, 158, 159, 178, 182, 183, 184, 187, 188；
    elif re.match(r"13[4,5,6,7,8,9]\d{8}", n) or \
            re.match(r"147\d{8}|178\d{8}", n) or \
            re.match(r"15[0,1,2,7,8,9]\d{8}", n) or \
            re.match(r"18[2,3,4,7,8]\d{8}", n):
        return 1
    else:
        return 0


# 连接模块
def mysql_connect():
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root',
                           password='', database='govdata1',
                           port=3306, charset='utf8')
    return conn

# 按给定的两个条件查询数据库


def accumulate_two_information(use_need_information):
    # 初始化游标
    conn = mysql_connect()
    cursor = conn.cursor()
    # 此处必须加一个list，因为filter转化后要以list展示，否则报错error<filter object at 0x02C18A70>
    str_process = list(filter(None, use_need_information.split(",")))
    select = "SELECT * FROM govdata1 where {} = '{}' and {} = '{}'".format(
        str_process[0], str_process[1], str_process[2], str_process[3])
    exe_select = cursor.execute(select)
    return exe_select

# 查询指定时间内不同类型的街道事件


def find_time_with_street_events(use_need_information):
    # 初始化游标
    conn = mysql_connect()
    cursor = conn.cursor()
    # 此处必须加一个list，因为filter转化后要以list展示，否则报错error<filter object at 0x02C18A70>
    str_process = list(filter(None, use_need_information.split(",")))
    select = "SELECT * FROM govdata1 where {} = '{}' and {} = '{}' and CREATE_TIME between '{}' and '{}'".format(str_process[0], str_process[1],
                                                                                                                 str_process[2], str_process[3], str_process[4], str_process[5])
    exe_select = cursor.execute(select)
    return exe_select

# 处理事件类型,进行预处理,逐行读取数据，之后生成列表


def precess_matters(file):
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    matters = []
    for line in lines:
        tmp_line1 = line.split('|')
        tmp_line2 = ''.join(tmp_line1[1])
        tmp_line2 = re.sub('\s+', '', tmp_line2).strip()
        matters.append(''.join(tmp_line2))
    return matters

# 用于民生饼状图


def find_time_with_minsheng(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    select = "SELECT * FROM govdata1 where {} = '{}'  and CREATE_TIME between '{}' and '{}'".format(
        str_process[0], str_process[1],
        str_process[2], str_process[3])
    exe_select = cursor.execute(select)
    # 这里返回的是一个整数
    return exe_select

# 这个可以直接查询热点社区


def hot_street(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    select = "SELECT * FROM govdata1 where COMMUNITY_NAME like '{}'  and CREATE_TIME between '{}' and '{}'".format(
        str_process[0], str_process[1],
        str_process[2])
    exe_select = cursor.execute(select)
    # 这里返回的是一个整数
    return exe_select

# 查询处置中（未结办）事件的数量


def intime_to_archive_num(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    start_time = str_process[0]
    end_time = str_process[1]
    # if start_time[0:9] < '2018-10-30':
    #     return 0
    select = "SELECT * FROM govdata1 where INTIME_TO_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
        start_time, end_time)
    exe_select = cursor.execute(select)
    # 这里返回的是一个整数
    return exe_select

# 查询超期结办事件的数量


def overtime_archive_num(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    select = "SELECT * FROM govdata1 where OVERTIME_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
        str_process[0], str_process[1])
    exe_select = cursor.execute(select)
    # 这里返回的是一个整数
    return exe_select

# 查询按期结办事件的数量


def intime_archive_num(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    select = "SELECT * FROM govdata1 where INTIME_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
        str_process[0], str_process[1])
    exe_select = cursor.execute(select)
    # 这里返回的是一个整数
    return exe_select

# 按季度查询处置中（未结办）事件的数量


def intime_to_archive_num_quarter(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    year = str_process[1]
    # 利用选择进行季度的数据选择
    if str_process[0] == '1':
        start_time = year + '-01-01'
        end_time = year + '-03-31'
        select = "SELECT * FROM govdata1 where INTIME_TO_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select
    elif str_process[0] == '2':
        start_time = year + '-04-01'
        end_time = year + '-06-30'
        select = "SELECT * FROM govdata1 where INTIME_TO_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select
    elif str_process[0] == '3':
        start_time = year + '-07-01'
        end_time = year + '-09-30'
        select = "SELECT * FROM govdata1 where INTIME_TO_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select
    elif str_process[0] == '4':
        start_time = year + '-10-01'
        end_time = year + '-12-31'
        select = "SELECT * FROM govdata1 where INTIME_TO_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select

# 按季度查询超期结办事件的数量


def overtime_archive_num_quarter(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    year = str_process[1]
    # 利用选择进行季度的数据选择
    if str_process[0] == '1':
        start_time = year + '-01-01'
        end_time = year + '-03-31'
        select = "SELECT * FROM govdata1 where OVERTIME_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select
    elif str_process[0] == '2':
        start_time = year + '-04-01'
        end_time = year + '-06-30'
        select = "SELECT * FROM govdata1 where OVERTIME_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select
    elif str_process[0] == '3':
        start_time = year + '-07-01'
        end_time = year + '-09-30'
        select = "SELECT * FROM govdata1 where OVERTIME_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select
    elif str_process[0] == '4':
        start_time = year + '-10-01'
        end_time = year + '-12-31'
        select = "SELECT * FROM govdata1 where OVERTIME_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select

# 按季度查询按期结办事件的数量


def intime_archive_num_quarter(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    # 第一个是年份，第二个是季度
    year = str_process[1]
    # 利用选择进行季度的数据选择
    if str_process[0] == '1':
        start_time = year + '-01-01'
        end_time = year + '-03-31'
        select = "SELECT * FROM govdata1 where INTIME_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select
    elif str_process[0] == '2':
        start_time = year + '-04-01'
        end_time = year + '-06-30'
        select = "SELECT * FROM govdata1 where INTIME_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select
    elif str_process[0] == '3':
        start_time = year + '-07-01'
        end_time = year + '-09-30'
        select = "SELECT * FROM govdata1 where INTIME_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select
    elif str_process[0] == '4':
        start_time = year + '-10-01'
        end_time = year + '-12-31'
        select = "SELECT * FROM govdata1 where INTIME_ARCHIVE_NUM like '1'  and CREATE_TIME between '{}' and '{}'".format(
            start_time, end_time)
        exe_select = cursor.execute(select)
        # 这里返回的是一个整数
        return exe_select
# 查询各类型事件的数量


def event_type(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    select = "SELECT * FROM govdata1 where EVENT_TYPE_NAME like '{}'  and CREATE_TIME between '{}' and '{}'".format(
        str_process[0], str_process[1],
        str_process[2])
    exe_select = cursor.execute(select)
    # 这里返回的是一个整数
    return exe_select

# 用于给政府工作人员读取用户的反馈信息


def back_info(use_give_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_give_information.split(",")))
    # 这个地方要插入一个游标的函数
    # 这个数据库的标记不对
    query = "insert into infoback values ('{}', '{}', '{}', '{}', '{}', '{}','{}')".format(str_process[0],
                                                                                           str_process[1],
                                                                                           str_process[2],
                                                                                           str_process[3],
                                                                                           str_process[4],
                                                                                           str_process[5],
                                                                                           str_process[6],
                                                                                           )
    cursor.execute(query)
    conn.commit()  # 只要是修改了表内容的操作，后面一定要提交，否则不起作用
    return '反馈成功'

# 当前需要先实现寻找时间范围


def find_back_info(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    # 下面能够提供的查询次序分别是街道，姓名，时间，时间是要有格式要求的
    query = "SELECT * FROM infoback where {} like '{}' and = {} like '{}' and backtime between '{}' and '{}'".format(
        str_process[0], str_process[1],
        str_process[2], str_process[3],
        str_process[4], str_process[5])
    cursor.execute(query)
    Okdata = cursor.fetchall()
    return Okdata

# 用户登录时候的数据库


def login_check(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    # 下面能够提供的查询次序分别是街道，姓名，时间，时间是要有格式要求的
    query = "SELECT * FROM account where tel  = '{}' ".format(str_process[0])
    cursor.execute(query)
    cipher = cursor.fetchall()
    if(len(cipher) == 0):
        return '用户不存在'
    # 这里返回的是用户密码，字符串类型
    else:
        return cipher[0][2:4]

# 新用户注册


def regist_new_user(use_give_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_give_information.split(",")))
    name = str_process[0]
    phonenum = str_process[1]
    password = str_process[2]
    if(phone(phonenum) == 0):
        return 'Phone number is error'
    # 这里传入的三个信息全都应该是字符串格式
    # 通过网页注册的用户，其身份默认为resident
    query = "insert into account (name, tel, cipher, identity) values ('{}', '{}', '{}', 'resident')".format(
        name, phonenum, password)
    cursor.execute(query)
    conn.commit()
    return '注册成功'

# 检查手机号是否被注册过


def check_if_register(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    query = "SELECT * FROM account where tel  = '{}' ".format(str_process[0])
    cursor.execute(query)
    cipher = cursor.fetchall()
    # 这里返回的是用户密码，字符串类型
    if len(cipher) == 0:
        return 1
    else:
        return 0

# 返回所有异常事件（同一天内多次报警事件）


def matter_exceptions():
    conn = mysql_connect()
    cursor = conn.cursor()
    query = "select CREATE_TIME,COMMUNITY_NAME,STREET_NAME,SUB_TYPE_NAME,COUNT(STREET_NAME) As Account,COUNT(SUB_TYPE_NAME) As Account2 from govdata1 gdb group by CREATE_TIME,EVENT_TYPE_NAME,COMMUNITY_NAME,STREET_NAME,SUB_TYPE_NAME HAVING Account>2 ORDER BY CREATE_TIME DESC "
    cursor.execute(query)
    exceptions = cursor.fetchall()
    exc_matters = []
    for i in range(len(exceptions)):
        exc_matters.append([])
        for j in range(len(exceptions[i])):
            if j == 0:
                exc_time = exceptions[i][j].strftime("%Y-%m-%d %H:%M:%S")
                exc_matters[i].append(exc_time)
            elif j <= 4:
                exc_matters[i].append(exceptions[i][j])
    # 这里返回的是list套list
    # print(exc_matters[0])
    return exc_matters

# 返回所有超期未结办事件


def not_done_matters():
    conn = mysql_connect()
    cursor = conn.cursor()
    # 下面能够提供的查询次序分别是街道，姓名，时间，时间是要有格式要求的
    query = "SELECT * FROM govdata1 where OVERTIME_ARCHIVE_NUM  = 1 "
    cursor.execute(query)
    undo_matter = cursor.fetchall()
    # print(undo_matter)
    exc_matters = []
    for i in range(len(undo_matter)):
        exc_matters.append([])
        for j in range(len(undo_matter[i])):
            if j == 17:
                exc_time = undo_matter[i][j].strftime("%Y-%m-%d %H:%M:%S")
                exc_matters[i].append(exc_time)
            elif j == 16 or j == 2 or j == 5 or j == 20 or j == 23 or j == 24:
                exc_matters[i].append(undo_matter[i][j])
    # 这里返回的是list套list
    return exc_matters

# 账户信息,字典形式返回


def account_info(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    # 下面能够提供的查询次序分别是街道，姓名，时间，时间是要有格式要求的
    query = "SELECT * FROM account where tel  = {} ".format(str_process[0])
    cursor.execute(query)
    user_account_info = cursor.fetchall()
    # 这里返回的是用户密码，字符串类型
    dict_user_info = {}
    for i in range(len(user_account_info)):
        dict_user_info['name'] = user_account_info[i][0]
        dict_user_info['tel'] = user_account_info[i][1]
        dict_user_info['identity'] = user_account_info[i][3]
    return dict_user_info

# 管理员添加数据


def feedback_information(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split("*")))
    # 这个地方要插入一个游标的函数
    # 这个数据库的标记不对
    query = (
        'insert into infoback(name,tel,backtime,content,street,community,matter_type) values(%s, %s,%s, %s, %s, %s, %s)')
    cursor.execute(query, (str_process[0], str_process[1],
                           str_process[2], str_process[3],
                           str_process[4], str_process[5],
                           str_process[6]))
    conn.commit()  # 只要是修改了表内容的操作，后面一定要提交，否则不起作用
    cursor.close()
    conn.close()

# 更改数据


def change_data(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(
        " ")))  # 此处必须加一个list，因为filter转化后要以list展示，否则报错error<filter object at 0x02C18A70>
    user_input1 = str_process[0]
    user_input2 = str_process[1]
    # 这个地方要插入一个游标的函数
    # 这个数据库的标记不对
    query = 'update govdata1 set name = %s where id = %s'
    cursor.execute(query, (user_input1, user_input2))
    conn.commit()  # 只要是修改了表内容的操作，后面一定要提交，否则不起作用
    cursor.close()
    conn.close()

# 查询数据/统计数据


def accumulate_information(use_need_information):
    # 初始化游标
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(
        " ")))  # 此处必须加一个list，因为filter转化后要以list展示，否则报错error<filter object at 0x02C18A70>
    # user_input1 = str_process[0]
    # user_input2 = str_process[1]
    select = (
        "SELECT * FROM govdata1 where \
         {} = '{}' and {} = '{}' and {} = '{}' and {} = '{}' and \
         {} = '{}' and {} = '{}' and {} = '{}' and {} = '{}' and \
         {} = '{}' and {} = '{}' and {} = '{}' and {} = '{}' and \
         {} = '{}' and {} = '{}' and {} = '{}' and {} = '{}' and \
         {} = '{}' and {} = '{}' and {} = '{}' and {} = '{}' and \
         {} = '{}' and {} = '{}' and {} = '{}' and {} = '{}' and \
         {} = '{}' and {} = '{}' ").format(
        'COUNT', str_process[0],
        'REPORT_NUM', str_process[1],
        'EVENT_PROPERTY_NAME', str_process[2],
        'EVENT_TYPE_ID', str_process[3],
        'EVENT_TYPE_NAME', str_process[4],
        'EVENT_SRC_NAME', str_process[5],
        'DISTRICT_ID', str_process[6],
        'INTIME_ARCHIVE_NUM', str_process[7],
        'SUB_TYPE_ID', str_process[8],
        'DISTRICT_NAME', str_process[9],
        'COMMUNITY_ID', str_process[10],
        'REC_ID', str_process[11],
        'STREET_ID', str_process[12],
        'OVERTIME_ARCHIVE_NUM', str_process[13],
        'OPERATE_NUM', str_process[14],
        'DISPOSE_UNIT_ID', str_process[15],
        'STREET_NAME', str_process[16],
        'CREATE_TIME', str_process[17],
        'EVENT_SRC_ID', str_process[18],
        'INTIME_TO_ARCHIVE_NUM', str_process[19],
        'SUB_TYPE_NAME', str_process[20],
        'EVENT_PROPERTY_ID', str_process[21],
        'OCCUR_PLACE', str_process[22],
        'COMMUNITY_NAME', str_process[23],
        'DISPOSE_UNIT_NAME', str_process[24],
        'MAIN_TYPE_NAME', str_process[25],
        'MAIN_TYPE_ID', str_process[26])

    # select = "SELECT * FROM govdata1 where {} = '{}' ".format(user_input1, user_input2)
    exe_select = cursor.execute(select)
    if exe_select == 0:
        print('抱歉,您提供的信息可能有误,数据结果为0')
    else:
        print(exe_select)
    conn.commit()  # 只要是修改了表内容的操作，后面一定要提交，否则不起作用
    cursor.close()
    conn.close()


def accumulate_one_information(use_need_information):
    # 初始化游标
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(
        " ")))  # 此处必须加一个list，因为filter转化后要以list展示，否则报错error<filter object at 0x02C18A70>
    # print(str_process)
    select = "SELECT * FROM govdata1 where {} = '{}' ".format(
        str_process[0], str_process[1])
    exe_select = cursor.execute(select)
    return exe_select

# 政府工作人员查看所有的反馈信息数据


def scan_all_data_in_infoback_database():
    # 初始化游标
    conn = mysql_connect()
    cursor = conn.cursor()
    select = "SELECT * FROM govdata1.infoback"
    exe_select = cursor.execute(select)
    user_account_info = cursor.fetchall()
    return_user_account_info = []
    for i in range(len(user_account_info)):
        return_user_account_info.append({})
        for j in range(len(user_account_info[i])):
            if j == 2:
                return_user_account_info[i]['time'] = user_account_info[i][j].strftime(
                    "%Y-%m-%d %H:%M:%S")
            elif j == 0:
                return_user_account_info[i]['name'] = user_account_info[i][j]
            elif j == 1:
                return_user_account_info[i]['tel'] = user_account_info[i][j]
            elif j == 3:
                return_user_account_info[i]['content'] = user_account_info[i][j]
            elif j == 4:
                return_user_account_info[i]['street'] = user_account_info[i][j]
            elif j == 5:
                return_user_account_info[i]['community'] = user_account_info[i][j]
            elif j == 6:
                return_user_account_info[i]['property'] = user_account_info[i][j]
    # 这里返回的是list套list
    # print(exc_matters[0])
    return return_user_account_info

# 添加数据


def government_insert_information(use_need_information):
    # 社区和街道都是id映射到名字
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split("*")))
    query = "select * from govdata1 order by count DESC limit 1;"
    cursor.execute(query)
    final_record = cursor.fetchall()[0][0]  # 提取到的是count值
    count_insert_now = final_record + 1
    # EVENT_PROPERTY_NAME，EVENT_TYPE_NAME, EVENT_SRC_NAME，INTIME_ARCHIVE_NUM
    # EVENT_TYPE_NAME:字典一，时间类别名称与id对应
    EVENT_TYPE_ID = {
        '食药市监': '9',
        '规土城建': '4',
        '统一战线': '16',
        '组织人事': '12',
        '社区管理': '17',
        '环保水务': '3',
        '治安维稳': '2',
        '民政服务': '15',
        '文体旅游': '10',
        '教育卫生': '11',
        '市政设施': '6',
        '市容环卫': '5',
        '安全隐患': '1',
        '劳动社保': '8',
        '党纪政纪': '14',
        '党建群团': '13',
        '交通运输': '7',
        '专业事件采集': '695'}
    # SUB_TYPE_NAME：小类名称====================================================================================
    f = open('D:\\MyProject\\gov_3.1\\static\\dict_use.txt',
             'r', encoding='utf-8')
    lines = f.readlines()
    SUB_TYPE_ID = {}
    count = 0
    for line in lines:
        tmp_line = line.split('\t')
        SUB_TYPE_ID[tmp_line[0]] = tmp_line[1].split('\n')[0]
    f.close()
    # COMMUNITY_ID：社区id=======================================================================================
    f = open('D:\\MyProject\\gov_3.1\\static\\community_id.txt',
             'r', encoding='utf-8')
    lines = f.readlines()
    COMMUNITY_ID = {}
    count = 0
    for line in lines:
        tmp_line = line.split('\t')
        COMMUNITY_ID[tmp_line[1].split('\n')[0]] = tmp_line[0]
    f.close()
    # STREET_NAME:街道名===========================================================================================
    f = open('D:\\MyProject\\gov_3.1\\static\\street_name.txt',
             'r', encoding='utf-8')
    lines = f.readlines()
    STREET_ID = {}
    count = 0
    for line in lines:
        tmp_line = line.split('\t')
        STREET_ID[tmp_line[1].split('\n')[0]] = tmp_line[0]
    f.close()
    # DISPOSE_UNIT_ID:处置部门标识============================================================================================================
    f = open('D:\\MyProject\\gov_3.1\\static\\dispose_id.txt',
             'r', encoding='utf-8')
    lines = f.readlines()
    DISPOSE_UNIT_ID = {}
    count = 0
    for line in lines:
        tmp_line = line.split('\t')
        DISPOSE_UNIT_ID[tmp_line[0]] = tmp_line[1].split('\n')[0]
    f.close()
    # MAIN_TYPE_ID:主类名称============================================================================================================
    f = open('D:\\MyProject\\gov_3.1\\static\\main_type_id.txt',
             'r', encoding='utf-8')
    lines = f.readlines()
    MAIN_TYPE_ID = {}
    count = 0
    for line in lines:
        tmp_line = line.split('\t')
        MAIN_TYPE_ID[tmp_line[0]] = tmp_line[1].split('\n')[0]
    f.close()
    # ========================================================================
    # EVENT_PROPERTY_ID:投诉之类的名称============================================================================================================
    f = open('D:\\MyProject\\gov_3.1\\static\\event_property_id.txt',
             'r', encoding='utf-8')
    lines = f.readlines()
    EVENT_PROPERTY_ID = {}
    count = 0
    for line in lines:
        tmp_line = line.split('\t')
        EVENT_PROPERTY_ID[tmp_line[0]] = tmp_line[1].split('\n')[0]
    f.close()
    # ========================================================================
    query = (
        'insert into govdata1(COUNT,REPORT_NUM,EVENT_PROPERTY_NAME,EVENT_TYPE_ID,EVENT_TYPE_NAME,EVENT_SRC_NAME,DISTRICT_ID,INTIME_ARCHIVE_NUM,SUB_TYPE_ID,DISTRICT_NAME,COMMUNITY_ID,REC_ID,STREET_ID,OVERTIME_ARCHIVE_NUM,OPERATE_NUM,DISPOSE_UNIT_ID,STREET_NAME,CREATE_TIME,EVENT_SRC_ID,INTIME_TO_ARCHIVE_NUM,SUB_TYPE_NAME,EVENT_PROPERTY_ID,OCCUR_PLACE,COMMUNITY_NAME,DISPOSE_UNIT_NAME,MAIN_TYPE_NAME,MAIN_TYPE_ID) values(%s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s, %s,%s, %s, %s,%s, %s,%s, %s, %s, %s, %s)')
    cursor.execute(query, (count_insert_now,
                           1,  # REPORT_NAME
                           str_process[0],  # EVENT_PROPERTY_NAME,是投诉还是咨询之列的：
                           EVENT_TYPE_ID[str_process[1]],  # EVENT_TYPE_ID
                           str_process[1],  # EVENT_TYPE_NAME
                           '坪山区政府大数据综合服务平台',  # EVENT_SRC_NAME
                           1,  # DISTREECT
                           0,  # INTIME_ARCHIVE_NUM
                           # 小类id：绑字典2,SUB_TYPE_ID
                           SUB_TYPE_ID[str_process[4]],
                           '坪山区',
                           str_process[5],  # 社区id:绑字典3,
                           count_insert_now + 300000,  # REC主键
                           str_process[2],  # 街道id:绑字典5,
                           0,  # 超期结伴,
                           1,  # 受理,因为输入即受理,OPEATE_NUM
                           DISPOSE_UNIT_ID[str_process[6]],  # 处置部门标识：绑字典,
                           STREET_ID[str_process[2]],  # 街道名
                           str_process[3],  # 创建时间：
                           999,  # 这个是我们自己定义的输入的id编号
                           1,  # 处置中
                           str_process[4],  # SUB_TYPE_NAME
                           EVENT_PROPERTY_ID[str_process[0]],
                           '-',  # 发生地点
                           COMMUNITY_ID[str_process[5]],  # 社区名
                           str_process[6],  # 处理单位名
                           str_process[7],  # MAIN_TYPE_NAME
                           MAIN_TYPE_ID[str_process[7]]
                           ))
    conn.commit()  # 只要是修改了表内容的操作，后面一定要提交，否则不起作用
    cursor.close()
    conn.close()

# 每当政府工作人员处理完一条居民反馈数据，在临时数据库中将其删除


def delete_has_been_used_info_in_infoback_database(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split("*")))
    # 下面能够提供的查询次序分别是街道，姓名，时间，时间是要有格式要求的
    query = "delete from  infoback where tel = '{}' and backtime = '{}' ".format(
        str_process[0], str_process[1],)
    cursor.execute(query)
    conn.commit()  # 只要是修改了表内容的操作，后面一定要提交，否则不起作用
    cursor.close()
    conn.close()

# 查看给定手机号的账户数据


def scan_all_data_in_account_database(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split(",")))
    # 下面能够提供的查询次序分别是街道，姓名，时间，时间是要有格式要求的
    query = "SELECT * FROM account where tel  = {} ".format(str_process[0])
    cursor.execute(query)
    user_account_info = cursor.fetchall()
    # 这里返回的是用户密码，字符串类型
    dict_user_info = {}
    for i in range(len(user_account_info)):
        dict_user_info['name'] = user_account_info[i][0]
        dict_user_info['tel'] = user_account_info[i][1]
        dict_user_info['identity'] = user_account_info[i][3]
        dict_user_info['sex'] = user_account_info[i][4]
        dict_user_info['email'] = user_account_info[i][5]
        dict_user_info['address'] = user_account_info[i][6]
        dict_user_info['description'] = user_account_info[i][7]
    return dict_user_info

# 修改账户信息
# 除密码和身份之外别的都得改


def account_information_change(use_need_information):
    conn = mysql_connect()
    cursor = conn.cursor()
    str_process = list(filter(None, use_need_information.split("*")))

    # 下面能够提供的查询次序分别是街道，姓名，时间，时间是要有格式要求的
    query = "update account set name = '{}' , tel = {}, sex = '{}', email = '{}', address = '{}', description = '{}' where tel  = {} ".format(
        str_process[0], str_process[1],
        str_process[2], str_process[3],
        str_process[4], str_process[5],
        str_process[6])
    cursor.execute(query)
    conn.commit()  # 只要是修改了表内容的操作，后面一定要提交，否则不起作用
    cursor.close()
    conn.close()


# # 查询事件结办信息
# def exec_type(use_need_information):
#     conn = mysql_connect()
#     cursor = conn.cursor()
#     str_process = list(filter(None, use_need_information.split(",")))
#     select = "SELECT * FROM govdata1 where '{}' like '1'  and CREATE_TIME between '{}' and '{}'".format(
#         str_process[0], str_process[1],
#         str_process[2])
#     exe_select = cursor.execute(select)
#     # 这里返回的是一个整数
#     return exe_select
