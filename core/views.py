from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
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
