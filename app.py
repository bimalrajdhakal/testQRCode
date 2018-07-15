# coding=utf-8

from flask import Flask, render_template, flash, redirect, request, url_for, session, logging,send_file
from flask_mysqldb import MySQL
import qrcode
import cStringIO


app = Flask(__name__)

# config database

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bimal'
app.config['MYSQL_DB'] = 'eloc_database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init mysql
mysql = MySQL(app)



def random_qr():
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=4,
                       border=2)
    eloc_id='2JKR8A'

    cur = mysql.connection.cursor()
    # get data by eloc id
    result = cur.execute("SELECT * FROM eloc_master_tbl WHERE eloc_id = %s", [eloc_id])
    data = cur.fetchone()
    print data
    
    qrdata=( 'H.No:'+ data['hno']+'Street:'+data['street']+'Landmark:'+data['landmark']+'Area:'+data['area']
            +'Village/Town:'+data['village_town']+'Pincode:'+data['pincode'])
    
    print qrdata
    mysql.connection.commit()
    cur.close()

    qr.add_data(qrdata)
    qr.make(fit=True)
    img = qr.make_image()
    return img


@app.route('/get_qrimg')
def get_qrimg():
    img_buf = cStringIO.StringIO()
    # filename='static/abc.png'
    img = random_qr()
    img.save(img_buf)
    img_buf.seek(0)
    return send_file(img_buf, mimetype='image/png')

@app.route('/show_qr')
def show_qr():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)