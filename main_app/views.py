import logging
import requests
from django.contrib import messages
from django.shortcuts import render,redirect
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import os
from main_app.models import *
import json
from django import forms
from django.views.decorators.csrf import csrf_exempt
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

i = 0 # 用于异常报警的全局变量
j = 0 # 用于滚动显示的全局变量
flag_guest = 1 # 标志当前是否以游客身份访问系统
cnt_login = 0 # 记录登录次数(否则只要一次登录失败，之后进入登录页面就会报错)
cnt_register = 0 # 记录注册次数
flag_login = [1]*100 # 用于标记第i次(1<=i<=100)登录时的账户、密码是否匹配：1-匹配,0-不匹配
flag_register = [1]*100 # 用于标记注册时手机号码是否已被注册过(是否合法)：1-未注册过（合法）,0-已注册过（不合法）

# 主页
def index(request):
    global flag_guest
    if flag_guest == 1 or request.session['is_login'] == False:
        request.session['is_login'] == False
        flag_guest = flag_guest-1
        return render(request,"index.html")
    else:
        return render(request,"index.html")
        
# 登录
def login(request):
    global flag_login,cnt_login
    cnt_login = cnt_login+1
    return render(request, 'login.html',{'flag':flag_login[cnt_login-1]})

# 处理登录表单
@csrf_exempt
def form_login(request):
    global flag_login
    # 待定
    # if request.session.get('is_login',None):
    #     return redirect('../index/')
    if request.method == "POST":
        form_data = request.POST.dict()
        para_dict = form_data
        # 将手机号传给数据库,从数据库返回该手机号对应的密码
        temp = login_check(para_dict['tel'])
        # 若该手机号对应的用户不存在，则数据库返回错误提示信息，并重定向至登录页面   
        if(temp == "用户不存在"):
            flag_login[cnt_login] = 0 # 将登录标志位置0
            return redirect("../login/")
        # 若输入的手机号存在对应用户，则获取该用户的密码和身份信息
        password = temp[0]
        identity = temp[1]
        #如果账号密码匹配，即登陆成功，则根据用户的身份进行url重定向
        if (para_dict['password'] == password): 
            request.session['is_login'] = True
            #request.session['user_id'] = para_dict['tel'] # 暂定以电话号码确定身份（即登录状态显示电话号码）
            account_data = scan_all_data_in_account_database(para_dict['tel'])
            request.session['user_id'] = account_data['name'] 
            request.session['user_tel'] = account_data['tel']
            flag_login[cnt_login] = 1
            if (identity == 'gov'):  # 若用户是政府工作人员，则重定向至/realtime
                request.session['is_gov'] = True # 设置session中的用户身份项
                return redirect("../realtime/")
            elif (identity == 'resident'):  # 若用户是居民，则重定向至主页/index
                request.session['is_gov'] = False
                return redirect("../index/")
            else: # 若用户是管理员，则重定向至？？
                pass
        else: # 否则，重定向至登录页面
            flag_login[cnt_login] = 0
            return redirect("../login/")
        #     # message = "密码错误！"
            
    else:
        return HttpResponse("No POST request recieved!!")

# 注册
def register(request):
    global flag_register,cnt_register
    cnt_register = cnt_register+1
    return render(request, 'register.html',{'flag':flag_register[cnt_register-1]})

# 处理注册表单
@csrf_exempt
def form_register(request):
    global flag_register
    if request.method == "POST":
        form_data = request.POST.dict()
        para_dict = form_data
        # if(isValid_phonenum(para_dict['tel']) and isValid_password(para_dict['password'])):
        if(check_if_register(para_dict['tel'])==1):
            flag_register[cnt_register] = 1
            msg = regist_new_user(para_dict['name']+','+para_dict['tel']+','+para_dict['password'])
            if(msg=='Phone number is error'):
                flag_register[cnt_register] = 2
                return redirect("../register/")
            else:
                return redirect("../index/")
        else:
            flag_register[cnt_register] = 0
            return redirect("../register/")
    else:
        return HttpResponse("No POST request recieved!!")

