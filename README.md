
# Django REST Framework

## Important Topics

- AppConfig
- Django ORM
  - .get()
    - throws `DoesNotExist` exception if no object found
    - throws `MultipleObjectsReturned` exception if more than one object found
    - throws `FieldError` exception if more than one object found
  - .filter()
    - returns empty QuerySet if no object found
    - returns QuerySet if one or more objects found
    - can be used to check if exists or not
    - update multiple objects
    - delete multiple objects
- Server-side Rendering
  - Django Templates
    - collectstatic : collect all static files from all apps and put them in a single folder
    - static : to access static files
    - STATIC_ROOT : where to collect static files
    - STATICFILES_DIRS : where to look for static files
  - Forms
    - fields
    - widgets
    - validators
    - CSRF
- DRF (Django Rest Framework)
  - Serializers
    - ModelSerializer
    - HyperlinkedModelSerializer
    - Serializer Context Object
    - SerializerMethod Object
  - Salted Password Hashing
  - Token Authentication
  - Image Validators
  - APIView
    - Class based views
    - Function based views
  - GenericAPIView
  - Mixins
    - CreateModelMixin
    - ListModelMixin
    - RetrieveModelMixin
    - UpdateModelMixin
    - DestroyModelMixin
  - Pagination
    - LimitOffsetPagination
    - PageNumberPagination
  - ViewSets : urls get configured automatically but methods needs to be defined
    - GenericViewSet (Mixins can be used) : urls and methods are configured automatically using mixins.
    - ModelViewSet : urls and methods are configured automatically.
    - Routers
    - Nested Routers
    - Dynamic Routers
  - Object Level Permissions
  - View Level Permissions
  - Celery
    - Django Celery Beat (stores schedule in database)
    - Django Celery Results (stores results in database)
    - Django Celery Email (sends emails)
    - Django Celery Admin (admin interface)
    - Django Celery Flower (monitoring)
    - Django Celery Progress (monitoring)
    - Django Celery Cam (monitoring)
    - Django Celery Once (prevents duplicate tasks)
  - Signals
    - pre_save
    - post_save
    - pre_delete
    - post_delete
  - Middleware
    - Called during request :
      - process_request
      - process_view
    - Called during response :
      - process_template_response
      - process_response
      - process_exception
  - 


## Frontend :

Commands used to setup React : 

npx create-react-app frontend
npm i @material-ui/core
yarn add @material-ui/core