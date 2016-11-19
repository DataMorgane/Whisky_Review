from django.shortcuts import render, get_object_or_404
from .models import Review, Whisky

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
    return render(request, 'reviews/whisky_detail.html', {'whisky': whisky})
