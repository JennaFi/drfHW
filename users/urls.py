from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register('users/', UserViewSet)

router.register('users/(?P<pk>\d+)/payments', PaymentViewSet)
urlpatterns = router.urls