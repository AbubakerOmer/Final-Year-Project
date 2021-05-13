from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


from chat.views import ThreadView,get_All_Users

urlpatterns = [
    path('',get_All_Users,name="get_All_Users"),
    path('<str:username>/', ThreadView.as_view()),


]
# if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
