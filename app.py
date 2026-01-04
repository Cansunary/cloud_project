import os
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Render'dan gelen veritabanı URL'sini al
DATABASE_URL = os.environ.get('DATABASE_URL')

HTML = """
<!DOCTYPE html>
<html>
<head><title>Ziyaretçi Defteri</title></head>
<body>
    <form method="POST">
        İsim: <input type="text" name="isim"><br>
        Şehir: <input type="text" name="sehir"><br>
        <input type="submit" value="Gönder">
    </form>
    <h3>Ziyaretçiler:</h3>
    <ul>
    {% for isim, sehir in ziyaretciler %}
        <li>Selam! Ben {{ isim }}, {{ sehir }}'den sevgiler.</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

def connect_db():
    # Render PostgreSQL için sslmode='require' zorunludur
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    conn = connect_db()
    cur = conn.cursor()
    
    # 1. Tabloyu oluştur ve MÜHÜRLE (commit)
     cur.execute("DROP TABLE IF EXISTS ziyaretciler")
    cur.execute("CREATE TABLE ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT, sehir TEXT)")
    conn.commit()

    # 2. Eğer form gönderildiyse veriyi kaydet
    if request.method == "POST":
        isim = request.form.get("isim")
        sehir = request.form.get("sehir")
        if isim and sehir:
            cur.execute("INSERT INTO ziyaretciler (isim, sehir) VALUES (%s, %s)", (isim, sehir))
            conn.commit()

    # 3. Verileri veritabanından çek (Hata aldığın "sehir" sütunu burada çekiliyor)
    cur.execute("SELECT isim, sehir FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    ziyaretciler = cur.fetchall()

    cur.close()
    conn.close()
    
    return render_template_string(HTML, ziyaretciler=ziyaretciler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
