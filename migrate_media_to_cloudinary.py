import os
import django
import cloudinary.uploader
from django.conf import settings
from dotenv import load_dotenv

# ✅ Load .env first
load_dotenv()

# ✅ Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")
django.setup()

# ✅ Import Product model dynamically (avoid circular import)
from django.apps import apps
Product = apps.get_model('store', 'Product')

# ✅ Configure Cloudinary manually (ensure .env is read)
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def upload_to_cloudinary():
    count = 0
    for product in Product.objects.all():
        if not product.image:
            continue

        image_path = getattr(product.image, 'path', None)
        if not image_path or not os.path.exists(image_path):
            continue

        print(f"Uploading {image_path} to Cloudinary...")
        try:
            result = cloudinary.uploader.upload(image_path, folder="products/")
            product.image = result['secure_url']
            product.save()
            count += 1
            print(f"✅ Uploaded: {product.name}")
        except Exception as e:
            print(f"❌ Failed: {product.name} — {e}")

    print(f"\nDone! Uploaded {count} files to Cloudinary.")

if __name__ == "__main__":
    upload_to_cloudinary()
