import uuid
from django.db import models
from django.utils.text import slugify

from core.models import User


# ================= SELLER =================
class SellerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField("core.User", on_delete=models.CASCADE, related_name="seller_profile")
    store_name = models.CharField(max_length=255)
    store_slug = models.SlugField(unique=True)
    gst_number = models.CharField(max_length=50)
    pan_number = models.CharField(max_length=50)
    bank_account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    business_address = models.TextField()
    rating = models.FloatField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.store_name:
            return self.store_name
        return self.user.username

    def __str__(self):
        return self.store_name



# ================= PRODUCT =================
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    seller = models.ForeignKey(
        "seller.SellerProfile",
        on_delete=models.CASCADE,
        related_name="products"
    )

    subcategory = models.ForeignKey(
        "core.SubCategory",
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)

    approval_status = models.CharField(
        max_length=20,
        choices=(
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected')
        ),
        default='PENDING'
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Auto slug
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    # ✅ Get display price from variants
    def get_price(self):
        return self.variants.aggregate(
            Min('selling_price')
        )['selling_price__min']

    def __str__(self):
        return self.name


# ================= PRODUCT VARIANT =================
class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    slug = models.SlugField(unique=True, blank=True)
    sku_code = models.CharField(max_length=100, unique=True)

    # ✅ Use Decimal for money
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)

    stock_quantity = models.IntegerField(default=0)

    # Optional dimensions
    weight = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    tax_percentage = models.FloatField(default=0)

    is_cancellable = models.BooleanField(default=True)
    is_returnable = models.BooleanField(default=True)
    return_days = models.IntegerField(default=7)

    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Auto slug
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.sku_code)
            slug = base_slug
            counter = 1

            while ProductVariant.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.sku_code


# ================= PRODUCT IMAGE =================
class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="productimages/")

    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional description"
    )

    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_primary", "-created_at"]

    # ✅ Ensure only one primary image
    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)

        # ✅ Auto-set primary if none exists
        if not ProductImage.objects.filter(product=self.product, is_primary=True).exists():
            self.is_primary = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} Image"


# ================= ATTRIBUTES =================
class Attribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AttributeOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="options")
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name} - {self.value}"


class VariantAttributeBridge(models.Model):
    variant = models.ForeignKey("seller.ProductVariant", on_delete=models.CASCADE)
    option = models.ForeignKey(AttributeOption, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.variant.sku_code} - {self.option}"

    def __str__(self):
        return f"{self.variant.sku_code} - {self.option.value}"


# ================= INVENTORY =================
class InventoryLog(models.Model):
    variant = models.ForeignKey("seller.ProductVariant", on_delete=models.CASCADE)
    change_amount = models.IntegerField()
    reason = models.CharField(max_length=50)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.variant.sku_code} ({self.change_amount})"