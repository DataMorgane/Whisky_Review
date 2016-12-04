from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Review, Whisky, Cluster
from django.contrib.auth.models import User
from .forms import ReviewForm
from .suggestions import update_clusters
import datetime

from django.contrib.auth.decorators import login_required

# Create your views here.

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'reviews/review_list.html', context)

def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})

def whisky_list(request):
    whisky_list = Whisky.objects.order_by('-name')
    context = {'whisky_list': whisky_list}
    return render(request, 'reviews/whisky_list.html', context)

def whisky_detail(request, whisky_id):
    whisky = get_object_or_404(Whisky, pk=whisky_id)
    form = ReviewForm()
    return render(request, 'reviews/whisky_detail.html', {'whisky': whisky, 'form': form})

@login_required
def add_review(request, whisky_id):
    whisky = get_object_or_404(Whisky, pk=whisky_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.whisky = whisky
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:whisky_detail', args=(whisky.id,)))

    return render(request, 'reviews/whisky_detail.html', {'whisky': whisky, 'form': form})

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)

@login_required
def user_recommendation_list(request):
    # Get request user reviewed whiskies
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('whisky')
    user_reviews_whisky_ids = set(map(lambda x: x.whisky.id, user_reviews))

    # Get request cluster name (juste the first one right now)
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except: # If no cluster has been assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    # Get usernames for other members of the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # Get reviews by those users, excluding whiskies reviewed bu the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(whisky_id__in=user_reviews_whisky_ids)
    other_users_reviews_whisky_ids = set(map(lambda x: x.whisky.id, other_users_reviews))

    # Then get a whisky list including the previous IDs, order by rating
    whisky_list = sorted(
        list(Whisky.objects.filter(id__in=other_users_reviews_whisky_ids)),
        key=lambda x: x.average_rating(),
        reverse=True
    )

    return render(
        request,
        'reviews/user_recommendation_list.html',
        {'username': request.user.username, 'whisky_list':whisky_list}
    )