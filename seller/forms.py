from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage, ProductVariant, SellerProfile, AttributeOption


input_classes = (
    "w-full rounded-xl border border-gray-300 py-3.5 px-5 "
    "focus:ring-primary focus:border-black focus:bg-white "
    "outline-none transition-all duration-200"
)


# ================= PRODUCT FORM =================
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "brand",
            "model_number",
            "subcategory",
            "description",
            "is_active",   # ❌ removed approval_status (admin only)
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": input_classes}),
            "brand": forms.TextInput(attrs={"class": input_classes}),
            "model_number": forms.TextInput(attrs={"class": input_classes}),
            "subcategory": forms.Select(attrs={"class": input_classes}),
            "description": forms.Textarea(attrs={"class": input_classes, "rows": 4}),
            "is_active": forms.CheckboxInput(attrs={"class": "mr-2"}),
        }


# ================= VARIANT FORM =================
class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = [
            "sku_code",
            "mrp",
            "selling_price",
            "cost_price",
            "stock_quantity",
            "weight",
            "length",
            "width",
            "height",
            "tax_percentage",
            "is_cancellable",
            "is_returnable",
            "return_days",
        ]

        widgets = {
            "sku_code": forms.TextInput(attrs={"class": input_classes}),

            "mrp": forms.NumberInput(attrs={"class": input_classes}),
            "selling_price": forms.NumberInput(attrs={"class": input_classes}),
            "cost_price": forms.NumberInput(attrs={"class": input_classes}),
            "stock_quantity": forms.NumberInput(attrs={"class": input_classes}),

            "weight": forms.NumberInput(attrs={"class": input_classes}),
            "length": forms.NumberInput(attrs={"class": input_classes}),
            "width": forms.NumberInput(attrs={"class": input_classes}),
            "height": forms.NumberInput(attrs={"class": input_classes}),

            "tax_percentage": forms.NumberInput(attrs={"class": input_classes}),
            "return_days": forms.NumberInput(attrs={"class": input_classes}),

            "is_cancellable": forms.CheckboxInput(),
            "is_returnable": forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        sp = cleaned_data.get("selling_price")
        mrp = cleaned_data.get("mrp")

        if sp and mrp and sp > mrp:
            raise forms.ValidationError("Selling price cannot exceed MRP")

        return cleaned_data


# ✅ FORMSET FOR VARIANTS
VariantFormSet = inlineformset_factory(
    Product,
    ProductVariant,
    form=ProductVariantForm,
    extra=1,
    can_delete=True
)


# ================= PRODUCT IMAGE FORM =================
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image", "alt_text", "is_primary"]

        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": input_classes}),
            "alt_text": forms.TextInput(
                attrs={"class": input_classes, "placeholder": "Optional description"}
            ),
            "is_primary": forms.CheckboxInput(),
        }


# ✅ IMAGE FORMSET
ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=4,
    max_num=4,
    validate_max=True,
    can_delete=True
)


# ================= ATTRIBUTE OPTION FORM =================
class AttributeOptionForm(forms.Form):
    options = forms.ModelMultipleChoiceField(
        queryset=AttributeOption.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


# ================= SELLER PROFILE FORM =================
class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = [
            "store_name",
            "store_slug",
            "gst_number",
            "pan_number",
            "bank_account_number",
            "ifsc_code",
            "business_address"
        ]

        widgets = {
            field: forms.TextInput(attrs={"class": input_classes})
            for field in [
                "store_name",
                "store_slug",
                "gst_number",
                "pan_number",
                "bank_account_number",
                "ifsc_code"
            ]
        }

        widgets["business_address"] = forms.Textarea(attrs={"class": input_classes})

    def clean_ifsc_code(self):
        ifsc = self.cleaned_data.get("ifsc_code")
        if ifsc and len(ifsc) < 8:
            raise forms.ValidationError("Invalid IFSC code")
        return ifsc