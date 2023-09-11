from django.db import models


class CategoryImage(models.Model):
    """Product category image model"""

    default_path = "categories/images/default.png"

    src = models.ImageField(
        upload_to='categories/images/',
        verbose_name='Ссылка',
    )

    @property
    def alt(self) -> str:
        """Get alt for category image"""

        if self.src == self.default_path or not self.category.all():
            return 'Default category image'
        return f"{self.category.get().title} image: {self.src.url.split('/')[-1]}"

    @classmethod
    def get_default_pk(cls) -> int:
        """Get pk for default category image"""

        image, _ = cls.objects.get_or_create(src=cls.default_path)
        return image.pk

    def __str__(self) -> str:
        return self.alt


class Category(models.Model):
    """Product category model"""

    title = models.CharField(
        max_length=100,
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(
        CategoryImage,
        related_name='category',
        on_delete=models.CASCADE,
        verbose_name='Изображение',
        default=CategoryImage.get_default_pk,
    )

    def __str__(self) -> str:
        return self.title