# 反馈
def contact(request):
    return render(request,'contact.html')

# 处理反馈表单
@csrf_exempt
def form_contact(request):
    #request.session['is_login'] = True
    if request.method == "POST":
        form_data = request.POST.dict()
        # 获取反馈提交的时间（通过将系统时间给以一定偏移实现）
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=393)
        n_days = (now - delta).strftime('%Y-%m-%d %H:%M:%S')
        para_str = form_data['name'] + ',' + form_data['tel'] + ',' + n_days + ',' + form_data['message'] + ','+ form_data['street'] + ',' + form_data['community'] + ',' + form_data['property']
        # para_str = form_data['name'] + ',' + form_data['tel'] + ',' + '2019-09-01 18:00:00' + ',' + form_data['message'] + ','+ form_data['street'] + ',' + form_data['community'] + ',' + form_data['problem']
        # 将表单信息交给数据库处理（插入数据）
        back_info(para_str)
        # 反馈成功，2s后自动跳转至主页
        return render(request,"wait2sec.html")
    else:
        return HttpResponse("No POST request recieved!!")

# 展示realtime主页
def realtime(request):
    if request.session['is_login'] and request.session['is_gov']:
        return render(request, 'realtime.html')
    else :
        return redirect('../livelihood_analysis/')

# 展示“各街道民生事件情况”（小类名称+事件数目）条形图
def street_events(request):
    # 这个为将可视化网页塞入这个框架之中
    data = ['市容环卫', '环保水务', '市政设施', '规土城建', '教育卫生',
            '安全隐患', '组织人事', '党纪政纪', '劳动社保', '社区管理',
            '交通运输', '治安维稳', '专业事件采集', '统一战线',
            '民政服务', '文体旅游', '食药市监', '党建群团']
    street = ['龙田街道', '坪山街道', '碧岭街道', '坑梓街道', '马峦街道', '石井街道', '-']
    # 查询数据，按照类别进行单条查询
    main_column = 'EVENT_TYPE_NAME'
    second_column = 'STREET_NAME'
    qdata = []
    if request.method == 'POST':
        request.encoding = 'utf-8'
        # 用户选择的时间格式为‘年-月-日’（即查看指定时间范围内的数据）
        if request.POST['mode'] == '1':
            time1 = request.POST['startDate'] + " 00:00:00"
            time2 = request.POST['endDate'] + " 23:59:59"
            for i in range(len(data)):
                qdata.append([])
                for j in range(len(street)):
                    qdata[i].append(find_time_with_street_events(main_column + ',' + data[i] + ',' + second_column + ',' + street[j] + ',' + time1 + ',' + time2))
            return render(request, 'street_events.html', {'street_lst': street,'smalltypename_lst': data,'data_lst': qdata,
            'startDate':request.POST['startDate'],'endDate':request.POST['endDate'],'datemode':'1'})
        # 用户选择的时间格式为‘年-月’（即查看指定月份的数据）
        elif request.POST['mode'] == '2':
            year_month = request.POST['startDate'] # 获取‘年-月’
            time1 = year_month + '-01 ' + '00:00:00'
            # 按照指定的月份确定查询数据库的结束时间time2
            if year_month.split('-')[1] in ['01','03','05','07','08','10','12']:
                time2 = year_month + '-31' + " 23:59:59"
            elif year_month.split('-')[1] in ['04','06','09','11']:
                time2 = year_month + '-30' + " 23:59:59"
            else:
                time2 = year_month + '-28' + " 23:59:59"
            for i in range(len(data)):
                qdata.append([])
                for j in range(len(street)):
                    qdata[i].append(find_time_with_street_events(main_column + ',' + data[i] + ',' + second_column + ',' + street[j] + ',' + time1 + ',' + time2))
            return render(request, 'street_events.html', {'street_lst': street,'smalltypename_lst': data,'data_lst': qdata,
            'startDate':request.POST['startDate'],'endDate':'','datemode':'2'})                   
    else:
        time1 = "2018-10-30 00:00:00"
        time2 = "2018-10-30 23:59:59"        
        for i in range(len(data)):
            qdata.append([])
            for j in range(len(street)):
                qdata[i].append(find_time_with_street_events(main_column + ',' + data[i] + ',' + second_column + ',' + street[j] + ',' + time1 + ',' + time2))
        return render(request, 'street_events.html', {'street_lst': street,'smalltypename_lst': data,'data_lst': qdata,
        'startDate':"2018-10-30",'endDate':"2018-10-30",'datemode':'1'})

