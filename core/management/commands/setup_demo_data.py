from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from menu.models import Category, FoodItem
from tables.models import CafeTable
from accounts.models import CustomerProfile

class Command(BaseCommand):
    help = "Populate database with demo categories, foods, tables and accounts"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@cafe.com', 'admin123')
            CustomerProfile.objects.create(user=admin)
            self.stdout.write("Created Superuser: admin / admin123")

        if not User.objects.filter(username='delivery1').exists():
            staff = User.objects.create_user('delivery1', 'del@cafe.com', 'delivery123')
            CustomerProfile.objects.create(user=staff, phone="9876543210", is_delivery_staff=True)
            self.stdout.write("Created Delivery Staff: delivery1 / delivery123")

        categories = [
            ("Salads & Bowls", "Wholesome bowls"),
            ("Breakfast & Oats", "High protein energy meals"),
            ("Detox & Fresh Juices", "Cold-pressed pure juices"),
            ("Healthy Meals", "High protein, organic plates"),
            ("Herbal Teas", "Ayurvedic immunity teas"),
        ]
        cat_map = {}
        for cname, cdesc in categories:
            cat, _ = Category.objects.get_or_create(name=cname, defaults={'description': cdesc})
            cat_map[cname] = cat

        foods = [
            ("Quinoa Avocado Power Bowl", "Salads & Bowls", 249.00, "Cooked organic quinoa, sliced Hass avocados, chickpeas.", True),
            ("Sprouted Moong Salad", "Salads & Bowls", 149.00, "Sprouted mung beans, pomegranate pearls, lemon zest.", False),
            ("Berry Chia Seed Pudding", "Breakfast & Oats", 199.00, "Almond milk infused chia seeds with blueberries.", True),
            ("Steel-Cut Masala Oats", "Breakfast & Oats", 169.00, "Steel-cut oats cooked with fresh spinach, carrots, and turmeric.", False),
            ("Green Goddess Detox Juice", "Detox & Fresh Juices", 129.00, "Celery, cucumber, green apple, ginger. Zero sugar.", True),
            ("Beetroot Glow Cold Press", "Detox & Fresh Juices", 139.00, "Fresh beetroot, Valencia orange, and carrot.", False),
            ("Grilled Paneer Protein Bowl", "Healthy Meals", 289.00, "Herb-marinated grilled paneer, sauteed broccoli, brown rice.", True),
            ("Steamed Millet Khichdi", "Healthy Meals", 219.00, "Foxtail millet cooked with yellow lentils, desi ghee.", False),
            ("Ashwagandha Golden Milk", "Herbal Teas", 119.00, "Desi cow milk simmered with organic turmeric and herbs.", False),
            ("Kashmiri Kahwa Green Tea", "Herbal Teas", 99.00, "Green tea infused with saffron strands and crushed almonds.", False),
            ("Flaxseed Ragi Wrap", "Healthy Meals", 179.00, "Handmade ragi roti stuffed with crunchy vegetables and hummus.", True),
            ("Tender Coconut Water Cooler", "Detox & Fresh Juices", 109.00, "Pure tender coconut water with soaked basil seeds.", False),
        ]

        for fname, cname, price, desc, feat in foods:
            FoodItem.objects.get_or_create(
                name=fname,
                defaults={
                    'category': cat_map[cname],
                    'price': Decimal(str(price)),
                    'description': desc,
                    'is_available': True,
                    'is_featured': feat,
                }
            )

        for num in range(1, 9):
            table, _ = CafeTable.objects.get_or_create(table_number=num, defaults={'seating_capacity': 4, 'is_active': True})
            table.generate_qr_code()
            table.save()

        self.stdout.write(self.style.SUCCESS("All demo data, categories, and QR tables successfully generated!"))
