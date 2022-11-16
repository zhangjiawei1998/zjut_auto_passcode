from flask import Flask, request, make_response
from log import logger
import json
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)

app.config['JSON_AS_ASCII'] = False

@app.route('/ping', methods=['GET', 'POST'])
def test():
    return 'ping success !!!'

@app.route('/join', methods=['POST'])
def add_stuInfo():
    
    new_stuInfo = request.get_json()
    all_stuInfo = dict()
    with open('../studentsInfo.json', 'r') as f:
        all_stuInfo = json.load(f)
    
    # 判断用户是否存在
    message = ''
    for _, stuInfo in all_stuInfo.items():
        if new_stuInfo['id'] == stuInfo['id']:
            message = '学号已经存在'
            break
        elif new_stuInfo['name'] == stuInfo['name']:
            message = '姓名已经存在'
            break
        elif new_stuInfo['mobile'] == stuInfo['mobile']:
            message = '手机号已经存在'
            break
    # 如果不存在，则新添加一个
    if message == '':
        try:
            with open('../studentsInfo.json', 'w') as f:
                all_stuInfo[new_stuInfo['id']] = new_stuInfo
                json.dump(all_stuInfo, f, indent=4, ensure_ascii=False)
                message='添加成功'
                logger.info('用户[%s]加入打卡名单成功', new_stuInfo['name'])
        except Exception as e:
            logger.error('用户[%s]加入打卡名单时发生错误, err: %s', new_stuInfo['name'], e)
            message='添加失败'
            
    resp = dict(
        success= message == '添加成功',
        message= message,
    )
    return resp

@app.route('/stopClock', methods=['POST'])
def stop_clock():
    try:
        stuId = request.get_json()['id']
        response = { 
            "success": False, 
            "message": "无事发生"
        }
        all_stuInfo = dict()
        with open('../studentsInfo.json', 'r') as f:
            all_stuInfo = json.load(f)
        with open('../studentsInfo.json', 'w') as f:
            if stuId not in all_stuInfo.keys():
                response['success'] = False
                response['message'] = '该学号不存在'
                logger.info(f'修改用户[{stuId}]的自动打卡状态失败，该用户不存在')
            else:
                all_stuInfo[stuId]['needClock'] = not all_stuInfo[stuId]['needClock']
                json.dump(all_stuInfo, f, indent=4, ensure_ascii=False)
                response['success'] = True
                response['message'] = '修改状态成功, 现在的状态：\n正常自动打卡\n' if all_stuInfo[stuId]['needClock'] else '修改状态成功, 现在的状态：\n停止自动打卡\n'
                response['message'] += '提示: 每天凌晨1点-2点之间会进行打卡, 请勿在此时修改状态'
                logger.info('用户[%s]修改状态成功, 当前是否自动打卡: %s', stuId, str(all_stuInfo[stuId]['needClock']))
        return response
    except Exception as e:
        logger.error(f'修改打卡状态时发生错误, error: {e}',)
        return { "success": False, "message": f"修改打卡状态失败, {e}"}

@app.route('/search', methods=['POST'])
def search_stuInfo():
    try:
        stuId = request.get_json()['id']
        response = { 
            "success": False, 
            "message": ""
        }
        with open('../studentsInfo.json', 'r') as f:
            
            all_stuInfo = json.load(f)
            if stuId not in all_stuInfo.keys():
                response['success'] = False
                response['message'] = '该学号不存在'
                logger.info(f'查询用户[{stuId}]的信息失败，该用户不存在')
            else:
                response['success'] = True
                stuInfo = {
                    "学 号: ": all_stuInfo[stuId]['id'],
                    "姓 名: ": all_stuInfo[stuId]['name'],
                    "性 别: ": "男" if all_stuInfo[stuId]['sex'] == "1" else "女",
                    "学 院: ": all_stuInfo[stuId]['company'],
                    "年 级: ": all_stuInfo[stuId]['grade'],
                    "手 机: ": all_stuInfo[stuId]['mobile'],
                    "紧急联系人: ": all_stuInfo[stuId]['emLinkPerson'],
                    "紧急联系人手机: ": all_stuInfo[stuId]['emLinkMobile'],
                    "辅导员: ": all_stuInfo[stuId]['auditName'],
                    "辅导员id: ": all_stuInfo[stuId]['auditId'],
                    "是否自动打卡: ": str(all_stuInfo[stuId]['needClock']),
                }
                for field, value in stuInfo.items():
                    response['message'] += field + value + '\n'
                logger.info(f'查询用户[{stuId}]的信息成功')
        return response
    except Exception as e:
        logger.error(f'查询用户信息时发生错误, error: {e}',)
        return { "success": False, "message": f"查询用户信息失败, {e}"}
    
if __name__ == '__main__':
    app.run(host='10.0.4.15', port=5555, debug=True)