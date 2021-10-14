from django.db import models
from store.models import Category
from django.urls import reverse

class Popular_Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='photos/products')
    image_havor = models.ImageField(upload_to='photos/products-havor')
    stock = models.IntegerField()
    new = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    

    date_joined_for_format = models.DateTimeField(auto_now_add=True)
    last_login_for_format = models.DateTimeField(auto_now=True)
    def created(self):
        return self.date_joined_for_format.strftime('%B %d %Y')
    def updated(self):
        return self.last_login_for_format.strftime('%B %d %Y')

    def __str__(self):
        return self.name
    
    #def averageRating(self):
    #    reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
    #    avg = 0
    #    if reviews['average'] is not None:
    #        avg = float(reviews['average'])
    #    return avg
    #
    #def countReview(self):
    #    reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
    #    count = 0
    #    if reviews['count'] is not None:
    #        count = int(reviews['count'])
    #    return count
#
    def get_prodcut_details_url(self):
        return reverse('store:product_details', args=[self.category.slug, self.slug])
    
    #class Meta:
    #    verbose_name_plural = 'Products'
    #    ordering = ('-date_joined_for_format',)
    


class For_You(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='photos/products')
    image_havor = models.ImageField(upload_to='photos/products-havor')
    stock = models.IntegerField()
    new = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    date_joined_for_format = models.DateTimeField(auto_now_add=True)
    last_login_for_format = models.DateTimeField(auto_now=True)
    def created(self):
        return self.date_joined_for_format.strftime('%B %d %Y')
    def updated(self):
        return self.last_login_for_format.strftime('%B %d %Y')

    def __str__(self):
        return self.name
    
    #def averageRating(self):
    #    reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
    #    avg = 0
    #    if reviews['average'] is not None:
    #        avg = float(reviews['average'])
    #    return avg
    #
    #def countReview(self):
    #    reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
    #    count = 0
    #    if reviews['count'] is not None:
    #        count = int(reviews['count'])
    #    return count
#
    def get_prodcut_details_url(self):
        return reverse('store:product_details', args=[self.category.slug, self.slug])
    
    #class Meta:
    #    verbose_name_plural = 'Products'
    #    ordering = ('-date_joined_for_format',)
    

