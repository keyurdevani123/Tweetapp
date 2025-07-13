from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet, Like, Comment, CustomUser, Notification, Message
from .forms import TweetForm, UserRegistrationForm, CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model
from django.http import JsonResponse
from django.db.models import Q, Subquery, OuterRef

User = get_user_model()

# Create your views here.

def index(request):
    return render(request, 'index.html')

def user_tweets(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')  # Get the tweets
    tweet_count = tweets.count()  # Count the tweets
    return render(request, 'user_tweets.html', {
        'tweets': tweets,
        'user': user,
        'tweet_count': tweet_count,  # Pass tweet count to the template
    })

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
   # Check if the user is authenticated
    if request.user.is_authenticated:
        for tweet in tweets:
            tweet.liked_by_user = tweet.likes.filter(user=request.user).exists()
    else:
        # If the user is not authenticated, set liked_by_user to False
        for tweet in tweets:
            tweet.liked_by_user = False
    return render(request, 'tweet_list.html', {'tweets': tweets, 'user': request.user})

@csrf_exempt
@login_required
def like_tweet(request, tweet_id):
    if not request.user.is_authenticated:
        return redirect('login')
    tweet = get_object_or_404(Tweet, id=tweet_id)
    user = request.user

    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        if tweet.user != user:
            Notification.objects.create(user=tweet.user,sender=user,notification_type='like',message=f"{user.username} liked your tweet.",related_tweet=tweet)

    return JsonResponse({
        'liked': liked,
        'likes_count': tweet.likes_count
    })


@login_required
def tweet_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    tweet.views += 1
    tweet.save()

    comments = tweet.comments.all()
    comment_form = CommentForm()

    return render(request, 'tweet_view.html', {
        'tweet': tweet,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def tweet_comments(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    comments = Comment.objects.filter(tweet=tweet).order_by('-created_at')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tweet = tweet
            comment.save()
            return redirect('tweet_comments', tweet_id=tweet.id)
    else:
        form = CommentForm()

    return render(request, 'comments.html', {
        'tweet': tweet,
        'comments': comments,
        'comment_form': form
    })

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required 
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

def register(request):
    if request.method == 'POST':  
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_search(request):
    query = request.GET.get('query', '').strip()
    users = User.objects.filter(username__icontains=query)[:10] if query else []
    results = [
        {
            "username": user.username,
            "profile_image": user.user_profile_image.url if user.user_profile_image else "/static/default_profile.png",
            "id": user.id
        }
        for user in users
    ]
    return JsonResponse(results, safe=False)

@login_required
def user_details(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if target_user == request.user:
        followers_count = request.user.followers.count()
        following_count = request.user.following.count()
        followers_list = request.user.followers.all()
        following_list = request.user.following.all()

        context = {
            'user': request.user,
            'followers_count': followers_count,
            'following_count': following_count,
            'followers_list': followers_list,
            'following_list': following_list,
        }

        return render(request, 'logged_user_details.html', context)
    else:
        is_following = target_user.followers.filter(id=request.user.id).exists()
        followers_count = target_user.followers.count()
        following_count = target_user.following.count()

        context = {
            'target_user': target_user,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
        }

        return render(request, 'unlogged_user_details.html', context)


@login_required
def follow(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    if target_user != request.user: 
        if target_user.followers.filter(id=request.user.id).exists():
            target_user.followers.remove(request.user)
            followed = False
        else:
            target_user.followers.add(request.user)
            followed = True
            
            Notification.objects.create(user=target_user,sender=request.user,notification_type='follow',message=f"{request.user.username} started following you.")
    
    return redirect('user_details', user_id=user_id)

@login_required
def followers_list(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    followers = user.followers.all()
    return render(request, 'followers_list.html', {'user': user, 'followers': followers})


@login_required
def following_list(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    following = user.following.all()
    return render(request, 'following_list.html', {'user': user, 'following': following})


@login_required
def remove_follower(request, follower_id):
    follower = get_object_or_404(CustomUser, id=follower_id)
    if follower in request.user.followers.all():
        request.user.followers.remove(follower)
    return redirect('followers_list', user_id=request.user.id)


@login_required
def unfollow_user(request, following_id):
    following = get_object_or_404(CustomUser, id=following_id)
    if request.user in following.followers.all():
        following.followers.remove(request.user)
    return redirect('following_list', user_id=request.user.id)


def create_notification(user, message, related_tweet=None, related_message=None):
    Notification.objects.create(
        user=user,
        message=message,
        related_tweet=related_tweet,
        related_message=related_message
    )

def user_tweets(request, user_id):
    """Retrieve tweets of a specific user"""
    user = get_object_or_404(User, id=user_id)
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')

    context = {
        'user': user,
        'tweets': tweets,
        'tweet_count': tweets.count(),
    }
    return render(request, 'user_tweets.html', context)


@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    data = {
        "notifications_count": notifications.count(),
        "notifications": [
            {
                "id": n.id,
                "message": n.message,
                "created_at": n.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "notification_type": n.notification_type,
                "related_tweet_id": n.related_tweet.id if n.related_tweet else None,
                "related_message_id": n.related_message.id if n.related_message else None,
            }
            for n in notifications
        ],
    }
    return JsonResponse(data)



@csrf_exempt
@login_required
def mark_all_notifications_as_read(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({"success": "All notifications marked as read"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def notifications_page(request):
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    response = render(request, "notifications.html", {
        "unread_notifications": unread_notifications
    })
    unread_notifications.update(is_read=True)
    return response



@login_required
def get_messages(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)

    # if request.user == recipient:
    #     return redirect('messages_page')
    
    # Fetch messages between the logged-in user and the recipient
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=request.user))
    ).order_by("created_at")

    # Mark messages as read for the recipient
    messages.filter(recipient=request.user, is_read=False).update(is_read=True)

    # Handle AJAX POST requests for sending new messages
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            new_message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                content=content
            )
            Notification.objects.create(user=recipient,sender=request.user,notification_type='message',message=f"{request.user.username} sent you a message.",related_message=new_message)
            return JsonResponse({
                'message': new_message.content,
                'created_at': new_message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'sender': request.user.username
            })

    return render(request, 'chat.html', {
        'messages': messages,
        'recipient': recipient
    })


@login_required
def messages_page(request):
    logged_user = request.user

    users_interacted = User.objects.filter(
        Q(sent_messages__recipient=logged_user) | Q(received_messages__sender=logged_user)
    ).distinct()

    latest_message_subquery = Message.objects.filter(
        Q(sender=OuterRef('pk'), recipient=logged_user) |
        Q(sender=logged_user, recipient=OuterRef('pk'))
    ).order_by('-created_at')

    users_with_last_message = users_interacted.annotate(
        last_message_time=Subquery(latest_message_subquery.values('created_at')[:1]),
        last_message_text=Subquery(latest_message_subquery.values('content')[:1])
    ).order_by('-last_message_time')

    return render(request, 'messages_page.html', {
        'users': users_with_last_message
    })

