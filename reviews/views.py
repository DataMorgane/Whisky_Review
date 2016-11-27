from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Review, Whisky
from .forms import ReviewForm
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
