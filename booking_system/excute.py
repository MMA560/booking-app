import sqlite3

# إعداد الاتصال بقاعدة البيانات
db_path = "your_database.db"  # اسم قاعدة البيانات الخاصة بك
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# المسار للصورة الافتراضية
default_image_path = "images/image.jpg"  # مسار الصورة الافتراضية

# تحديث جميع الغرف لإضافة المسار للصورة الافتراضية
try:
    cursor.execute("UPDATE bookings SET image_url = ? WHERE image_url IS NULL", (default_image_path,))
    conn.commit()
    print("تم تحديث جميع الغرف لتستخدم الصورة الافتراضية.")
except Exception as e:
    print(f"حدث خطأ: {e}")

# إغلاق الاتصال بقاعدة البيانات
conn.close()
