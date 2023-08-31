from django.db import models


def get_category_image_path(instance: 'ProductImage', filename: str) -> str:
    return f"categories/images/category_{instance.product.pk}/{filename}"


class CategoryImage(models.Model):
    """Product category image model"""

    default_path = "categories/images/default.png"

    src = models.ImageField(
        upload_to=get_category_image_path,
        verbose_name='Ссылка',
    )

    @property
    def alt(self):
        """Get alt for category image"""

        if self.src == self.default_path:
            return 'Default category image'
        return f"{self.category.get().name} image: {self.src.url.split('/')[-1]}"

    @classmethod
    def get_default_pk(cls):
        """Get pk for default category image"""

        image, _ = cls.objects.get_or_create(src=cls.default_path)
        return image.pk

    def __str__(self):
        return f"{self.__class__.__name__}" \
               f"(category={self.category.get().name})"


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

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name})"
