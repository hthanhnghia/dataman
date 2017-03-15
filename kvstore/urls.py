from django.conf.urls import url, include
from .views import save_value_for_key

urlpatterns = {
    url(r'^object$', view=save_value_for_key, name="save_value_for_key"),
}