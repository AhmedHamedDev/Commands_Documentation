
class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user

class PostList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    # permission_classes = [IsAdminUser]
    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

##############################################################################################

# *args and **kwargs are special keyword which allows function to take variable length argument.
# *args passes variable number of non-keyworded arguments list and on which operation of the list can be performed.
# **kwargs (key word args) passes variable number of keyword arguments dictionary to function on which operation of a dictionary can be performed.
# *args and **kwargs make the function flexible.

# every model class has a manager: objects
# we use this to run queries against the table
Product.objects.count()

# many methods return a querySet instanse
# a querySet represents a database query
# querySet are lazy. the following does not run any sql
Product.objects.filter(category__name=name)
# this allow chaining of filters
Product.objects.filter(name__contains="k", price__lt=100).exclude(stock_count__gt=5)

# what will cause a querySet to run its sql ?
# - convert to string in template
# - looping
# - convert to list
list(products)

# Lookups
# Allow specifying more complex where clauses with get(), filter(), exclude()
# syntax: field__lookuptype=value
Product.objects.filter(category__name=name)


# Relations
class Category(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField('Product', related_name="categories")

class Product(models.Model):
    name = models.CharField(max_length=100)

c = Category.objects.get(pk=1)
c.products.all() # make an inner join

p = Product.objects.get(pk=1)
p.category_set.all() # in case if we didn't add related_name at ManyToManyField()
p.categories.all() # in case if we did add related_name at ManyToManyField()

# Aggregate and Annotate
Product.objects.aggregate(Avg('price')) # return the avg number
Category.objects.annotate(Avg('products__price')) # return all categories with new proverty contain avg product price

# F(): Referencing Field Values
Product.objects.filter(description__contains=F('name')) # get all products where product description contain product name
Category.objects.get(name="climbing").products.update(price=F('price')*.9)

# Complex Query with Q()
in_stock = Q(stock_count__gt = 0)
no_img = Q(images = None)

Product.objects.filter(in_stock) # products in stock
Product.objects.filter(~in_stock) # products out of stock
Product.objects.filter(no_img | ~in_stock) # products either out of stock or have no image
Product.objects.filter(no_img & ~in_stock) # products match both criteria


###############################################################

def category_View(request, name):
    products = Product.objects.count()
    products = Product.objects.all()
    products = Product.objects.all().distinct()
    products = Product.objects.all()[:5] #add limit 5 to the query
    products = Product.objects.all()[5] #get only one element with index 5
    products = Product.objects.reverse() 
    products = Product.objects.first() 
    products = Product.objects.last() 
    products = Product.objects.order_by("name")
    products = Product.objects.order_by("name").values() #return data after convert each roe to dictionary (object)
    products = Product.objects.order_by("name").values("name", "price") 
    products = Product.objects.order_by("name").values_list("name", "price") #return data after convert each roe to list
    products = Product.objects.filter(category__name=name)
    products = Product.objects.filter(name__endwith="k")
    products = Product.objects.filter(name__icontains="k") # icontains mean insenstive contains
    products = Product.objects.filter(name__contains="k", price__lt=100).exclude(stock_count__gt=5)
    products = Product.objects.get(pk=5) # return single value
    products = Product.objects.get(id=5) # return single value
    products = Product.objects.get(name__contains="a") # raise error if there is more than one value or no values
    users = UserProfile.objects.select_related('user__user_questions').values().annotate(name=F('user__username'), id=F('user__id'), questions=F('user__user_questions__id')).values()


####################################################################################
# Customizing Model Behaviour

# 1- Model Meta Class
    class Product(models.Model):
        name = models.CharField(max_length=100)

        class Meta:
            ordering = ['-price'] # all queries will return with order by price desinding
            verbose_name_plural = "Products" # will display in admin panal with that name
            db_table = "Products" # configure table name in database
            constraints = [
                models.CheckConstraint(check=models.Q(price__gte=0), name="price_not_negative")
            ]

# 2- Custom Methods

    class Product(models.Model):
        name = models.CharField(max_length=100)
        slug = models.SlugField() # short text used for the url

        @property
        def vat(self):
            return Decimal(.2) * self.price

        # for any product this function will return the url for the page of that product (link will appear in admin)
        def get_absolute_url(self):
            return reverse("store:product-detail", kwargs={'pk':self.id})
            # <a href="{{ p.get_absolute_url }}" />

        def __str__(self):
            return self.name

        def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.name)
            return super().save(*args, **kwargs)

