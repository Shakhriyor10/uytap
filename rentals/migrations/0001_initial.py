from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=128, unique=True, verbose_name="Город")),
            ],
            options={
                "ordering": ["name"],
                "verbose_name": "Город",
                "verbose_name_plural": "Города",
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(blank=True, max_length=32, null=True, verbose_name="Телефон")),
                ("avatar", models.ImageField(blank=True, null=True, upload_to="profiles/avatars/", verbose_name="Аватар")),
                ("is_host", models.BooleanField(default=False, verbose_name="Является хозяином")),
                ("rating", models.DecimalField(decimal_places=2, default=0.00, max_digits=3, verbose_name="Рейтинг")),
                ("date_of_birth", models.DateField(blank=True, null=True, verbose_name="Дата рождения")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Профиль",
                "verbose_name_plural": "Профили",
            },
        ),
        migrations.CreateModel(
            name="Listing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("address", models.CharField(blank=True, max_length=512, verbose_name="Адрес")),
                ("latitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name="Широта")),
                ("longitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name="Долгота")),
                ("price_per_day", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Цена за день")),
                (
                    "max_guests",
                    models.PositiveSmallIntegerField(default=1, verbose_name="Макс. гостей"),
                ),
                ("rooms", models.PositiveSmallIntegerField(default=1, verbose_name="Комнат")),
                ("beds", models.PositiveSmallIntegerField(default=1, verbose_name="Кроватей")),
                (
                    "baths",
                    models.DecimalField(decimal_places=1, default=1.0, max_digits=4, verbose_name="Санузлов"),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("apartment", "Квартира"),
                            ("house", "Дом"),
                            ("room", "Комната"),
                            ("villa", "Вилла"),
                            ("other", "Другое"),
                        ],
                        default="apartment",
                        max_length=32,
                        verbose_name="Тип недвижимости",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активно"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="listings",
                        to="rentals.city",
                        verbose_name="Город",
                    ),
                ),
                (
                    "host",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="listings",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Хозяин",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Объявление",
                "verbose_name_plural": "Объявления",
            },
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("check_in", models.DateField(verbose_name="Дата заезда")),
                ("check_out", models.DateField(verbose_name="Дата выезда")),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Итоговая цена")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Ожидает"),
                            ("confirmed", "Подтверждено"),
                            ("cancelled", "Отменено"),
                            ("completed", "Завершено"),
                        ],
                        default="pending",
                        max_length=16,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
                (
                    "guest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Гость",
                    ),
                ),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="rentals.listing",
                        verbose_name="Объявление",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Бронирование",
                "verbose_name_plural": "Бронирования",
            },
        ),
        migrations.CreateModel(
            name="ListingImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="listings/images/", verbose_name="Фото")),
                ("caption", models.CharField(blank=True, max_length=255, verbose_name="Описание изображения")),
                (
                    "is_cover",
                    models.BooleanField(default=False, verbose_name="Главное фото"),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Загружено"),
                ),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="rentals.listing",
                        verbose_name="Объявление",
                    ),
                ),
            ],
            options={
                "verbose_name": "Фото объявления",
                "verbose_name_plural": "Фото объявлений",
            },
        ),
        migrations.CreateModel(
            name="Availability",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="Дата")),
                (
                    "is_available",
                    models.BooleanField(default=True, verbose_name="Доступно"),
                ),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="availability",
                        to="rentals.listing",
                        verbose_name="Объявление",
                    ),
                ),
            ],
            options={
                "ordering": ["date"],
                "verbose_name": "Доступность",
                "verbose_name_plural": "Доступность",
                "unique_together": {("listing", "date")},
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Сумма")),
                (
                    "method",
                    models.CharField(
                        choices=[("card", "Карта"), ("paypal", "PayPal"), ("manual", "Наличные")],
                        default="card",
                        max_length=16,
                        verbose_name="Метод оплаты",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("created", "Создано"),
                            ("paid", "Оплачено"),
                            ("failed", "Ошибка"),
                            ("refunded", "Возвращено"),
                        ],
                        default="created",
                        max_length=16,
                        verbose_name="Статус оплаты",
                    ),
                ),
                (
                    "transaction_id",
                    models.CharField(blank=True, max_length=255, null=True, verbose_name="ID транзакции"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
                (
                    "booking",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment",
                        to="rentals.booking",
                        verbose_name="Бронирование",
                    ),
                ),
            ],
            options={
                "verbose_name": "Оплата",
                "verbose_name_plural": "Оплаты",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(verbose_name="Оценка")),
                ("comment", models.TextField(blank=True, verbose_name="Комментарий")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "guest",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Гость",
                    ),
                ),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="rentals.listing",
                        verbose_name="Объявление",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
            },
        ),
        migrations.CreateModel(
            name="Wishlist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlisted_by",
                        to="rentals.listing",
                        verbose_name="Объявление",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlist",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Избранное",
                "verbose_name_plural": "Избранное",
                "unique_together": {("user", "listing")},
            },
        ),
        migrations.AddIndex(
            model_name="listing",
            index=models.Index(fields=["city", "price_per_day"], name="rentals_li_city_pr_69c4c5_idx"),
        ),
    ]
