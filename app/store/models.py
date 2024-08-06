from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_at` and `updated_at` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-updated_at']


class Category(BaseModel):
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name_plural = "categories"
        ordering = ['-pk']

    def __str__(self):
        return f"Category {self.name}"


class Product(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category)
    sku = models.CharField(max_length=50, unique=True)

    class Meta(BaseModel.Meta):
        ordering = ['pk']

    def __str__(self):
        return f"Product {self.name}"


class Customer(BaseModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    user = models.OneToOneField(
        User,
        related_name="customer",
        on_delete=models.CASCADE,
    )
    company = models.CharField(max_length=128, null=True, blank=True)
    # Australian phone format
    australian_phone_number_validator = RegexValidator(
        regex=r'^(\+61|0)[2-478](\d{8})$',
        message="Phone number must be in the format: '+614XXXXXXXX' or '0XXXXXXXX'."
    )
    phone_number = models.CharField(
        max_length=12,
        validators=[australian_phone_number_validator]
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)
    last_login_date = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        name = ""
        if self.user.first_name or self.user.last_name:
            name = f" {self.user.first_name} {self.user.last_name}"

        return f"[{self.pk}]{name}"

    class Meta:
        ordering = ['-pk']


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
    ]
    STATE_CHOICES = [
        ('NSW', 'New South Wales'),
        ('VIC', 'Victoria'),
        ('QLD', 'Queensland'),
        ('SA', 'South Australia'),
        ('WA', 'Western Australia'),
        ('TAS', 'Tasmania'),
        ('ACT', 'Australian Capital Territory'),
        ('NT', 'Northern Territory'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    contact_phone_number = models.CharField(
        max_length=12,
        null=True,
        blank=True
    )
    contact_email = models.CharField(max_length=64, blank=True, null=True)
    unit = models.CharField(max_length=32, blank=True, null=True)
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=3, choices=STATE_CHOICES)
    postcode = models.CharField(max_length=4)
    country = models.CharField(max_length=64)
    is_billing = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    is_default = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        is_default = "(default)" if self.is_default else ''
        address_type = 'Billing' if self.is_billing else 'Shipping'
        return f"{self.customer} - {address_type} Address {is_default}"

    def save(self, *args, **kwargs):
        self.validate_is_default()
        super().save(*args, **kwargs)

    def validate_is_default(self):
        # if self.is_default:
        #     self.customer.addresses.update(is_default=False)
        if self.is_default:
            if self.is_billing:
                Address.objects.filter(
                    customer=self.customer, is_billing=True, is_default=True
                ).update(is_default=False)
            else:
                Address.objects.filter(
                    customer=self.customer, is_billing=False, is_default=True
                ).update(is_default=False)



"""
class Cart():

class CartItem():

class Order():

class OrderItem():

class Payment():



"""