# 展示“民生分析”（问题性质）饼状图
def livelihood_analysis(request):
    # 这个为将可视化网页塞入这个框架之中
    data = ['投诉', '咨询', '建议',
            '感谢', '求决', '-', '其他']
    main_column = 'EVENT_PROPERTY_NAME'
    qdata = []
    if request.method == 'POST':
        request.encoding = 'utf-8'
        # 即查看指定时间范围内的数据
        time1 = request.POST['startDate'] + " 00:00:00"
        time2 = request.POST['endDate'] + " 23:59:59"
        for i in range(len(data)):
            qdata.append(find_time_with_minsheng(main_column + ',' + data[i] + ',' + time1 + ',' + time2))
        return render(request, 'livelihood_analysis.html', {'typename_lst': data,'data_lst': qdata,
        'startDate':request.POST['startDate'],'endDate':request.POST['endDate']})

    else:  # 默认展示今日（2018-10-30）的事件
        time1 = "2018-10-30 00:00:00"
        time2 = "2018-10-30 23:59:59"   
        for i in range(len(data)):
            qdata.append(find_time_with_minsheng(main_column + ',' + data[i] + ',' + time1 + ',' + time2))
        return render(request, 'livelihood_analysis.html', {'typename_lst': data,'data_lst': qdata,
        'startDate':"2018-10-30",'endDate':"2018-10-30",'datemode':'1'})

# 展示“热点社区分析”图表
def hot_community(request):
    community = ['龙田社区', '金龟社区', '金沙社区', '马峦社区','老坑社区',  '竹坑社区', '秀新社区', 
    '碧岭社区', '石井社区', '田心社区', '田头社区', '沙田社区', '沙湖社区', '沙坣社区', '汤坑社区', 
    '江岭社区', '坪环社区', '坪山社区', '坑梓社区', '和平社区', '南布社区', '六联社区', '六和社区']
    qdata = []
    if request.method == 'POST':
        request.encoding = 'utf-8'
        # 用户选择的时间格式为‘年-月-日’（即查看指定时间范围内的数据）
        if request.POST['mode'] == '1':
            time1 = request.POST['startDate'] + " 00:00:00"
            time2 = request.POST['endDate'] + " 23:59:59"
            for i in range(len(community)):
                qdata.append(hot_street(community[i] + ',' + time1 + ',' + time2))
            return render(request,"hot_community.html",{'street_lst': community,'data_lst': qdata,
            'startDate':request.POST['startDate'],'endDate':request.POST['endDate'],'datemode':'1'})
        # 用户选择的时间格式为‘年-月’（即查看指定月份的数据）
        elif request.POST['mode'] == '2':
            year_month = request.POST['startDate'] # 获取‘年-月’
            time1 = year_month + '-01 ' + '00:00:00'
            # 按照指定的月份确定查询数据库的结束时间time2
            if year_month.split('-')[1] in ['01','03','05','07','08','10','12']:
                time2 = year_month + '-31' + " 23:59:59"
            elif year_month.split('-')[1] in ['04','06','09','11']:
                time2 = year_month + '-30' + " 23:59:59"
            else:
                time2 = year_month + '-28' + " 23:59:59"
            for i in range(len(community)):
                qdata.append(hot_street(community[i] + ',' + time1 + ',' + time2))
            return render(request,"hot_community.html",{'street_lst': community,'data_lst': qdata,
            'startDate':request.POST['startDate'], 'endDate':'', 'datemode':'2'})
    else:
        time1 = "2018-10-30 00:00:00"
        time2 = "2018-10-30 23:59:59"  
        for i in range(len(community)):
            qdata.append(hot_street(community[i] + ',' + time1 + ',' + time2))
        return render(request,"hot_community.html",{'street_lst': community,'data_lst': qdata,
        'startDate':"2018-10-30",'endDate':"2018-10-30",'datemode':'1'})

