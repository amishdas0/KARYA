from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.update_profile, name='profile'),
    path('friends/', views.find_profile, name='friends'),
    path('friends_overview', views.my_following_followers, name='friends_overview'),
    path('add_friend/<int:profile_id>/', views.follow_profile, name='add_friend')
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
