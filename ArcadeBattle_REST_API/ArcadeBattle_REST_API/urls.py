"""ArcadeBattle_REST_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.urls import reverse
from rest_framework import routers
from app import views

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login', views.login),
    path('logout', views.logout),

    path('all_people', views.get_all_people),
    path('all_admins', views.get_all_admins),
    path('all_doctors', views.get_all_doctors),
    path('all_patients', views.get_all_patients),
    path('all_games', views.get_all_games),
    path('my_profile', views.get_my_profile),


    url('^profile/(?P<username>.+)', views.get_profile),
    url('^game_max_score/(?P<game_name>.+)', views.get_game_max_score),
    url('^gesture_max_score/(?P<username>.+)/(?P<gesture_name>.+)', views.get_gesture_max_score),
    url('^gestures/(?P<username>.+)', views.get_gestures),
    url('^game_gestures/(?P<username>.+)', views.get_game_gestures),

    url('^delete_user/(?P<username>.+)', views.delete_user),
    url('^delete_gesture/(?P<username>.+)/(?P<gesture_name>.+)', views.delete_gesture),

    #POST
    path('new_user', views.new_user),
    path('update_notes', views.update_notes),
    path('new_game', views.new_game),
    path('update_profile', views.update_profile),
    path('add_game_played', views.add_game_played),

    path('games_played', views.get_games_played),
    path('gestures_used', views.get_gestures_used),
    path('reload_database', views.reload_database),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
