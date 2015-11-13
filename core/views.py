from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import *
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import FormView
from .forms import *

# Create your views here.
class Home(TemplateView):
    template_name = "home.html"

class HotelCreateView(CreateView):
    model = Hotel
    template_name = "hotel/hotel_form.html"
    fields = ['title', 'description', 'visibility']
    success_url = reverse_lazy('hotel_list')

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super(HotelCreateView, self).form_valid(form)

class HotelListView(ListView):
    model = Hotel
    template_name = "hotel/hotel_list.html"
    paginate_by = 5
class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotel/hotel_detail.html'

    def get_context_data(self, **kwargs):
        context = super(HotelDetailView, self).get_context_data(**kwargs)
        hotel = Hotel.objects.get(id=self.kwargs['pk'])
        reviews = Review.objects.filter(hotel=hotel)
        context['reviews'] = reviews
        user_reviews = Review.objects.filter(hotel=hotel, user=self.request.user)
        context['user_reviews'] = user_reviews
        return context

class HotelUpdateView(UpdateView):
    model = Hotel
    template_name = 'hotel/hotel_form.html'
    fields = ['title', 'description']
    def get_object(self, *args, **kwargs):
        object = super(HotelUpdateView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object
class HotelDeleteView(DeleteView):
    model = Hotel
    template_name = 'hotel/hotel_confirm_delete.html'
    success_url = reverse_lazy('hotel_list')
    def get_object(self, *args, **kwargs):
        object = super(HotelDeleteView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object
class ReviewCreateView(CreateView):
    model = Review
    template_name = "review/review_form.html"
    fields = ['text', 'visibility']

    def get_success_url(self):
        return self.object.hotel.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.hotel = Hotel.objects.get(id=self.kwargs['pk'])
        return super(ReviewCreateView, self).form_valid(form)
class ReviewUpdateView(UpdateView):
    model = Review
    pk_url_kwarg = 'review_pk'
    template_name = 'review/review_form.html'
    fields = ['text']

    def get_success_url(self):
        return self.object.hotel.get_absolute_url()

    def get_object(self, *args, **kwargs):
        object = super(ReviewUpdateView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object
class ReviewDeleteView(DeleteView):
    model = Review
    pk_url_kwarg = 'review_pk'
    template_name = 'review/review_confirm_delete.html'

    def get_success_url(self):
        return self.object.hotel.get_absolute_url()

    def get_object(self, *args, **kwargs):
        object = super(ReviewDeleteView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise PermissionDenied()
        return object
class VoteFormView(FormView):
    form_class = VoteForm

    def form_valid(self, form):
      user = self.request.user
      hotel = Hotel.objects.get(pk=form.data["hotel"])
      try:
        review = Review.objects.get(pk=form.data["review"])
        prev_votes = Vote.objects.filter(user=user, review=review)
        has_voted = (prev_votes.count()>0)
        if not has_voted:
            Vote.objects.create(user=user, review=review)
        else:
            prev_votes[0].delete()
        return redirect(reverse('hotel_detail', args=[form.data["hotel"]]))
      except:
        prev_votes = Vote.objects.filter(user=user, hotel=hotel)
        has_voted = (prev_votes.count()>0)
        if not has_voted:
            Vote.objects.create(user=user, hotel=hotel)
        else:
            prev_votes[0].delete()
        return redirect('hotel_list')
class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'user/user_detail.html'
    context_object_name = 'user_in_view'

    def get_context_data(self, **kwargs):
      context = super(UserDetailView, self).get_context_data(**kwargs)
      user_in_view = User.objects.get(username=self.kwargs['slug'])
      hotels = Hotel.objects.filter(user=user_in_view).exclude(visibility=1)
      context['hotels'] = hotels
      reviews = Review.objects.filter(user=user_in_view).exclude(visibility=1)
      context['reviews'] = reviews
      return context
class UserUpdateView(UpdateView):
    model = User
    slug_field = "username"
    template_name = "user/user_form.html"
    fields = ['email', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('user_detail', args=[self.request.user.username])

    def get_object(self, *args, **kwargs):
        object = super(UserUpdateView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object
class UserDeleteView(DeleteView):
    model = User
    slug_field = "username"
    template_name = 'user/user_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('logout')

    def get_object(self, *args, **kwargs):
        object = super(UserDeleteView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

    def delete(self, request, *args, **kwargs):
        user = super(UserDeleteView, self).get_object(*args)
        user.is_active = False
        user.save()
        return redirect(self.get_success_url())

class SearchHotelListView(HotelListView):
    def get_queryset(self):
        incoming_query_string = self.request.GET.get('query','')
        return Hotel.objects.filter(title__icontains=incoming_query_string)


