from flask import Flask, request, make_response
from log import logger
from notPusher import pusher

import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

app.config['JSON_AS_ASCII'] = False

@app.route('/ping', methods=['GET', 'POST'])
def test():
    return 'ping success 😋!!!'

@app.route('/join', methods=['POST'])
def add_stuInfo():
    response = { 
        "success": True, 
        "message": ""
    }
    try:
        new_stuInfo = request.get_json()
        all_stuInfo = dict()
        with open('../studentsInfo.json', 'r') as f:
            all_stuInfo = json.load(f)
    
        for _, stuInfo in all_stuInfo.items():
            if new_stuInfo['id'] == stuInfo['id']:
                response['success'] = False
                response['message'] = '学号已经存在'
                break
            elif new_stuInfo['name'] == stuInfo['name']:
                response['success'] = False
                response['message'] = '姓名已经存在'
                break
            elif new_stuInfo['mobile'] == stuInfo['mobile']:
                response['success'] = False
                response['message'] = '手机号已经存在'
                break

        # 如果不存在，则新添加一个
        if response['success']:
            with open('../studentsInfo.json', 'w') as f:
                new_stuInfo['needClock'] = True
                all_stuInfo[new_stuInfo['id']] = new_stuInfo
                json.dump(all_stuInfo, f, indent=4, ensure_ascii=False)
                response['message'] = '用户 '+ new_stuInfo['name'] +' 添加自动打卡成功😋'
                pusher.send_text('auto_clock','zhangjiawei', response['message'])
                logger.info('用户 %s 加入打卡名单成功', new_stuInfo['name'])
        return response
    except Exception as e:
        logger.error(f'加入打卡名单时发生错误, error: {e}')
        response['success'] = False
        response['message'] = '添加自动打卡失败🤔, error: \n' + str(e)
        return response