# 展示“事情结办分析”图表（未完成）
def done(request):
    typename = ['专业事件采集','交通运输','党建群团','党纪政纪','劳动社保','安全隐患','市容环卫','市政设施',
    '教育卫生','文体旅游','民政服务','治安维稳','环保水务','社区管理','组织人事','统一战线','规土城建','食药市监']
    execdata = []
    problemdata = []
    if request.method == 'POST':
        request.encoding = 'utf-8'
        # 用户选择的时间格式为‘年-月-日’（即查看指定时间范围内的数据）
        if request.POST['mode'] == '1':
            time1 = request.POST['startDate'] + " 00:00:00"
            time2 = request.POST['endDate'] + " 23:59:59"
            # 查询结办情况
            execdata.append(intime_to_archive_num(time1 + ',' + time2))
            execdata.append(overtime_archive_num(time1 + ',' + time2))
            execdata.append(intime_archive_num(time1 + ',' + time2))
            for i in range(len(typename)): # 查询各类型事件数量
                problemdata.append(event_type(typename[i] + ',' + time1 + ',' + time2))
            return render(request,"done.html",{'typename_lst':typename,'execdata_lst':execdata,'problemdata_lst':problemdata,
            'startDate':request.POST['startDate'],'endDate':request.POST['endDate'], 'datemode':'1'})

        # 用户选择的时间格式为‘年-月’（即查看指定月份的数据）
        elif request.POST['mode'] == '2':
            year_month = request.POST['startDate'] # 获取‘年-月’
            time1 = year_month + '-01 ' + '00:00:00'
            # 按照指定的月份确定查询数据库的结束时间time2
            if year_month.split('-')[1] in ['01','03','05','07','08','10','12']:
                time2 = year_month + '-31' + " 23:59:59"
            elif year_month.split('-')[1] in ['04','06','09','11']:
                time2 = year_month + '-30' + " 23:59:59"
            else:
                time2 = year_month + '-28' + " 23:59:59"
            # 查询结办情况
            execdata.append(intime_to_archive_num(time1 + ',' + time2))
            execdata.append(overtime_archive_num(time1 + ',' + time2))
            execdata.append(intime_archive_num(time1 + ',' + time2))
            for i in range(len(typename)): # 按月份查询各类型事件数量
                problemdata.append(event_type(typename[i] + ',' + time1 + ',' + time2))
            return render(request,"done.html",{'typename_lst':typename,'execdata_lst':execdata,'problemdata_lst':problemdata,
            'startDate':request.POST['startDate'],'endDate':'','datemode':'2'}) # 返回的startDate和endDate可能要修改

        # 用户选择的时间格式为‘年-季度’（即查看指定季度的数据）
        elif request.POST['mode'] == '3':
            year = request.POST['year'] # 获取年份
            quarter = request.POST['season'] # 获取选择的季度('1' / '2' / '3' / '4')
            # 查询结办情况
            execdata.append(intime_to_archive_num_quarter(quarter+','+year))
            execdata.append(overtime_archive_num_quarter(quarter+','+year))
            execdata.append(intime_archive_num_quarter(quarter+','+year))
            for i in range(len(typename)): # 按季度查询各类型事件数量
                if quarter == '1':
                    time1 = year + '-01-01 00:00:00'
                    time2 = year + '-03-31 23:59:59'
                elif quarter == '2':
                    time1 = year + '-04-01 00:00:00'
                    time2 = year + '-06-30 23:59:59'
                elif quarter == '3':
                    time1 = year + '-07-01 00:00:00'
                    time2 = year + '-09-30 23:59:59'
                else :
                    time1 = year + '-10-01 00:00:00'
                    time2 = year + '-12-31 23:59:59'                    
                problemdata.append(event_type(typename[i] + ',' + time1 + ',' + time2))
            return render(request,"done.html",{'typename_lst':typename,'execdata_lst':execdata,'problemdata_lst':problemdata,
            'startDate':year+'-'+quarter,'endDate':'', 'datemode':'3'})  # 返回的startDate和endDate可能要修改 

    else: # 若用户为指定时间范围，则默认显示当天的数据
        time1 = "2018-10-30 00:00:00"
        time2 = "2018-10-30 23:59:59"  
        execdata.append(intime_to_archive_num(time1 + ',' + time2))
        execdata.append(overtime_archive_num(time1 + ',' + time2))
        execdata.append(intime_archive_num(time1 + ',' + time2))
        for i in range(len(typename)): # 查询各类型事件数量
            problemdata.append(event_type(typename[i] + ',' + time1 + ',' + time2))
        return render(request,"done.html",{'typename_lst':typename,'execdata_lst':execdata,'problemdata_lst':problemdata,
        'startDate':"2018-10-30",'endDate':"2018-10-30",'datemode':'1'})

