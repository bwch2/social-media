from django.shortcuts import render


from django.urls import reverse
from django.views import generic
# these are the generic views / CBVs

from django.contrib import messages

from groups.models import Group, GroupMember
from groups import models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import get_object_or_404
# Create your views here.

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ['name', 'description']
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin, generic.base.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, ('You are already a member'))
        else:
            messages.success(self.request, 'You are now a member')
        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.base.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        membership = models.GroupMember.objects.filter(
                    user = self.request.user,
                    group__slug = self.kwargs.get('slug')).get()

        try:
            membership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, "You're not in this group")

        else:
            membership.delete()
            messages.success(self.request, "You have left this group")
        return super().get(request, *args, **kwargs)
