import io
import os
import pymysql
import PIL.Image as Image

class DBManager:

    conn : pymysql.connections.Connection
    cursor : pymysql.connections.Connection.cursor

    def __init__(self):

        self.conn = pymysql.connect(
            user='root',
            passwd='1111',
            host='127.0.0.1',
            db='lg_dt_db',
            charset='utf8'
        )

        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def get_alarm(self,alarm_id):

        sql = "SELECT * FROM `alarm_history` WHERE `alarm_id` = '{}';".format(alarm_id)
        self.cursor.execute(sql)

        result = self.cursor.fetchone()

        alarm_dir_path = './static/images/{}/'.format(alarm_id)
        if not os.path.exists(alarm_dir_path):
            os.mkdir(alarm_dir_path)

        if result == None:
            return None

        dt_view_image_path = alarm_dir_path + 'dt_view_image.png'
        sps_chart_image_path = alarm_dir_path + 'sps_chart_image.png'
        doorfoam_chart_image_path = alarm_dir_path + 'doorfoam_chart_image.png'

        self.check_image_path(result, "dt_view_image", dt_view_image_path)
        self.check_image_path(result, "sps_chart_image", sps_chart_image_path)
        self.check_image_path(result, "doorfoam_chart_image", doorfoam_chart_image_path)

        return result

    #region Image
    def check_image_path(self, sql_result, column_name, image_path):

        if not os.path.exists(image_path):

            image_bytearr = sql_result[column_name]
            image = Image.open(io.BytesIO(image_bytearr))
            image.save(image_path)
    #endregion Image End