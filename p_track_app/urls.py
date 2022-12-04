from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Category path
    path('create-category/', views.create_category, name = 'create-category'),
    path('view-category/<str:pk>/', views.view_category, name = 'view-category'),
    path('update-category/<str:pk>/', views.update_category, name = 'update-category'),
    path('delete-category/<str:pk>/', views.delete_category, name = 'delete-category'),

    # Notes path
    path('create-note/<str:pk>', views.create_note, name = 'create-note'),
    path('view-note/<str:pk>/', views.view_note, name = 'view-note'),
    path('update-note/<str:pk>/', views.update_note, name = 'update-note'),
    path('delete-note/<str:pk>/', views.delete_note, name = 'delete-note'),

    # login and register urls.
    path("login/", views.login_user , name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),

    # Email Verification
    path('verify-email/', views.verify_email, name='verify-email'),
    path('verify/', views.verify, name='verify'),
]
