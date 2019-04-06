# Shareibc back-end server by Django

# Installation
1. Download [Anaconda](https://www.anaconda.com/distribution/#download-section) and activate virtual environment.
 2. After activated virtual environment, use this command to download and install all necessary file
```
pip install -r requirements.txt
```
# Run Django on local machine
```
python manage.py runserver
```

# Files Structure
## Order
To manage all the orders of the customer
## Product
To manage all the products of the customer
## Project
To manage all the project of the shareibc
## Shareibc
To manage all settings of the shareibc django project
## Static file
To manage all static files of the shareibc django project
## Template
To manage and overide the 'view' (in MVC) of django project

# The Shareibc third party services
Media file: Shareibc project using service from Amazon called S3 to upload and use media file like project and product images. In order to 
upload it to S3 service, Shareibc use [BOTO3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) access and 
upload image to Amazon S3.

Online payment: Shareibc use [Stripe](https://stripe.com) to make online payment. In Django project, Stripe serve as a purpose
of retrieving token on the front-end and to the charge and send back the response to front-end

Email: Shareibc use [Sendgrid](http://sendgrid.com) to send email to customer.

Database: Shareibc use [RDS](https://aws.amazon.com/rds/) as cloud database service from AWS. The database it uses is PostgresSQL.

Authentication: Django provide variety of services to do AuthO2, email authentication.

REST: [Django Rest Framework](https://www.django-rest-framework.org/) to create REST service.

# The Order folder

1. views.py: Manage the 'controller' (in MVC) of order
  ### Function purposes:
  * ```countTotalPrice``` : Take order parameter and loop through all the product and count the total of this order.
  return as int because stripe only accept charge as int. 
  
  * ```change_qty_Product_in_Order```: add/subtract quantity of the product after success charge and save it.
  
  * ```check_stock_product_in_order```: check the availibily/quantity of the product in stock before the charge.
  
  * ```send_email```: send receipt to customer.
  
  * ```OrderCreateAPI.post```: the main function to do the charge for the customer.
  
  * ```OrderAPI.get_queryset```: the controller to send JSON about customer order.
  
2. serializers.py: To serialize the model, data into JSON or API. [Wiki](https://en.wikipedia.org/wiki/Serialization) definition, 
[Serializer in Django Rest Framework](https://www.django-rest-framework.org/tutorial/1-serialization/). Shareibc using nested
serializers to create order. [Example](https://medium.freecodecamp.org/nested-relationships-in-serializers-for-onetoone-fields-in-django-rest-framework-bdb4720d81e6)

  * ```OrderSerializer``` class: use Order model and serialize it. For nested serializer.
  
  * ```OrdersProductSerialer``` class: this class is for checking the orders array on the client side.
  
  * ```DetailsSe``` class: this is nested serializer, this class is for order of the user.
  
  * ```OrderDetailsSerializer``` class:this is nested serializer, this class is for create order.
  
  * ```OrderDetailsSerializer.create``` function: a custom function to create an order.

3. admin.py: To modify the admin panel for Order on admin page.
  
  * ```OrderDetailAdmin.make_delivery``` function: custom admin function to mark the 'status' of the order to delivery.
  
  * ```OrderDetailAdmin.make_refund``` function: custom admin function to mark 'status' of the order to refund.
  
3. urls.py: To modify the order url.

# The Product folder

1. views.py: the 'controller' (in MVC) of product

  * ```ProductCity``` class: the send City API of the product.
  
  * ```ProductAPI``` class: the send Products API of the product. It also make search_fields (from django rest framework) for 
  searching. ordering_fields for ordering product (from django rest framework).
  
  * ```ProductAPI.get_query``` function: to fetch the url query p (https://api.shareibc.com/?p=) to search for city and date.
  
  * ```Images``` class: to send background_image from backend to server. ###this class is deprecated.
  
  * ```ProductDetailsAPI``` class: to send a Product details api to client.
  
2. serializers.py: the 'Product' serializer to send API.
  
  * ```ImageSeriallizer``` class: get all the Product images.

  * ```CitySerializer``` class: get all the Product cities.


  * ```ProductSerializer``` class: get all detail of a Product.


  * ```ProductIndexSerializer``` class: get all the Products.

3. admin.py: admin panel for Product.

  * ```ImageInLine``` class: [TabularInline](https://docs.djangoproject.com/en/2.2/ref/contrib/admin/) class to put the one model
  from different admin field to another related model.
  
4. urls.py: the main urls of the Product

# Project folders

1. views.py: The 'controller' (in MVC) of the Project.

  * ```ProjectsAPIView``` class: to list all the available prjects.
  
  * ```ProjectDetailsAPI``` class: to list all the details of a project.
  
2. serializers.py: the 'Project' sealizer to send API.

  * ```ImageSeriallizer``` class: to get all the images model of projects.
  
  * ```ProjectSerializer``` class: to get all projects include it OneToMany images model.
  
3. admin.py: the admin panel for 'Project'.

  * ```ImageInLine``` class: [TabularInline](https://docs.djangoproject.com/en/2.2/ref/contrib/admin/) class to put the one model
  from different admin field to another related model.
  
# User folder

#### Shareibc use 2 methods to authenticate user: email and social media (Facebook)

1. views.py: the 'controler' (in MVC) of the user.
  
  * ```RegisterAPIView``` class: for registration by email using django default authentication system and
  the User model in (django.contrib.auth)[https://docs.djangoproject.com/en/2.1/ref/contrib/auth/] package.
  
  * ```send_email``` function: for sending email to admin [contact@shareibc.com](contact@shareibc.com) in user support.
  
  * ```AuthVerify``` class: for authentication via http request for front-end. This help front-end to authenticate user.
  
  * ```UserSupport``` class: to fetch the user email, description support and save it to database.
  
  * ```UpdateUser``` class: for authenticated user in front-end to update their User Profile class.
  
2. serializers.py: the API of the User

  * ```UserSupportSerializer``` class: for creating a new data in User Support model to the data.
  
  * ```RegisterSerializer``` class: to register a new user via default Django authentication.
  
  * ```UpdateSerializer``` class to update the new in Django default authentication.
  
3. urls.py: the urls of the user.

  * ```verify_jwt_token``` function: to retrieve JWT token and verify it. If it a valid token, it respone back the same token.
  
  * ```refresh_jwt_token``` function: to refresh JWT token.
  
  * All function above could be find more info in [this](https://getblimp.github.io/django-rest-framework-jwt/).
  

  
  
