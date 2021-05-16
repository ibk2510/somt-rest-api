from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r'consumers', views.ConsumerViewset)
router.register(r'users/subscriptions', views.SubscriptionViewset)
# router.register(r'users/login', views.UserLoginView)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/',views.UserLoginView.as_view()),
    url(r'^signup/', views.UserRegistrationView.as_view()),
    url(r'view/' , views.UserProfileView.as_view()),
    # path('consumer-details/' , views.consumer_details),

]
