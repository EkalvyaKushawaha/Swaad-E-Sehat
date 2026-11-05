import os
import urllib.request
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from menu.models import FoodItem

# Images save karne ke liye local media folders
media_food_dir = os.path.join('media', 'food_items')
os.makedirs(media_food_dir, exist_ok=True)

# Quality recipe images
photo_sources = {
    'salad.jpg': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=700&q=80',
    'bowl.jpg': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=700&q=80',
    'juice.jpg': 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=700&q=80',
    'tea.jpg': 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=700&q=80',
    'soup.jpg': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=700&q=80',
    'hero_bg.jpg': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1400&q=80',
    'default.jpg': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=700&q=80'
}

headers = {'User-Agent': 'Mozilla/5.0'}

print('Images download ho rahi hain, kripya 5 second wait karein...')
for filename, url in photo_sources.items():
    dest_path = os.path.join(media_food_dir, filename)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp, open(dest_path, 'wb') as out_file:
            out_file.write(resp.read())
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

# Database ke har FoodItem ko local image path assign karna
for item in FoodItem.objects.all():
    name_lower = item.name.lower()
    if 'salad' in name_lower:
        item.image = 'food_items/salad.jpg'
    elif 'bowl' in name_lower:
        item.image = 'food_items/bowl.jpg'
    elif 'juice' in name_lower:
        item.image = 'food_items/juice.jpg'
    elif 'tea' in name_lower:
        item.image = 'food_items/tea.jpg'
    elif 'soup' in name_lower:
        item.image = 'food_items/soup.jpg'
    else:
        item.image = 'food_items/default.jpg'
    item.save()

# Templates/home.html ko local hero image ke sath update karna
home_path = 'templates/home.html'
if os.path.exists(home_path):
    with open(home_path, 'r', encoding='utf-8') as f:
        html = f.read()
    # Hero online URL ko local media URL me replace karna
    html = html.replace('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1600&q=80', '/media/food_items/hero_bg.jpg')
    with open(home_path, 'w', encoding='utf-8') as f:
        f.write(html)

print('\n>>> SUCCESS: Saari images permanently aapke computer par save ho gayi hain! <<<')
