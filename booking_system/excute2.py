import sqlite3

# إعداد الاتصال بقاعدة البيانات
db_path = "your_database.db"  # تأكد من استخدام اسم قاعدة البيانات الخاصة بك
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# إضافة العمود image_url
try:
    cursor.execute("ALTER TABLE bookings ADD COLUMN image_url TEXT;")
    conn.commit()
    print("تم إضافة العمود image_url بنجاح.")
except sqlite3.OperationalError as e:
    print(f"حدث خطأ: {e}")  # إذا كان العمود موجودًا مسبقًا، ستظهر رسالة خطأ

# إغلاق الاتصال بقاعدة البيانات
conn.close()