# 在异常事件展示中需要被访问的url（未完成）
def abnormal_events(request):
    global i
    exc_matters = matter_exceptions()
    events = exc_matters[i]
    if request.method == "GET":
        i = i+1
        return HttpResponse('系统检测到 {} 的 {} 的 {} 问题一天内被反馈 {} 次 ，可能存在异常，请及时通知相关人员处理。'.format
        (events[1], events[2], events[3], events[4]))

# 在滚动显示未结办事件中需要被访问的url
def scroll_display(request):
    global j
    not_done_events = not_done_matters()
    events = not_done_events[j]
    para = {'time':events[3],'street':events[2],'community':events[5],'src':events[1],'event':events[4],'property':events[0],'dispose_unit':events[6]}
    if request.method == "GET":
        j = j+1
        return HttpResponse(json.dumps(para))

# 为管理员展示反馈信息页面
def feedback(request):
    if request.session['is_login'] and request.session['is_gov']:
        feedback_info_raw = scan_all_data_in_infoback_database()
        return render(request,"feedback.html",{'data_lst':feedback_info_raw})
    else:
        return redirect('../livelihood_analysis/')

# 将管理员处理后的完整反馈存入数据库
def store_feedback(request):
    if request.method == "POST":
        form_data = request.POST.dict()
        para = form_data['property'] + '*' + form_data['event-type'] + '*' + form_data['street'] + '*' + form_data['time'] + '*' + form_data['sub-type'] + '*' + form_data['community'] + '*' + form_data['dispose-unit'] + '*' + form_data['main-type']
        government_insert_information(para)
        # 将临时数据库中的相应反馈数据删除
        delete_has_been_used_info_in_infoback_database(form_data['tel'] + '*' + form_data['time'])
        return redirect('../feedback/')

# 政府工作人员删除无效反馈
def delete_feedback(request):
    if request.method == "POST":
        form_data = request.POST.dict()
        delete_has_been_used_info_in_infoback_database(form_data['tel'] + '*' + form_data['time'])
        return redirect('../feedback')

# 展示个人信息页面
def profile(request):
    para_dict = scan_all_data_in_account_database(request.session['user_tel'])
    print(para_dict)
    return render(request,"user-profile.html",{'profile_dict': para_dict})

# 修改用户个人信息
def account_info_change(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        # 将用户未填的信息置为' '
        for key,value in form_data.items():
            if value=='':
                form_data[key] = ' '
        para = form_data['name'] + '*' + form_data['tel'] + '*' + form_data['sex'] + '*' + form_data['email'] + '*' + form_data['address'] + '*' + form_data['description'] + '*' + request.session['user_tel']
        print(para)
        account_information_change(para)
        return redirect('../user_profile/')

# 退出登录
def logout(request):
    request.session.flush()
    request.session['is_login'] = False
    return redirect("../index/")  # 退出登录后回到主页

# 定向至主页
def goto_index(request):
    return redirect("../index/")  # 退出登录后回到主页