@app.route('/modify', methods=['POST'])
def modify_stuInfo():
    response = { 
        "success": True, 
        "message": ""
    }
    try:
        modify_stuInfo = request.get_json()
        all_stuInfo = dict()
        with open('../studentsInfo.json', 'r') as f:
            all_stuInfo = json.load(f)
    
        stuId = modify_stuInfo['id']
        for _, stuInfo in all_stuInfo.items():
            if stuInfo['id'] == stuId:
                with open('../studentsInfo.json', 'w') as f:
                    # 修改信息
                    for field, value in modify_stuInfo.items():
                        if value != '':
                            all_stuInfo[stuId][field] = value
                    json.dump(all_stuInfo, f, indent=4, ensure_ascii=False)
                    # 构造返回response
                    response['success'] = True
                    whetherInSchool = ''
                    if all_stuInfo[stuId]['whetherInSchool'] == '1':
                        whetherInSchool = '今天在校园内'
                    elif all_stuInfo[stuId]['whetherInSchool'] == '2':
                        whetherInSchool = '已离校，在杭州租房'
                    elif all_stuInfo[stuId]['whetherInSchool'] == '3':
                        whetherInSchool = '已返乡'
                    else:
                        whetherInSchool = '该字段出错？请联系作者'
                        
                    _stuInfo = {
                        "学 号: ": all_stuInfo[stuId]['id'],
                        "姓 名: ": all_stuInfo[stuId]['name'],
                        "性 别: ": "男" if all_stuInfo[stuId]['sex'] == "1" else "女",
                        "学 院: ": all_stuInfo[stuId]['company'],
                        "当前位置: ": all_stuInfo[stuId]['currentLocation'],
                        "是否在校园内: ": whetherInSchool,
                        "年 级: ": all_stuInfo[stuId]['grade'],
                        "手 机: ": all_stuInfo[stuId]['mobile'],
                        "紧急联系人: ": all_stuInfo[stuId]['emLinkPerson'],
                        "紧急联系人手机: ": all_stuInfo[stuId]['emLinkMobile'],
                        "辅导员: ": all_stuInfo[stuId]['auditName']
                    }
                    response['message'] = '修改成功,当前信息为\n\n'
                    for field, value in _stuInfo.items():
                        response['message'] += field + value + '\n'
                    response['message'] += "🙂🙂🙂🙂"
                    logger.info('用户 %s 修改信息成功🙂' % (all_stuInfo[stuId]['name']))
                    return response
        # 如果不存在，则返回warning
        response['success'] = False
        response['message'] = '修改失败\n学号 ' + stuId + ' 不存在🤔'
        logger.info('修改信息失败, 学号 %s 不存在🤔' % stuId)
        return response
    except Exception as e:
        response['success'] = False
        response['message'] = '修改信息失败🤔, error: \n' + str(e)
        logger.error('用户 %s 修改信息时发生错误, error: %s' % (request.get_json()['id'], e))
        return response
    
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
                response['message'] = '该学号不存在🤔'
                logger.info('修改用户 %s 的自动打卡状态失败，该用户不存在' % stuId)
            else:
                all_stuInfo[stuId]['needClock'] = not all_stuInfo[stuId]['needClock']
                json.dump(all_stuInfo, f, indent=4, ensure_ascii=False)
                response['success'] = True
                response['message'] = '修改状态成功, 现在的状态：\n正常自动打卡😄\n' if all_stuInfo[stuId]['needClock'] else '修改状态成功, 现在的状态：\n停止自动打卡😞\n'
                response['message'] += '提示: 每天凌晨1点-2点之间会进行打卡, 请勿在此时修改状态😗'
                logger.info('用户 %s 修改状态成功, 当前是否自动打卡: %s', all_stuInfo[stuId]['name'], str(all_stuInfo[stuId]['needClock']))
        return response
    except Exception as e:
        logger.error(f'修改打卡状态时发生错误, error: {e}',)
        return { "success": False, "message": f"修改打卡状态错误😪, error:\n {e}"}

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
                response['message'] = '该学号不存在🤔'
                logger.info('查询用户 %s 的信息失败，该用户不存在' % stuId)
            else:
                response['success'] = True
                whetherInSchool = ''
                if all_stuInfo[stuId]['whetherInSchool'] == '1':
                    whetherInSchool = '今天在校园内'
                elif all_stuInfo[stuId]['whetherInSchool'] == '2':
                    whetherInSchool = '已离校，在杭州租房'
                elif all_stuInfo[stuId]['whetherInSchool'] == '3':
                    whetherInSchool = '已返乡'
                else:
                    whetherInSchool = '该字段出错？请联系作者'
                stuInfo = {
                    "学 号: ": all_stuInfo[stuId]['id'],
                    "姓 名: ": all_stuInfo[stuId]['name'],
                    "性 别: ": "男" if all_stuInfo[stuId]['sex'] == "1" else "女",
                    "学 院: ": all_stuInfo[stuId]['company'],
                    "当前位置: ": all_stuInfo[stuId]['currentLocation'],
                    "是否在校园内: ": whetherInSchool,
                    "年 级: ": all_stuInfo[stuId]['grade'],
                    "手 机: ": all_stuInfo[stuId]['mobile'],
                    "紧急联系人: ": all_stuInfo[stuId]['emLinkPerson'],
                    "紧急联系人手机: ": all_stuInfo[stuId]['emLinkMobile'],
                    "辅导员: ": all_stuInfo[stuId]['auditName'],
                    "是否自动打卡: ": str(all_stuInfo[stuId]['needClock']),
                }
                for field, value in stuInfo.items():
                    response['message'] += field + value + '\n'
                response['message'] += "🙂🙂🙂🙂"
                logger.info('查询用户 %s 的信息成功' % all_stuInfo[stuId]['name'])
        return response
    except Exception as e:
        logger.error(f'查询用户信息时发生错误, error: {e}',)
        return { "success": False, "message": f"查询用户信息失败😥, error:\n{e}"}

@app.route('/saytome', methods=['POST'])
def receive_idea():
    try:
        idea = request.get_json()['idea']
        
        if 'zjw' in idea or 'sbzjw' in idea or '张佳伟' in idea or '傻逼张佳伟' in idea or '张佳玮' in idea or '儿子' in idea:
            logger.info('有人提交idea: ' + idea + ', zjw给他竖了个中指😏')
            pusher.send_text('auto_clock','zhangjiawei','有人提交idea: ' + idea + '但是作者给他竖了个中指😏')
            return { "success": True, "message": "zjw给你竖了个中指😏" }
        else:
            logger.info('有人提交idea: ' + idea)
            pusher.send_text('auto_clock','zhangjiawei','有人提交idea: ' + idea)
            return { "success": True, "message": "感谢你的想法😊" }
    except Exception as e:
        logger.error(f'提交idea时发生错误, error: {e}',)
        return { "success": False, "message": f"提交时发生错误😪, error:\n {e}"}

if __name__ == '__main__':
    app.run(host='10.0.4.15', port=5555, debug=True)