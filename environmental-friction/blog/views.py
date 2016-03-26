from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.timezone import now
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import View

import base32_crockford

from .forms import QuickDraftForm
from .models import Post


class PostDetail(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = kwargs.get(self.slug_url_kwarg, None)
        if slug != self.object.slug:
            return redirect(self.object, permanent=True)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        try:
            pk = base32_crockford.decode(key)
        except ValueError:
            raise Http404
        return get_object_or_404(Post.objects.published(), pk=pk)


class PostList(ListView):
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = {
            'domain': Site.objects.get_current().domain,
        }
        return super(PostList, self).get_context_data(**context)

    def get_queryset(self):
        return Post.objects.published()


class EditPost(UpdateView):
    model = Post
    fields = ['title', 'body', 'post_image', 'tags']
    success_url = reverse_lazy('blog:write')
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        if 'publish' in self.request.POST:
            form.instance.publish = now()
        elif 'unpublish' in self.request.POST:
            form.instance.publish = None
        return super(EditPost, self).form_valid(form)


class ListPosts(LoginRequiredMixin, ListView):
    queryset = Post.objects.order_by('-modified')
    template_name = 'blog/write_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListPosts, self).get_context_data(**kwargs)
        context['form'] = QuickDraftForm()
        return context


class SaveQuickDraft(LoginRequiredMixin, FormView):
    form_class = QuickDraftForm
    success_url = reverse_lazy('blog:write')
    template_name = 'blog/write_list.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(SaveQuickDraft, self).form_valid(form)


class Write(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = ListPosts.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = SaveQuickDraft.as_view()
        return view(request, *args, **kwargs)
