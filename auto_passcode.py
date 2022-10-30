import requests
import json
import datetime
import time
import re
from log import logger



class autoPassCode(object):
    def __init__(self, studentsInfo_path: str) -> None:
        self.headers = {
            'Host':             'mryb.zjut.edu.cn',
            'Content-Type' : 'application/json;charset=UTF-8',
            'Accept':	'*/*',
            'Connection':	'keep-alive',
            'User-Agent':       "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            'Referer':          'http://mryb.zjut.edu.cn'
        }

        self.studentsInfo_path = studentsInfo_path
        
        with open(self.studentsInfo_path, 'r') as f:
            studentsInfo = json.load(f)
            for _, studentInfo in studentsInfo.items():
                # 获取审批人Id
                studentInfo['auditId'] = self.get_audit_info(studentInfo['id'], studentInfo['auditName'])
                # 检测是否需要补打卡
                date_list = self.get_missing_clock(studentInfo['id'])
                # 补打卡
                name = studentInfo['name']
                if len(date_list) > 0:
                    if studentInfo['auditId'] == 'notFound':
                        auditName = studentInfo['auditName']
                        logger.info(f'用户[{name}]需要补打卡, 但是没有找到审批人[{auditName}]的id, 补打卡失败')
                        continue
                    elif studentInfo['auditId'] == 'error':
                        continue
                    else:
                        self.auto_appeal(studentsInfo['name'], studentsInfo['id'], studentsInfo['auditId'], date_list)
                else:
                    logger.info(f'用户[{name}]不需要补打卡, 非常good')

            
    # 获取没打卡的日期
    def get_missing_clock(self, studentId):
        url = 'http://mryb.zjut.edu.cn/htk/baseInfo/getQRCode'
        payload = {
            'mobile': studentId
        }
        try:
            resp = requests.get(url=url, headers=self.headers, params=payload)
            resp_json = json.loads(resp.text)
            match_list = re.findall(r'未打卡日期', resp_json['message'])
            # 有未打卡
            if resp_json['success'] and len(match_list) != 0:
                date_list = re.findall(r'\d+-\d+-\d+', resp_json['message'])
                return date_list
            else:
                return [ ]
        except Exception as e:
            for _, studentInfo in self.studentsInfo.item():
                if studentInfo['id'] == studentId:
                    name = studentInfo['name']
                    logger.error(f'获取用户[{name}]的状态信息出错, error: {e}')
                    return  [ ]
            return [ ]
    # 是否已经打卡: 返回的messages为 '已完成新冠疫苗接种' 即为已打卡
    def is_already_clock(self, studentId):
        url = 'http://mryb.zjut.edu.cn/htk/baseInfo/getQRCode'
        payload = {
            'mobile': studentId
        }
        try:
            resp = requests.get(url=url, headers=self.headers, params=payload)
            resp_json = json.loads(resp.text)
            match_list = re.findall(r'已完成新冠疫苗接种', resp_json['message'])
            # 已打卡
            if resp_json['success'] and len(match_list) != 0:
                return True
            else:
                return False
        except Exception as e:
            for _, studentInfo in self.studentsInfo.item():
                if studentInfo['id'] == studentId:
                    name = studentInfo['name']
                    logger.error(f'获取用户[{name}]的状态信息出错, error: {e}')
                    return  False
            return False
    # 自动补卡
    def auto_appeal(self, name: str, studentId: str, auditId: str, date_list: list):
        """ 用户补打卡

        Args:
            name (str): 姓名
            studentId (str): 学号
            auditId (str): 审批人的id
            date_list (list): 补打卡日期列表
        Example:
            >>> self.auto_appeal('2112103400', '06190', ['2022-10-12', '2022-10-11', '2022-10-10'])
            
        """
        url = 'http://mryb.zjut.edu.cn/htk/appeal/add'
        data = {
            "auditId": auditId,
            "userId": studentId,
            "data": [],
            "travelCard": "Do not go gentle into that good night ~"
        }
        
        for date in date_list:
            date_info = {
                "createTime": date,
                "currentLocation": "浙江省杭州市西湖区",
                "temperatureOne": "36.0℃",
                "temperatureTwo": "36.0℃",
                "whetherSymptom": "2",
                "symptomDate": None,
                "whetherMeetRisk": "2",
                "meetRiskTime": None,
                "healthCode": "3",
                "agreement": None
            }
            data['data'].push(date_info)
        
        try:
            date_str = date_list.join(',')
            resp_json = requests.post(url=url, headers=self.headers, json=data).json()
            if(resp_json['success']):
                logger.error(f'用户[{name}]补打卡成功, 补打卡日期: {date_str}')
            else:
                message = resp_json['message']
                logger.error(f'用户[{name}]补打卡失败, message: {message}, 补打卡日期: {date_str}')
        except Exception as e:
            logger.error(f'用户[{name}]补打卡报错, error: {e}')
    # 自动打卡
    def auto_clock(self, studentInfo):
        url = 'http://mryb.zjut.edu.cn/htk/baseInfo/save'
        data = {
            "workNo": studentInfo['id'],
            "name": studentInfo['name'],
            "sex": studentInfo['sex'],
            "campus": "2",
            "company": studentInfo['company'],
            "currentLocation": "浙江省杭州市西湖区",
            "whetherLeave": "2",
            "leaveReson": None,
            "leaveReasonInfo": None,
            "whetherInSchool": "1",
            "grade": studentInfo['grade'],
            "mobile": studentInfo['mobile'],
            "emLinkPerson": studentInfo['emLinkPerson'],
            "emLinkMobile": studentInfo['emLinkMobile'],
            "studentType": "2",
            "locationPandemic": "3",
            "meetRiskTime": None,
            "mentalStatus": "1",
            "temperatureOne": "36.0℃",
            "temperatureTwo": "36.0℃",
            "whetherSymptom": "2",
            "whetherMeetRisk": "2",
            "healthCode": "3",
            "whetherVaccine": "1",
            "whetherAllVaccine": "3",
            "agreement": True,
            "type": 1,
            "companyId": "21030"
        }
        try:
            name = studentInfo['name']
            
            if self.is_already_clock(studentInfo['id']):
                logger.info(f'用户[{name}]今日已打卡')
                return True, studentInfo
            
            resp_json = requests.post(url=url, headers=self.headers, json=data).json()
            if(resp_json['success']):
                logger.info(f'用户[{name}]自动打卡成功')
                return True, studentInfo
            else:
                message = resp_json['message']
                logger.warn(f'用户[{name}]自动打卡失败, message: {message}')
                return False, studentInfo
        except Exception as e:
            logger.error(f'用户[{name}]自动打卡报错, error: {e}')
            return False, studentInfo
    # 获取审批人Id
    def get_audit_info(self, studentId: str, auditName: str):
        url = 'http://mryb.zjut.edu.cn/htk/appeal/audit/person'
        payload = {
            'userId': studentId
        }
        
        try:
            resp = requests.get(url=url, headers=self.headers, params=payload)
            resp_json = json.loads(resp.text)
            for auditInfo in resp_json['result']:
                if auditInfo['name'] == auditName:
                    return auditInfo['userId']
            print(resp_json['result'])
            return 'notFound'
        except Exception as e:
            print(e)
            return 'error'

    def wait_for_time(self, clock_time: int, time_sleep: float=60*60):
        while True:
            timeHour = datetime.datetime.now().hour
            if timeHour == clock_time:
                break
            else:
                time.sleep(time_sleep)
                
    def auto(self):
        try:
            # 时间在 01:00:00 ~ 01:59:59 会进行打卡
            self.wait_for_time(1)
            with open(self.studentsInfo_path, 'r') as f:
                studentsInfo = json.load(f)
                while True:
                    need_clock_List = [ studentInfo for _, studentInfo in studentsInfo.items() ] # 需要打卡的学生列表
                    sleep_after_clockAll = 23 # 打卡完毕之后的休眠时间 初始值23小时
                    while len(need_clock_List) != 0: # 打卡失败的情况（maybe网络炸了
                        # 一小时内打完所有人的卡
                        for _, studentInfo in studentsInfo.items():
                            # 自动打卡
                            success, stuInfo = self.auto_clock(studentInfo)
                            if success:
                                need_clock_List.remove(stuInfo)
                            time.sleep(60*60/len(studentsInfo))
                        # 如果有人打卡失败, 则间隔4个小时再试
                        sleep_after_clockAll -= 4
                        if sleep_after_clockAll <= 0:
                            for stu in need_clock_List:
                                name = stu['name']
                                logger.info(f'用户{name}今日打卡失败')
                            break
                        time.sleep(4*60*60)
                    
                    logger.info('-----------打卡完毕----------')
                    logger.info(' ')
                    # 休眠
                    time.sleep(sleep_after_clockAll*60*60)
                    
        except KeyboardInterrupt:
            logger.info('--------END--------')


logger.info('--------START--------')

x = autoPassCode('./studentsInfo.json')
x.auto()