from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields
from pprint import pprint  
from datetime import datetime
# from workBitrix import get_task_work_time, create_item, get_crm_task, prepare_crm_task
# from collections import deque
import workBitrix
from dotenv import load_dotenv
import os
import requests 
from pprint import pformat
# from werkzeug.contrib.fixers import ProxyFix

load_dotenv()
PORT=os.getenv('PORT')
HOST=os.getenv('HOST')
app = Flask(__name__)
# app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='tovar system API',description='A pkGroup API\nЛоги можно посмотреть по пути /logs\nОчистить логи можно по пути /clear_logs\n',)
logs = []
PAY_ENTY_ID=os.getenv('PAY_ENTY_ID')


@api.route('/tovar/<int:dealID>')
class tovar_entity(Resource):
    def post(self, dealID):
        """Обновление сущности"""
        # data = request.__dict__ 
        # ImmutableMultiDict([('event', 'ONCRMDYNAMICITEMUPDATE'), ('data[FIELDS][ID]', '87'), ('data[FIELDS][ENTITY_TYPE_ID]', '155'), ('ts', '1715004068')])
        # data = request.form
        # PAY_ID=data['data[FIELDS][ID]']
        # enityID=data['data[FIELDS][ENTITY_TYPE_ID]']
        # if enityID != f'{PAY_ENTY_ID}': return 'Not pay'
        
        workBitrix.main(dealID=dealID)
        # print(f"{enityID=}")
        # pprint(data)
        
        # pprint(a)

        return 'OK'
    
    def get(self,):
        """Обновление сущности"""
        pprint(request)
        # data = request.get_json() 
        # pprint(data)
        return 'OK'


@app.route('/create_sum_deal/<int:dealID>', methods=['POST', 'GET'])
def create_sum_deal(dealID):
    productsDeal=workBitrix.find_product_entity(dealID)
    
    #просчет полей товаров(процесс) и сразу обновление товара
    for product in productsDeal:
        workBitrix.recalculate_product_fields(product['id'], product)
    #обновление суммы сделки
    workBitrix.sum_deal_create(productsDeal,dealID)
        
    return 'OK'

# Очередь для хранения логов
# logs_queue = deque(maxlen=10)  # Максимум 10 последних логов


# ДЛЯ ЛОГОВ
def log_counts_by_level(logs:list)->dict:
        counts = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0}
        for log in logs:
            counts[log['level']] += 1
        return counts

def log_counts_by_minute(logs:list)->dict:
        counts_by_minute = {}
        for log in logs:
            timestamp_minute = log['timestamp'][:16]  # Обрезаем до минут
            if timestamp_minute in counts_by_minute:
                counts_by_minute[timestamp_minute][log['level']] += 1
            else:
                counts_by_minute[timestamp_minute] = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0}
                counts_by_minute[timestamp_minute][log['level']] += 1
        return counts_by_minute

def send_log(message, level='INFO'):
    requests.post(f'http://{HOST}:{PORT}/logs', json={'log_entry': message, 'log_level': level})

@app.route("/logs", methods=['GET', 'POST'])
def index1():
    global logs
    if request.method == 'POST':
        logR=request.get_json()
        # pprint(log)
        log_entry = logR.get('log_entry')
        # log_entry = request.form.get('log_entry')
        if log_entry:
            # log_level = request.form.get('log_level', 'INFO')  # По умолчанию INFO
            log_level = logR.get('log_level', 'INFO')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            if len(logs) >= 100:
                logs.pop(0)
            logs.append({'timestamp': timestamp, 'level': log_level, 'message': log_entry})
            return 'Лог записан!'
        else:
            return 'Нет данных для записи в лог!'
    else:
        pprint(logs)
        for log in logs:
            if isinstance(log['message'], dict) or isinstance(log['message'], list):
                log['message'] = pformat(log['message'])

        logs.reverse()
        countsLog=log_counts_by_level(logs)
        countsLog=log_counts_by_minute(logs)
        pprint(countsLog)
        return render_template('index.html', logs=logs, log_counts=countsLog)
    
@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    logs.clear()
    return 'Логи очищены!'


@app.route('/', methods=['POST', 'GET'])
def handle_post_request():
    data=request.__dict__
    pprint(data)
    domain = request.args.get('DOMAIN')
    protocol = request.args.get('PROTOCOL')
    lang = request.args.get('LANG')
    app_sid = request.args.get('APP_SID')

    # здесь можно добавить код для обработки параметров из запроса
    # например, сохранить их в базу данных или выполнить какие-то другие действия

    return 'Request processed successfully'

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=False)
    # dealID=17452
    # workBitrix.main(dealID=dealID) 
    # create_sum_deal(dealID)

    
