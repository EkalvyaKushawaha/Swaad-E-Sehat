import os

# 1. config/settings.py mein MEDIA_URL aur MEDIA_ROOT check/add karna
settings_path = 'config/settings.py'
with open(settings_path, 'r', encoding='utf-8') as f:
    s_content = f.read()

if 'MEDIA_ROOT' not in s_content:
    media_settings = "\nMEDIA_URL = '/media/'\nMEDIA_ROOT = BASE_DIR / 'media'\n"
    s_content += media_settings
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(s_content)
    print("Added MEDIA_ROOT to settings.py")

# 2. config/urls.py mein static(settings.MEDIA_URL) serve route add karna
urls_path = 'config/urls.py'
with open(urls_path, 'r', encoding='utf-8') as f:
    u_content = f.read()

if 'settings.MEDIA_URL' not in u_content:
    if 'from django.conf import settings' not in u_content:
        u_content = "from django.conf import settings\nfrom django.conf.urls.static import static\n" + u_content
    elif 'from django.conf.urls.static import static' not in u_content:
        u_content = "from django.conf.urls.static import static\n" + u_content

    u_content += "\nurlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n"
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(u_content)
    print("Added MEDIA serving to urls.py")

# 3. templates/home.html me clean fallback setup karna
home_path = 'templates/home.html'
if os.path.exists(home_path):
    with open(home_path, 'r', encoding='utf-8') as f:
        h = f.read()
    # Image tag ko direct item.image.url render karne ke liye format karna
    target_img_block = """        {% if item.image %}
          <img src="{{ item.image.url }}" alt="{{ item.name }}" class="dish-img">
        {% else %}
          <img src="/media/food_items/default.jpg" alt="{{ item.name }}" class="dish-img">
        {% endif %}"""
    if '<div class="dish-img-box">' in h:
        start_idx = h.find('<div class="dish-img-box">') + len('<div class="dish-img-box">')
        end_idx = h.find('<span class="category-tag">', start_idx)
        if end_idx != -1:
            h = h[:start_idx] + "\n" + target_img_block + "\n        " + h[end_idx:]
            with open(home_path, 'w', encoding='utf-8') as f:
                f.write(h)
            print("Updated home.html template image tag")

print("\n>>> SUCCESS: Media Config & URLs Fixed! Local images are now active. <<<\n")