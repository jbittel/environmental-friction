from django.contrib.sites.models import Site
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic import ListView

import base32_crockford

from .models import Post


class PostList(ListView):
    paginate_by = 5
    queryset = Post.objects.published()

    def get_context_data(self, **kwargs):
        context = {
            'domain': Site.objects.get_current().domain,
        }
        return super(PostList, self).get_context_data(**context)


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
