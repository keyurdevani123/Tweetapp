from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Tweet-related paths
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),
    path('<int:tweet_id>/view/', views.tweet_view, name='tweet_view'),
    path('<int:tweet_id>/comments/', views.tweet_comments, name='tweet_comments'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),

    # User-related paths
    path('register/', views.register, name='register'),
    path('user_search/', views.user_search, name='user_search'),
    path('user/details/<int:user_id>/', views.user_details, name='user_details'),
    path('<int:user_id>/user_tweets/', views.user_tweets, name='user_tweets'),  # ✅ Corrected

    # Follow/Unfollow functionality
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('<int:user_id>/followers/', views.followers_list, name='followers_list'),
    path('<int:user_id>/following/', views.following_list, name='following_list'),
    path('<int:follower_id>/remove_follower/', views.remove_follower, name='remove_follower'),
    path('<int:following_id>/unfollow_user/', views.unfollow_user, name='unfollow_user'),

    # Notifications
    path("notifications/", views.notifications_page, name="notifications_page"),
    path("notifications/get/", views.get_notifications, name="get_notifications"),
    path('notifications/mark_all_read/<int:notification_id>/', views.mark_all_notifications_as_read, name="mark_all_notifications_as_read"),

    # Messages
    path('messages/', views.messages_page, name='messages_page'),
    path('messages/<int:recipient_id>/', views.get_messages, name='get_messages'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
