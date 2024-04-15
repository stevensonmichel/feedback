from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView

from .forms import ReviewForm
from .models import Review

# Create your views here.

class ReviewView(CreateView):
    # EXAMPLE FOR ------CREATEVIEW
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review.html"
    success_url = "/thank-you"
    
    # EXAMPLE FOR ------FORMVIEW
    # form_class = ReviewForm
    # template_name = "reviews/review.html"
    # success_url = "/thank-you"  
    
    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)
      
      
    # EXAMPLE FOR ------VIEW
    # def get(self, request):
    #     form = ReviewForm()
        
    #     return render(request, "reviews/review.html", {
    #     "form": form
    # })
        
        
    # def post(self, request):
    #     form = ReviewForm(request.POST)
        
    #     if form.is_valid():
    #         form.save()
            
    #         return HttpResponseRedirect("/thank-you")
        
    #     return render(request, "reviews/review.html", {
    #     "form": form
    # })


class ThankYouView(TemplateView):
    template_name = "reviews/thank_you.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "This work"
        return context
    
    
class ReviewsListView(ListView):
    template_name = "reviews/review_list.html"
    model = Review
    context_object_name = "reviews"
    
    # def get_queryset(self):
    #     base_query = super().get_queryset()
    #     data = base_query.filter(rating__gt=4)
    #     return data
    
    
class SingleReviewView(DetailView):
    template_name = "reviews/single_review.html"
    model = Review
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        loaded_review = self.get_object
        request = self.request
        favorite_id = request.session.get("favorite_review")
        context["is_favorite"] = favorite_id == str(loaded_review.id)
        return context
    
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     review_id = kwargs["id"]
    #     selected_review = Review.objects.get(pk=review_id)
    #     context["review"] = selected_review
    #     return context

    

class AddFavoriteView(View):
    def post(self, request):
        review_id = request.POST["review_id"]
        request.session["favorite_review"] = review_id
        return HttpResponseRedirect("reviews/" + review_id)
