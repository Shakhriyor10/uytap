from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="Пользователь")
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to="profiles/avatars/", blank=True, null=True, verbose_name="Аватар")
    is_host = models.BooleanField(default=False, verbose_name="Является хозяином")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name="Рейтинг")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль: {self.user.username}"


class Listing(models.Model):
    PROPERTY_TYPES = [
        ("apartment", "Квартира"),
        ("house", "Дом"),
        ("room", "Комната"),
        ("villa", "Вилла"),
        ("other", "Другое"),
    ]

    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", verbose_name="Хозяин")
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    city = models.CharField(max_length=128, verbose_name="Город")
    address = models.CharField(max_length=512, blank=True, verbose_name="Адрес")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Широта")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Долгота")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за день")
    max_guests = models.PositiveSmallIntegerField(default=1, verbose_name="Макс. гостей")
    rooms = models.PositiveSmallIntegerField(default=1, verbose_name="Комнат")
    beds = models.PositiveSmallIntegerField(default=1, verbose_name="Кроватей")
    baths = models.DecimalField(max_digits=4, decimal_places=1, default=1.0, verbose_name="Санузлов")
    property_type = models.CharField(max_length=32, choices=PROPERTY_TYPES, default="apartment", verbose_name="Тип недвижимости")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["city", "price_per_day"])]
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return f"{self.title} — {self.city}"

    def get_main_image(self):
        return self.images.filter(is_cover=True).first() or self.images.first()


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images", verbose_name="Объявление")
    image = models.ImageField(upload_to="listings/images/", verbose_name="Фото")
    caption = models.CharField(max_length=255, blank=True, verbose_name="Описание изображения")
    is_cover = models.BooleanField(default=False, verbose_name="Главное фото")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Загружено")

    class Meta:
        verbose_name = "Фото объявления"
        verbose_name_plural = "Фото объявлений"

    def __str__(self):
        return f"Фото {self.listing.title} ({'обложка' if self.is_cover else 'фото'})"


class Availability(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="availability", verbose_name="Объявление")
    date = models.DateField(verbose_name="Дата")
    is_available = models.BooleanField(default=True, verbose_name="Доступно")

    class Meta:
        unique_together = ("listing", "date")
        ordering = ["date"]
        verbose_name = "Доступность"
        verbose_name_plural = "Доступность"

    def __str__(self):
        return f"{self.listing.title} — {self.date} — {'OK' if self.is_available else 'Занято'}"


class Booking(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Ожидает"),
        (STATUS_CONFIRMED, "Подтверждено"),
        (STATUS_CANCELLED, "Отменено"),
        (STATUS_COMPLETED, "Завершено"),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings", verbose_name="Объявление")
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", verbose_name="Гость")
    check_in = models.DateField(verbose_name="Дата заезда")
    check_out = models.DateField(verbose_name="Дата выезда")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Итоговая цена")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Бронь {self.id} — {self.listing.title} — {self.guest.username}"

    def nights(self):
        return (self.check_out - self.check_in).days


class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews", verbose_name="Объявление")
    guest = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviews", verbose_name="Гость")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка")  # 1..5
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв {self.rating} — {self.listing.title}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist", verbose_name="Пользователь")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="wishlisted_by", verbose_name="Объявление")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        unique_together = ("user", "listing")
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.user.username} ❤️ {self.listing.title}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("card", "Карта"),
        ("paypal", "PayPal"),
        ("manual", "Наличные"),
    ]

    PAYMENT_STATUS = [
        ("created", "Создано"),
        ("paid", "Оплачено"),
        ("failed", "Ошибка"),
        ("refunded", "Возвращено"),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment", verbose_name="Бронирование")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")

class Payment(models.Model):
    PAYMENT_METHODS = [
        ("card", "Карта"),
        ("paypal", "PayPal"),
        ("manual", "Наличные"),
    ]

    PAYMENT_STATUS = [
        ("created", "Создано"),
        ("paid", "Оплачено"),
        ("failed", "Ошибка"),
        ("refunded", "Возвращено"),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="payment", verbose_name="Бронирование")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    method = models.CharField(max_length=16, choices=PAYMENT_METHODS, default="card", verbose_name="Метод оплаты")
    status = models.CharField(max_length=16, choices=PAYMENT_STATUS, default="created", verbose_name="Статус оплаты")
    transaction_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID транзакции")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"Оплата {self.amount} — бронь {self.booking.id}"
