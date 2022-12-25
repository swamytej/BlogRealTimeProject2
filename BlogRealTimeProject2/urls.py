"""BlogRealTimeProject2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from BlogApp2 import views
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
      path('admin/', admin.site.urls),
      path('accounts/', include('django.contrib.auth.urls')),
      path('post/', views.postview, name='post'),
      path('logout/', views.logout_view),
      path('<year>/<month>/<day>/<post>/', views.post_detailview, name='post_detail'),
      path('<id>/share/', views.mailsendview),
      path('signup/', views.signupview),
      path('thank/', views.thankyou1),
      path('comment/', views.commentview.as_view()),
      path('update/<pk>', views.postupdateview.as_view(), name='update'),
      path('<pk>/userupdate/', views.profileupdate, name='upedit'),
      path('delete/<pk>', views.commentdelete.as_view(), name='delete'),
      path('delete1/<pk>', views.Postdeleteview.as_view(), name='delete'),
      path('succ/', views.postsuccview, name='succ'),
      path('profile/', views.profileview),
      path('succ/', views.commentdelsucc, name='succ'),
      path('contact/', views.contactview),
      path('home/', views.home_page),
      path('tag/', views.post_list_view),
      path('<tag_slug>/comment/', views.post_list_view, name='post_list_by_tag_name'),

      # path('postlist/',views.postview),

      re_path('^.*$', views.home_page),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

