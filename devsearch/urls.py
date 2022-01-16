from django.contrib import admin
from django.urls import path, include

from django.conf import settings  # import settings.py file to connect MEDIA_ROOT and MEDIA_URL
from django.conf.urls.static import static  # static basically going to help us create a new URL for our static files

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('', include('users.urls')),
    path('api/', include('api.urls')),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='users/reset_password.html'), name='password_reset'),  # PasswordResetView: auth class name for reset password. name: we can use by our own name value. template_name='users/reset_password.html': we can also place the template into apps template directory
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # grab the MEDIA_URL and connected it to MEDIA_ROOT.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # grab the STATIC_URL and connected it to STATIC_ROOT.
