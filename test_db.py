from app.database import engine
from sqlalchemy import text

print("Testing connection...")

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database Connected Successfully!")
except Exception as e:
    print("❌ Connection Failed:", e)