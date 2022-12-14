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
    return 'ping success π!!!'

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
                response['message'] = 'ε­¦ε·ε·²η»ε­ε¨'
                break
            elif new_stuInfo['name'] == stuInfo['name']:
                response['success'] = False
                response['message'] = 'ε§εε·²η»ε­ε¨'
                break
            elif new_stuInfo['mobile'] == stuInfo['mobile']:
                response['success'] = False
                response['message'] = 'ζζΊε·ε·²η»ε­ε¨'
                break

        # ε¦ζδΈε­ε¨οΌεζ°ζ·»ε δΈδΈͺ
        if response['success']:
            with open('../studentsInfo.json', 'w') as f:
                new_stuInfo['needClock'] = True
                all_stuInfo[new_stuInfo['id']] = new_stuInfo
                json.dump(all_stuInfo, f, indent=4, ensure_ascii=False)
                response['message'] = 'η¨ζ· '+ new_stuInfo['name'] +' ζ·»ε θͺε¨ζε‘ζεπ'
                pusher.send_text('auto_clock','zhangjiawei', response['message'])
                logger.info('η¨ζ· %s ε ε₯ζε‘εεζε', new_stuInfo['name'])
        return response
    except Exception as e:
        logger.error(f'ε ε₯ζε‘εεζΆεηιθ――, error: {e}')
        response['success'] = False
        response['message'] = 'ζ·»ε θͺε¨ζε‘ε€±θ΄₯π€, error: \n' + str(e)
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
                    # δΏ?ζΉδΏ‘ζ―
                    for field, value in modify_stuInfo.items():
                        if value != '':
                            all_stuInfo[stuId][field] = value
                    json.dump(all_stuInfo, f, indent=4, ensure_ascii=False)
                    # ζι θΏεresponse
                    response['success'] = True
                    whetherInSchool = ''
                    if all_stuInfo[stuId]['whetherInSchool'] == '1':
                        whetherInSchool = 'δ»ε€©ε¨ζ ‘ε­ε'
                    elif all_stuInfo[stuId]['whetherInSchool'] == '2':
                        whetherInSchool = 'ε·²η¦»ζ ‘οΌε¨ζ­ε·η§ζΏ'
                    elif all_stuInfo[stuId]['whetherInSchool'] == '3':
                        whetherInSchool = 'ε·²θΏδΉ‘'
                    else:
                        whetherInSchool = 'θ―₯ε­ζ?΅εΊιοΌθ―·θη³»δ½θ'
                        
                    _stuInfo = {
                        "ε­¦ ε·: ": all_stuInfo[stuId]['id'],
                        "ε§ ε: ": all_stuInfo[stuId]['name'],
                        "ζ§ ε«: ": "η·" if all_stuInfo[stuId]['sex'] == "1" else "ε₯³",
                        "ε­¦ ι’: ": all_stuInfo[stuId]['company'],
                        "ε½εδ½η½?: ": all_stuInfo[stuId]['currentLocation'],
                        "ζ―ε¦ε¨ζ ‘ε­ε: ": whetherInSchool,
                        "εΉ΄ ηΊ§: ": all_stuInfo[stuId]['grade'],
                        "ζ ζΊ: ": all_stuInfo[stuId]['mobile'],
                        "η΄§ζ₯θη³»δΊΊ: ": all_stuInfo[stuId]['emLinkPerson'],
                        "η΄§ζ₯θη³»δΊΊζζΊ: ": all_stuInfo[stuId]['emLinkMobile'],
                        "θΎε―Όε: ": all_stuInfo[stuId]['auditName']
                    }
                    response['message'] = 'δΏ?ζΉζε,ε½εδΏ‘ζ―δΈΊ\n\n'
                    for field, value in _stuInfo.items():
                        response['message'] += field + value + '\n'
                    response['message'] += "ππππ"
                    logger.info('η¨ζ· %s δΏ?ζΉδΏ‘ζ―ζεπ' % (all_stuInfo[stuId]['name']))
                    return response
        # ε¦ζδΈε­ε¨οΌεθΏεwarning
        response['success'] = False
        response['message'] = 'δΏ?ζΉε€±θ΄₯\nε­¦ε· ' + stuId + ' δΈε­ε¨π€'
        logger.info('δΏ?ζΉδΏ‘ζ―ε€±θ΄₯, ε­¦ε· %s δΈε­ε¨π€' % stuId)
        return response
    except Exception as e:
        response['success'] = False
        response['message'] = 'δΏ?ζΉδΏ‘ζ―ε€±θ΄₯π€, error: \n' + str(e)
        logger.error('η¨ζ· %s δΏ?ζΉδΏ‘ζ―ζΆεηιθ――, error: %s' % (request.get_json()['id'], e))
        return response
    