# 3- Custom Manager

    class ProductInStockQuerySet(models.QuerySet):
        def in_stock(self):
            return self.filter(stock_count__gt=0)

    class Product(models.Model):
        name = models.CharField(max_length=100)

        # use this instead of objects so u will get the filter all the time
        in_stock = ProductInStockQuerySet.as_manager()


# 4- Custom Manager

    ## often, you will just want to use the parent class to hold information that you don't want
    ## to have to type out for each child model. this class isn't going to ever be used in
    ## isolation, so Abstract base classes are what you're after

    class TimeStampedModel(models.Model):
        created = AutoCreatedField(_('created'))
        modified = AutoLastModifiedField(_('modified'))

        def save(self, *args, **kwargs):
            update_fields = kwargs.get('update_fields', None)
            if update_fields:
                kwargs['update_fields'] = set(update_fields).union({'modified'})

            super().save(*args, **kwargs)
        
        class Meta:
            abstract = True

    ## if you're subclassing an existing model (perhaps something from another application entirely)
    ## and want each model to have its own  database table, Multi-table inheritance is the way to go
    ## next example will create three tables two of them will have product forign key

    class Product(models.Model):
        name = models.CharField(max_length=100)

    class DigitalProduct(Product):
        file = models.FileField()

    class PhysicalProduct(Product):
        stock_count = models.IntegerField(help_text="how many items are currently in stock")

    ## finally, if you only want to modify the python-level behavior of a model, without changing the models
    ## fields in any way, you can use Proxy models

    class Product(models.Model):
        name = models.CharField(max_length=100)

    # this class will still represent the same database table
    class OrderedPerson(Person):
        class Meta:
            ordering = ["name"]
            proxy = True

    ## now normal Person queries will be unorderd and OrderedPerson queries will be orderd by name

#####################################################################################################

# migration comands

    ## python manage.py showmigrations : show all migrations sorted by apps
    ## python manage.py sqlmigrate <app-name> <migration-number> : show generated sql for this migration
    ## python manage.py makemigrations
    ## python manage.py migrate 
    ## python manage.py migrate --fake : Mark migrations as run without actually run them
    ## python manage.py migrate store 005 : migrate back to 005
    ## python manage.py migrate store zero : migrate to initial state (remove every thing)

# migration file 

    ## dependencies : name of the migration that this migration depend on
    dependencies = [
        ('store', '0001_initial')
    ]

    ## operations
    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('excerpt', models.TextField(null=True)),
                ('content', models.TextField()),
                ('slug', models.SlugField(max_length=250, unique_for_date='published')),
                ('published', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='blog.category')),
            ],
            options={
                'ordering': ('-published',),
            },
        ),
    ]


# Merging Migrations

    ## python manage.py makemigrations --merge
    ## when me and my team mate make migration and we have to files with the same number
    ## will generate new migration file with dependancies contains both files and empty operations

# Squashing Migrations

    ## python manage.py squashmigrations store 0008
    ## when you have many migrations files and want to compine them at one
    ## this one will contain a replace section contains all migration names that it replaces

# Custom Migration

    ## python manage.py makemigrations --empty store

    def slugify_product_titles(apps, schema_editor):
        Product = apps.get_model("store", "Product")

        for p in Product.objects.filter(slug=""):
            p.slug = slugify(p.name)
            p.save()
    
    def undo_slugify(apps, schema_editor):
        pass
    
    class Migration(migrations.Migration):

        dependencies = [
            ('store', '0006_auto-4324523'),
        ]

        operations = [
            migrations.RunPython(slugify_product_titles, reverse_code=undo_slugify)
        ]

#################################################################################################

# optimizing the orm

    ## Django Debug Toolbar: Great tool to monitor queries

    ## Reducing the number of queries
        ProductImage.objects.select_related('product').get(pk=1) # its like include in EF
        Product.objects.filter(name__contains=name).prefetch_related('images') # for many to many

    ## Raw SQL
        Product.objects.raw('SELECT * from store-product where price < %s', [100])

    ## Transactions : Add ATOMIC_REQUESTS: True to DATABASES Section at settings or wrap it with your self

###################################################################################################


# signal a function to fire before save

# A slug is a human-readable, unique identifier, used to identify a resource instead of a less human-readable identifier like an id .
# instead of id in the url

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


####################################################################################################

def returnNewString():
    variavle1 = "ahmed"
    variavle2 = "hamed"
    return "%s - %s" %(variavle1, variavle2)


####################################################################################################

