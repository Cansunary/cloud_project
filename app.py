from flask import Flask, render_template_string, request
import os
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL","postgresql://cansu:9jSZui0vOmWIgRptyHlWgKpeTSisfBA8@dpg-d5da5eeuk2gs738s33u0-a.oregon-postgres.render.com/cloud_db_d492?sslmode=require")

HTML = """
<!doctype html>
<html>
<head>
<title>Buluttan Selam!</title>
<style>
body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
h1 { color: #333; }
form { margin: 20px auto; }
input { padding: 10px; font-size: 16px; }
button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
ul { list-style: none; padding: 0px; }
li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; }
</style>
</head>

<body>
<h1>Ziyaretçi Defteri</h1>
<p>Adını yaz, selamını bırak!</p>
<form method="POST">
  <input type="text" name="isim" placeholder="Adını yaz" required>
  <input type="text" name="sehir" placeholder="Şehrini yaz" required>
  <button type="submit">Gönder</button>
</form
<h3>Ziyaretçiler:</h3>
<ul>
  {% for isim, sehir in ziyaretciler %}
    <li>Selam! Ben {{ isim }} {{ sehir }}'den sevgiler.</li><li>{{ isim }} ({{ sehir }})</li>
  {% endfor %}
</ul>
</body>
</html>
"""

def connect_db():
 conn = psycopg2.connect(DATABASE_URL, sslmode='require')
  return conn

@app.route("/", methods=["GET", "POST"])
def index():
  conn = connect_db()
  cur = conn.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT, sehir TEXT)")


  if request.method == "POST":
    isim =request.form.get("isim")
    sehir = request.form.get("sehir")
    if isim and sehir:
      cur.execute("INSERT INTO ziyaretciler (isim,sehir) VALUES (%s, %s)", (isim, sehir))
      conn.commit()

  cur.execute("SELECT isim, sehir FROM ziyaretciler ORDER BY id DESC LIMIT 10")
  ziyaretciler = cur.fetchall()

  cur.close()
  conn.close()
  return render_template_string(HTML, ziyaretciler=ziyaretciler)

if __name__=="__main__":
  app.run(host="0.0.0.0", port=5000)
