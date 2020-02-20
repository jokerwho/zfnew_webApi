# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import time
import requests
import json
from urllib import parse


class GetInfo(object):
    def __init__(self, base_url, cookies):
        self.base_url = base_url
        self.headers = {
            'Referer': base_url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        self.cookies = cookies
        with open('config.json',mode='r',encoding='utf-8') as f:
            config = json.loads(f.read())
        self.proxies = {
            'http':config["proxy"]
        }

    def get_pinfo(self):
        """获取个人信息"""
        url = parse.urljoin(self.base_url, '/xsxxxggl/xsxxwh_cxCkDgxsxx.html?gnmkdm=N100801')
        res = requests.get(url, headers=self.headers, cookies=self.cookies, proxies=self.proxies)
        jres = res.json()
        #print(jres)
        res_dict = {
            'name': jres['xm'],
            'studentId': jres['xh'],
            'birthDay': jres['csrq'],
            'idNumber': jres['zjhm'],
            'candidateNumber': jres['ksh'],
            'status': jres['xjztdm'],
            'collegeName': jres['zsjg_id'],
            'majorName': jres['zyh_id'] if jres.get('zszyh_id')== None else jres.get('zszyh_id'),
            'className': jres['bh_id'],
            'entryDate': jres['rxrq'],
            'graduationSchool': jres['byzx'],
            'domicile': jres['jg'],
            'phoneNumber':'无' if jres.get('sjhm')== None else jres.get('sjhm'),
            'parentsNumber':'无' if jres.get('gddh')== None else jres.get('gddh'),
            'email':'无' if jres.get('dzyx')== None else jres.get('dzyx'),
            'politicalStatus': jres['zzmmm'],
            'national': jres['mzm'],
            'education': jres['pyccdm'],
            'postalCode': jres['yzbm'],
            'grade': int(jres['xh'][0:2])
        }
        return res_dict
    def term_cn(self,xh,year,term):
        nj = int(xh[0:2])
        xnm = int(year[2:4])
        xqm = int(term)
        global grade
        if xnm == nj:
            if xqm == 1:
                grade = '大一上'
            elif xqm == 2:
                grade = '大一下'
        elif xnm == nj+1:
            if xqm == 1:
                grade = '大二上'
            elif xqm == 2:
                grade = '大二下'
        elif xnm == nj+2:
            if xqm == 1:
                grade = '大三上'
            elif xqm == 2:
                grade = '大三下'
        elif xnm == nj+3:
            if xqm == 1:
                grade = '大四上'
            elif xqm == 2:
                grade = '大四下'
        return grade

    def get_study(self,xh):
        """获取学业情况"""
        sessions = requests.Session()

        url_main = parse.urljoin(self.base_url,'/xsxy/xsxyqk_cxXsxyqkIndex.html?gnmkdm=N105515&layout=default')
        url_info = parse.urljoin(self.base_url,'/xsxy/xsxyqk_cxJxzxjhxfyqKcxx.html?gnmkdm=N105515')

        mainr = sessions.get(url_main,headers=self.headers, cookies=self.cookies, proxies=self.proxies)
        mainr.encoding = mainr.apparent_encoding
        soup = BeautifulSoup(mainr.text, 'html.parser')

        allc_str = []
        for allc in soup.find_all('font',size = re.compile('2px')):
            allc_str.append(allc.get_text())
        gpa = float(allc_str[2])
        allc_num = re.findall(r"\d+",allc_str[3])
        allc_num2 = re.findall(r"\d+",allc_str[5])
        allc_num.append(allc_num2[0])
        ipa = int(allc_num[0])
        ipp = int(allc_num[1])
        ipf = int(allc_num[2])
        ipn = int(allc_num[3])
        ipi = int(allc_num[4])
        allc_num3 = re.findall(r"\d+",allc_str[6])
        allc_num4 = re.findall(r"\d+",allc_str[7])
        opp = int(allc_num3[0])
        opf = int(allc_num4[0])

        id_find = re.findall(r"xfyqjd_id='(.*)' jdkcsx='1' leaf=''",str(soup))
        idList = list({}.fromkeys(id_find).keys())
        if xh[0:2] != '19': #本校特色，19级因更改了培养方案导致id非体系
            match = '20' + xh[0:6]
            for i in idList:
                if re.findall(r"tsjy",i):
                    tsid = i[0:14]
                elif re.findall(r"tzjy",i):
                    tzid = i[0:14]
                elif re.findall(r"zyjy",i):
                    zyid = i[0:14]
                elif re.findall(r"qtkcxfyq",i):
                    qtid = i
        else:
            tsid = idList[0]
            tzid = idList[2]
            zyid = idList[1]
            qtid = idList[3]

        res_ts = sessions.post(url_info, headers=self.headers, data={'xfyqjd_id': tsid}, cookies=self.cookies, proxies=self.proxies)
        res_tz = sessions.post(url_info, headers=self.headers, data={'xfyqjd_id': tzid}, cookies=self.cookies, proxies=self.proxies)
        res_zy = sessions.post(url_info, headers=self.headers, data={'xfyqjd_id': zyid}, cookies=self.cookies, proxies=self.proxies)
        res_qt = sessions.post(url_info, headers=self.headers, data={'xfyqjd_id': qtid}, cookies=self.cookies, proxies=self.proxies)

        ts_point_find = re.findall(r"通识教育&nbsp;要求学分:(\d+\.\d+)&nbsp;获得学分:(\d+\.\d+)&nbsp;&nbsp;未获得学分:(\d+\.\d+)&nbsp",str(soup))
        ts_point_list = list(list({}.fromkeys(ts_point_find).keys())[0])    #先得到元组再拆开转换成列表
        ts_point = {
            'tsr':ts_point_list[0],
            'tsg':ts_point_list[1],
            'tsn':ts_point_list[2]
        }
        tz_point_find = re.findall(r"拓展教育&nbsp;要求学分:(\d+\.\d+)&nbsp;获得学分:(\d+\.\d+)&nbsp;&nbsp;未获得学分:(\d+\.\d+)&nbsp",str(soup))
        tz_point_list = list(list({}.fromkeys(tz_point_find).keys())[0])
        tz_point = {
            'tzr':tz_point_list[0],
            'tzg':tz_point_list[1],
            'tzn':tz_point_list[2]
        }
        zy_point_find = re.findall(r"专业教育&nbsp;要求学分:(\d+\.\d+)&nbsp;获得学分:(\d+\.\d+)&nbsp;&nbsp;未获得学分:(\d+\.\d+)&nbsp",str(soup))
        zy_point_list = list(list({}.fromkeys(zy_point_find).keys())[0])
        zy_point = {
            'zyr':zy_point_list[0],
            'zyg':zy_point_list[1],
            'zyn':zy_point_list[2]
        }
        
        res_main = {
            'gpa':gpa,  #平均学分绩点GPA
            'ipa':ipa,  #计划内总课程数
            'ipp':ipp,  #计划内已过课程数
            'ipf':ipf,  #计划内未过课程数
            'ipn':ipn,  #计划内未修课程数
            'ipi':ipi,  #计划内在读课程数
            'opp':opp,  #计划外已过课程数
            'opf':opf,  #计划外未过课程数
            'tsData':{
                'tsPoint':ts_point, #通识教育学分情况
                'tsItems':[{
                    'courseTitle':j["KCMC"],
                    'courseId':j["KCH"],
                    'courseSituation':j["XDZT"],
                    'courseTerm':self.term_cn(xh,j["JYXDXNM"],j["JYXDXQMC"]),
                    'courseCategory': ' ' if j.get('KCLBMC') == None else j.get('KCLBMC'),
                    'courseAttribution': ' ' if j.get('KCXZMC') == None else j.get('KCXZMC'),
                    'maxGrade':' ' if j.get('MAXCJ') == None else j["MAXCJ"],
                    'credit':' ' if j.get('XF') == None else float(j["XF"]),
                    'gradePoint':' ' if j.get('JD') == None else float(j["JD"]),
                }for j in res_ts.json()], #通识教育修读情况
                },
            'tzdata':{
                'tzPoint':tz_point, #拓展教育学分情况
                'tzItems':[{
                    'courseTitle':k["KCMC"],
                    'courseId':k["KCH"],
                    'courseSituation':k["XDZT"],
                    'courseTerm':self.term_cn(xh,k["JYXDXNM"],k["JYXDXQMC"]),
                    'courseCategory': ' ' if k.get('KCLBMC') == None else k.get('KCLBMC'),
                    'courseAttribution': ' ' if k.get('KCXZMC') == None else k.get('KCXZMC'),
                    'maxGrade':' ' if k.get('MAXCJ') == None else k["MAXCJ"],
                    'credit':' ' if k.get('XF') == None else float(k["XF"]),
                    'gradePoint':' ' if k.get('JD') == None else float(k["JD"]),
                }for k in res_tz.json()], #拓展教育修读情况
                },
            'zydata':{
                'zyPoint':zy_point, #专业教育学分情况
                'zyItems':[{
                    'courseTitle':l["KCMC"],
                    'courseId':l["KCH"],
                    'courseSituation':l["XDZT"],
                    'courseTerm':self.term_cn(xh,l["JYXDXNM"],l["JYXDXQMC"]),
                    'courseCategory': ' ' if l.get('KCLBMC') == None else l.get('KCLBMC'),
                    'courseAttribution': ' ' if l.get('KCXZMC') == None else l.get('KCXZMC'),
                    'maxGrade':' ' if l.get('MAXCJ') == None else l["MAXCJ"],
                    'credit':' ' if l.get('XF') == None else float(l["XF"]),
                    'gradePoint':' ' if l.get('JD') == None else float(l["JD"]),
                }for l in res_zy.json()], #专业教育修读情况
                },
            'qtdata':{
                'qtPoint':'{}', #其它课程学分情况
                'qtItems':[{
                    'courseTitle':m["KCMC"],
                    'courseId':m["KCH"],
                    'courseSituation':m["XDZT"],
                    'courseTerm':self.term_cn(xh,m["XNM"],m["XQMMC"]),
                    'courseCategory': ' ' if m.get('KCLBMC') == None else m.get('KCLBMC'),
                    'courseAttribution': ' ' if m.get('KCXZMC') == None else m.get('KCXZMC'),
                    'maxGrade':' ' if m.get('MAXCJ') == None else m["MAXCJ"],
                    'credit':' ' if m.get('XF') == None else float(m["XF"]),
                    'gradePoint':' ' if m.get('JD') == None else float(m["JD"]),
                }for m in res_qt.json()], #其它课程修读情况
                },
        }

        return res_main

            

    #def get_notice(self):
    #   """获取通知"""
    #    url_0 = parse.urljoin(self.base_url, '/xtgl/index_cxNews.html?localeKey=zh_CN&gnmkdm=index')
    #    url_1 = parse.urljoin(self.base_url, 'xtgl/index_cxAreaTwo.html?localeKey=zh_CN&gnmkdm=index')
    #    res_list = []
    #    url_list = []

    #    res_0 = requests.get(url_0, headers=self.headers, cookies=self.cookies)
    #    res_1 = requests.get(url_1, headers=self.headers, cookies=self.cookies)
    #    soup_0 = BeautifulSoup(res_0.text, 'lxml')
    #    soup_1 = BeautifulSoup(res_1.text, 'lxml')
    #    url_list += [i['href'] for i in soup_0.select('a[href^="/xtgl/"]')]
    #    url_list += [i['href'] for i in soup_1.select('a[href^="/xtgl/"]')]

    #    for u in url_list:
    #        _res = requests.get(self.base_url + u, headers=self.headers, cookies=self.cookies)
    #        _soup = BeautifulSoup(_res.text, 'lxml')
    #        title = _soup.find(attrs={'class': 'text-center'}).string
    #        info = [i.string for i in _soup.select_one('[class="text-center news_title1"]').find_all('span')]
    #        publisher = re.search(r'：(.*)', info[0]).group(1)
    #        ctime = re.search(r'：(.*)', info[1]).group(1)
    #        vnum = re.search(r'：(.*)', info[2]).group(1)
    #        detailed = _soup.find(attrs={'class': 'news_con'})
    #        content = ''.join(list(detailed.strings))
    #        doc_urls = [self.base_url + i['href'][2:] for i in detailed.select('a[href^=".."]')]
    #        res_list.append({
    #            'title': title,
    #            'publisher': publisher,
    #            'ctime': ctime,
    #            'vnum': vnum,
    #            'content': content,
    #            'doc_urls': doc_urls
    #        })
    #    return res_list

    def get_message(self):
        """获取消息"""
        url = parse.urljoin(self.base_url, '/xtgl/index_cxDbsy.html?doType=query')
        data = {
            'sfyy': '0',  # 是否已阅，未阅未1，已阅为2
            'flag': '1',
            '_search': 'false',
            'nd': int(time.time()*1000),
            'queryModel.showCount': '1000',  # 最多条数
            'queryModel.currentPage': '1',  # 当前页数
            'queryModel.sortName': 'cjsj',
            'queryModel.sortOrder': 'desc',  # 时间倒序, asc正序
            'time': '0'
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies, proxies=self.proxies)
        jres = res.json()
        res_list = [{'message': i['xxnr'], 'ctime': i['cjsj']} for i in jres['items']]
        return res_list

    # def get_elective_list(self):
    #     """获取选课名单信息"""
    #     pass
    #
    # def get_expriment_grade(self):
    #     """获取实验成绩信息"""
    #     pass

    def get_grade(self, year, term):
        """获取成绩"""
        url = parse.urljoin(self.base_url, '/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        elif term == '0':
            term = ''
        else:
            print('Please enter the correct term value！！！ ("0" or "1" or "2")')
            return {}
        data = {
            'xnm': year,  # 学年数
            'xqm': term,  # 学期数，第一学期为3，第二学期为12, 整个学年为空''
            '_search': 'false',
            'nd': int(time.time()*1000),
            'queryModel.showCount': '100',  # 每页最多条数
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '0'  # 查询次数
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies, proxies=self.proxies)
        jres = res.json()
        if jres.get('items'):  # 防止数据出错items为空
            res_dict = {
                'name': jres['items'][0]['xm'],
                'studentId': jres['items'][0]['xh'],
                'schoolYear': jres['items'][0]['xnm'],
                'schoolTerm': jres['items'][0]['xqmmc'],
                'course': [{
                    'courseTitle': i['kcmc'],
                    'teacher': i['jsxm'],
                    'courseId': i['kch_id'],
                    'className': '无'if i.get('jxbmc')== None else i.get('jxbmc'),
                    'courseNature': '无'if i.get('kcxzmc')== None else i.get('kcxzmc'),
                    'credit': i['xf'],
                    'grade': i['cj'],
                    'gradePoint': '无' if i.get('jd') == None else i.get('jd'),
                    'gradeNature': i['ksxz'],
                    'startCollege': '无' if i.get('kkbmmc') == None else i.get('kkbmmc'),
                    'courseMark': i['kcbj'],
                    'courseCategory': '无' if i.get('kclbmc') == None else i.get('kclbmc'),
                    'courseAttribution': '无' if i.get('kcgsmc') == None else i.get('kcgsmc')
                } for i in jres['items']]}
            return res_dict
        else:
            return {}

    def get_schedule(self, year, term):
        """获取课程表信息"""
        url = parse.urljoin(self.base_url, '/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151')
        if term == '1':  # 修改检测学期
            term = '3'
        elif term == '2':
            term = '12'
        else:
            print('Please enter the correct term value！！！ ("1" or "2")')
            return {}
        data = {
            'xnm': year,
            'xqm': term
        }
        res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies, proxies=self.proxies)
        jres = res.json()
        res_dict = {
            'name': jres['xsxx']['XM'],
            'studentId': jres['xsxx']['XH'],
            'schoolYear': jres['xsxx']['XNM'],
            'schoolTerm': jres['xsxx']['XQMMC'],
            'normalCourse': [{
                'courseTitle': i['kcmc'],
                'courseTitleShort':i['kcmc'][0:12] + '..' if len(i['kcmc']) > 12 else i['kcmc'],
                'teacher': '无' if i.get('xm')== None else i.get('xm'),
                'courseId': i['kch_id'],
                'courseWeekday':i['xqj'],
                'courseSection': i['jc'],
                'courseWeek': i['zcd'],
                'exam':i['khfsmc'],
                'campus': i['xqmc'],
                'courseRoom': i['cdmc'],
                'className': i['jxbmc'],
                'hoursComposition': i['kcxszc'],
                'weeklyHours': i['zhxs'],
                'totalHours': i['zxs'],
                'credit': i['xf']
            } for i in jres['kbList']],
            #'otherCourses': [i['qtkcgs'] for i in jres['sjkList']]
            }
        return res_dict

    # def get_classroom(self):
    #     """获取空教室信息"""
    #     url = parse.urljoin(self.base_url, '/cdjy/cdjy_cxKxcdlb.html?gnmkdm=N2155&layout=default')
    #     data = {
    #         'fwzt': 'cx',
    #         'xqh_id': '1',
    #         'xnm': '2019',
    #         'xqm': '3',
    #         'cdlb_id': '',
    #         'cdejlb_id': '',
    #         'qszws': '',
    #         'jszws': '',
    #         'cdmc': '',
    #         'lh': '',
    #         'qssd': '',
    #         'jssd': '',
    #         'qssj': '',
    #         'jssj': '',
    #         'jyfs': '0',
    #         'cdjylx': '',
    #         'zcd': '256',
    #         'xqj': '3',
    #         'jcd': '9',
    #         '_search': 'false',
    #         'nd': '1571744696313',
    #         'queryModel.showCount': '50',  # 最多条数
    #         'queryModel.currentPage': '1',
    #         'queryModel.sortName': 'cdbh',
    #         'queryModel.sortOrder': 'asc',
    #         'time': '1'
    #     }
    #     res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
    #     return res

    #def get_exam(self, year, term):
    #    """获取考试信息"""
    #    url = parse.urljoin(self.base_url, '/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N358105')
    #    if term == '1':  # 修改检测学期
    #        term = '3'
    #    elif term == '2':
    #        term = '12'
    #    else:
    #        print('Please enter the correct term value！！！ ("1" or "2")')
    #        return {}
    #    data = {
    #        'xnm': year,  # 学年数
    #        'xqm': term,  # 学期数，第一学期为3，第二学期为12
    #        '_search': 'false',
    #        'nd': int(time.time() * 1000),
    #        'queryModel.showCount': '100',  # 每页最多条数
    #        'queryModel.currentPage': '1',
    #        'queryModel.sortName': '',
    #        'queryModel.sortOrder': 'asc',
    #        'time': '0'  # 查询次数
    #    }
    #    res = requests.post(url, headers=self.headers, data=data, cookies=self.cookies)
    #    jres = res.json()
    #    if jres.get('items'):  # 防止数据出错items为空
    #        res_dict = {
    #            'name': jres['items'][0]['xm'],
    #            'studentId': jres['items'][0]['xh'],
    #            'schoolYear': jres['items'][0]['xnmc'][:4],
    #            'schoolTerm': jres['items'][0]['xqmmc'],
    #            'exams': [{
    #                'courseTitle': i['kcmc'],
    #                'teacher': i['jsxx'],
    #                'courseId': i['kch'],
    #                'reworkMark': i['cxbj'],
    #                'selfeditingMark': i['zxbj'],
    #                'examName': i['ksmc'],
    #                'paperId': i['sjbh'],
    #                'examTime': i['kssj'],
    #                'eaxmLocation': i['cdmc'],
    #                'campus': i['xqmc'],
    #                'examSeatNumber': i['zwh']
    #            } for i in jres['items']]}
    #        return res_dict
    #    else:
    #        return {}
