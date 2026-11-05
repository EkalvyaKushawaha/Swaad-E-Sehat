from io import BytesIO
from django.db import models
from django.core.files import File

class CafeTable(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    seating_capacity = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def generate_qr_code(self, base_url='http://127.0.0.1:8000'):
        try:
            import qrcode
            qr = qrcode.QRCode(box_size=8, border=3)
            qr.add_data(f"{base_url}/tables/{self.table_number}/")
            qr.make(fit=True)
            img = qr.make_image(fill_color="#1b4332", back_color="white")
            buf = BytesIO()
            img.save(buf, format='PNG')
            self.qr_code.save(f"table_{self.table_number}.png", File(buf), save=False)
        except Exception:
            pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()
            super().save(update_fields=['qr_code'])
