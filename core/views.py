from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import *

# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class HotelCreateView(CreateView):
    model = Hotel
    template_name = "hotel/hotel_form.html"
    fields = ['title', 'description']
    success_url = reverse_lazy('hotel_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(HotelCreateView, self).form_valid(form)
class HotelListView(ListView):
    model = Hotel
    template_name = "hotel/hotel_list.html"
class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotel/hotel_detail.html'

    def get_context_data(self, **kwargs):
        context = super(HotelDetailView, self).get_context_data(**kwargs)
        hotel = Hotel.objects.get(id=self.kwargs['pk'])
        reviews = Review.objects.filter(hotel=hotel)
        context['reviews'] = reviews
        return context

class HotelUpdateView(UpdateView):
    model = Hotel
    template_name = 'hotel/hotel_form.html'
    fields = ['title', 'description']
class HotelDeleteView(DeleteView):
    model = Hotel
    template_name = 'hotel/hotel_confirm_delete.html'
    success_url = reverse_lazy('hotel_list')
class ReviewCreateView(CreateView):
    model = Review
    template_name = "review/review_form.html"
    fields = ['text']

    def get_success_url(self):
        return self.object.hotel.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.hotel = Hotel.objects.get(id=self.kwargs['pk'])
        return super(ReviewCreateView, self).form_valid(form)


