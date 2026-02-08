from flask import Flask, jsonify
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

@app.route("/health")
def health():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 503


@app.route("/")
def index():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO visits (timestamp) VALUES (NOW())")
        cur.execute("SELECT COUNT(*) FROM visits")
        count = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return f"""
        <h1>Flask App on Kubernetes</h1>
        <p>Visits: <strong>{count}</strong></p>
        <p>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><a href="/health">Health Check</a></p>
        """
    except Exception as e:
        return f"Database error: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)