[app]

# اسم التطبيق
title = حاسبة الضرائب

# اسم الحزمة
package.name = taxcalculator

# اسم المجلد
package.domain = org.samerawd

# الملف الرئيسي
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# الإصدار
version = 1.0

# المتطلبات
requirements = python3,kivy

# الأيقونة (اختياري - ضع مسار الأيقونة إذا كانت متوفرة)
#icon.filename = %(source.dir)s/icon.png

# التوجيه المسموح (portrait = عمودي، landscape = أفقي، all = الكل)
orientation = portrait

# الخدمات
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

# التحميل الكامل
fullscreen = 0

# إعدادات Android

[buildozer]

# السجل (0 = error only, 1 = info, 2 = debug)
log_level = 2

# مسار تحذيرات
warn_on_root = 1

# إعدادات بناء Android
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# معمارية (armeabi-v7a, arm64-v8a, x86, x86_64)
android.archs = arm64-v8a,armeabi-v7a
