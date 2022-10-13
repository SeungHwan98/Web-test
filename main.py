import os
import xml.etree.ElementTree as ET

from logging import Logger

from flask import Flask, render_template

from database.DBManager import DBManager

# PARAMETERS
SERVER_CONFIG_PATH = './server_config.xml'
SERVER_REPOSITORY_DIR_PATH = './'

# APP
app = Flask(__name__)
# Database
dbManager = DBManager()

@app.route('/')
def hello():

    return '동작'

@app.route('/<alarm_id>', methods=['GET','POST'])
def view_dt_alarm_template(alarm_id):

    alarm = dbManager.get_alarm(alarm_id)

    if alarm == None:
        return 'None'

    alarm_time = "{} {}".format(alarm['date'], alarm['time'])
    alarm_model_id = alarm['alarm_model_id']
    alarm_message = alarm['alarm_message']
    dt_view_image_path = 'dt_view_image.png'
    sps_chart_image_path = 'sps_chart_image.png'
    doorfoam_chart_image_path = 'doorfoam_chart_image.png'

    return render_template('lg_dt_alarm_template.html',
                           alarm_id = alarm_id,
                           alarm_time = alarm_time,
                           alarm_model_id = alarm_model_id,
                           alarm_message = alarm_message,
                           dt_view_image_path=dt_view_image_path,
                           sps_chart_image_path = sps_chart_image_path,
                           doorfoam_chart_image_path = doorfoam_chart_image_path)

# ** -- main -- **
if __name__ == '__main__':

    try:

        if os.path.exists(SERVER_CONFIG_PATH):

            tree = ET.parse(SERVER_CONFIG_PATH)

            root_element = tree.getroot()
            port_element = root_element.find('Port')
            maxContentLength_element = root_element.find('MaxContentLength')

            port = int(port_element.text)
            maxContentLength = int(maxContentLength_element.text)

            app.config['MAX_CONTENT_LENGTH'] = maxContentLength  # 파일 업로드 용량 제한 단위:바이트
            # 서버 실행
            app.run(host='0.0.0.0', port=port)

    except Exception as e:

        Logger.error(str(e))