@app.route('/stopClock', methods=['POST'])
def stop_clock():
    try:
        stuId = request.get_json()['id']
        response = { 
            "success": False, 
            "message": "ζ δΊεη"
        }
        all_stuInfo = dict()
        with open('../studentsInfo.json', 'r') as f:
            all_stuInfo = json.load(f)
        with open('../studentsInfo.json', 'w') as f:
            if stuId not in all_stuInfo.keys():
                response['success'] = False
                response['message'] = 'θ―₯ε­¦ε·δΈε­ε¨π€'
                logger.info('δΏ?ζΉη¨ζ· %s ηθͺε¨ζε‘ηΆζε€±θ΄₯οΌθ―₯η¨ζ·δΈε­ε¨' % stuId)
            else:
                all_stuInfo[stuId]['needClock'] = not all_stuInfo[stuId]['needClock']
                json.dump(all_stuInfo, f, indent=4, ensure_ascii=False)
                response['success'] = True
                response['message'] = 'δΏ?ζΉηΆζζε, η°ε¨ηηΆζοΌ\nζ­£εΈΈθͺε¨ζε‘π\n' if all_stuInfo[stuId]['needClock'] else 'δΏ?ζΉηΆζζε, η°ε¨ηηΆζοΌ\nεζ­’θͺε¨ζε‘π\n'
                response['message'] += 'ζη€Ί: ζ―ε€©εζ¨1ηΉ-2ηΉδΉι΄δΌθΏθ‘ζε‘, θ―·εΏε¨ζ­€ζΆδΏ?ζΉηΆζπ'
                logger.info('η¨ζ· %s δΏ?ζΉηΆζζε, ε½εζ―ε¦θͺε¨ζε‘: %s', all_stuInfo[stuId]['name'], str(all_stuInfo[stuId]['needClock']))
        return response
    except Exception as e:
        logger.error(f'δΏ?ζΉζε‘ηΆζζΆεηιθ――, error: {e}',)
        return { "success": False, "message": f"δΏ?ζΉζε‘ηΆζιθ――πͺ, error:\n {e}"}

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
                response['message'] = 'θ―₯ε­¦ε·δΈε­ε¨π€'
                logger.info('ζ₯θ―’η¨ζ· %s ηδΏ‘ζ―ε€±θ΄₯οΌθ―₯η¨ζ·δΈε­ε¨' % stuId)
            else:
                response['success'] = True
                whetherInSchool = ''
                if all_stuInfo[stuId]['whetherInSchool'] == '1':
                    whetherInSchool = 'δ»ε€©ε¨ζ ‘ε­ε'
                elif all_stuInfo[stuId]['whetherInSchool'] == '2':
                    whetherInSchool = 'ε·²η¦»ζ ‘οΌε¨ζ­ε·η§ζΏ'
                elif all_stuInfo[stuId]['whetherInSchool'] == '3':
                    whetherInSchool = 'ε·²θΏδΉ‘'
                else:
                    whetherInSchool = 'θ―₯ε­ζ?΅εΊιοΌθ―·θη³»δ½θ'
                stuInfo = {
                    "ε­¦ ε·: ": all_stuInfo[stuId]['id'],
                    "ε§ ε: ": all_stuInfo[stuId]['name'],
                    "ζ§ ε«: ": "η·" if all_stuInfo[stuId]['sex'] == "1" else "ε₯³",
                    "ε­¦ ι’: ": all_stuInfo[stuId]['company'],
                    "ε½εδ½η½?: ": all_stuInfo[stuId]['currentLocation'],
                    "ζ―ε¦ε¨ζ ‘ε­ε: ": whetherInSchool,
                    "εΉ΄ ηΊ§: ": all_stuInfo[stuId]['grade'],
                    "ζ ζΊ: ": all_stuInfo[stuId]['mobile'],
                    "η΄§ζ₯θη³»δΊΊ: ": all_stuInfo[stuId]['emLinkPerson'],
                    "η΄§ζ₯θη³»δΊΊζζΊ: ": all_stuInfo[stuId]['emLinkMobile'],
                    "θΎε―Όε: ": all_stuInfo[stuId]['auditName'],
                    "ζ―ε¦θͺε¨ζε‘: ": str(all_stuInfo[stuId]['needClock']),
                }
                for field, value in stuInfo.items():
                    response['message'] += field + value + '\n'
                response['message'] += "ππππ"
                logger.info('ζ₯θ―’η¨ζ· %s ηδΏ‘ζ―ζε' % all_stuInfo[stuId]['name'])
        return response
    except Exception as e:
        logger.error(f'ζ₯θ―’η¨ζ·δΏ‘ζ―ζΆεηιθ――, error: {e}',)
        return { "success": False, "message": f"ζ₯θ―’η¨ζ·δΏ‘ζ―ε€±θ΄₯π₯, error:\n{e}"}

@app.route('/saytome', methods=['POST'])
def receive_idea():
    try:
        idea = request.get_json()['idea']
        
        if 'zjw' in idea or 'sbzjw' in idea or 'εΌ δ½³δΌ' in idea or 'ε»ιΌεΌ δ½³δΌ' in idea or 'εΌ δ½³η?' in idea or 'εΏε­' in idea:
            logger.info('ζδΊΊζδΊ€idea: ' + idea + ', zjwη»δ»η«δΊδΈͺδΈ­ζπ')
            pusher.send_text('auto_clock','zhangjiawei','ζδΊΊζδΊ€idea: ' + idea + 'δ½ζ―δ½θη»δ»η«δΊδΈͺδΈ­ζπ')
            return { "success": True, "message": "zjwη»δ½ η«δΊδΈͺδΈ­ζπ" }
        else:
            logger.info('ζδΊΊζδΊ€idea: ' + idea)
            pusher.send_text('auto_clock','zhangjiawei','ζδΊΊζδΊ€idea: ' + idea)
            return { "success": True, "message": "ζθ°’δ½ ηζ³ζ³π" }
    except Exception as e:
        logger.error(f'ζδΊ€ideaζΆεηιθ――, error: {e}',)
        return { "success": False, "message": f"ζδΊ€ζΆεηιθ――πͺ, error:\n {e}"}

if __name__ == '__main__':
    app.run(host='10.0.4.15', port=5555, debug=True)