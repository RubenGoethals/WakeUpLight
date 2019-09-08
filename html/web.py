import os
from flask import Flask, render_template, request, make_response
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL(app)

btn1 = True
btn2 = True
musicpath = os.listdir(r"/home/pi/Documents/Flask_web/static/music/nature music")
#lsize = str(len(musicpath))
looper = len(musicpath)

app.config['MYSQL_DATABASE_USER'] = 'your username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'your password'
app.config['MYSQL_DATABASE_DB'] = 'your database name'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

def set_data(sql, params=None):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    try:
        print(sql)
        cursor.execute(sql, params)
        conn.commit()
        print("SQL uitgevoerd")
    except Exception as e:
        print("Fout bij het uitvoeren van sql: {0}".format(e))
        return False
    cursor.close()
    conn.close()
    
    return True


@app.route("/")
def start():       
    return render_template("index.html", btn1 = btn1)

@app.route("/light", methods = ['GET','POST'])
def light():
    global btn1
    if request.method == "POST":
        if request.form['lamp'] == 'on':
            btn1 = False
            set_data("UPDATE ledstrip SET ledstrip_state=%s", request.form['lamp'])
        elif request.form['lamp'] == 'off':
            btn1 = True
            set_data("UPDATE ledstrip SET ledstrip_state=%s", request.form['lamp'])
    
    return render_template("light.html", btn1 = btn1)

@app.route("/light_color", methods = ['POST'])
def light_color():
    if request.method == "POST":
        color = request.form['color']
        set_data("UPDATE ledstrip SET ledstrip_color=%s", color)
        print(color)
    
    return render_template("light.html")

@app.route("/alarm_clock", methods = ['GET','POST'])
def alarm_clock():
    global looper
    global musicpath
    
    if request.method == "POST":
        music = request.form['som']
        color = request.form['color']
        date = request.form['time']
        set_data("UPDATE wakeup SET wakeup_color=%s, wakeup_music=%s, wakeup_date=%s", (color, music, date))
        print(music)
        
    return render_template("alarm_clock.html", looper=looper, musicpath=musicpath)

@app.route("/music", methods = ['GET','POST'])
def music():
    global btn2
    musicpath = os.listdir(r"/home/pi/Documents/Flask_web/static/music/playlist")
    looper = len(musicpath)
    
    if request.method == "POST":
        if request.form['sound'] == 'on':
            btn2 = False
            set_data("UPDATE music SET music_state=%s", request.form['sound'])
        elif request.form['sound'] == 'off':
            btn2 = True
            set_data("UPDATE music SET music_state=%s", request.form['sound'])
    
    return render_template("music.html", btn2 = btn2, looper=looper, musicpath=musicpath)

@app.route("/music_song", methods = ['GET','POST'])
def music_song():
    global btn2
    musicpath = os.listdir(r"/home/pi/Documents/Flask_web/static/music/playlist")
    looper = len(musicpath)

    
    if request.method == "POST":
        song = request.form['som']
        set_data("UPDATE music SET music_name=%s", song)
        print(music)
    
    return render_template("music.html", btn2 = btn2, looper=looper, musicpath=musicpath)


if __name__ == '__main__':
    host = "0.0.0.0"
    app.run(host=host, port=80, debug=True)
