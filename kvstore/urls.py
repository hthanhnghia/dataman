from django.conf.urls import url, include
from .views import save_value_for_key, get_value_by_key

urlpatterns = {
    url(r'^object$', view=save_value_for_key, name="save_value_for_key"),
    url(r'^object/(?P<key>.+)$', view=get_value_by_key, name="get_value_by_key"),
}