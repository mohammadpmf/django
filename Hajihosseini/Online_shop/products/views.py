from django.shortcuts import render, get_object_or_404
from django.views import generic

from .forms import CommentForm
from .models import Product, Comment


class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    queryset =Product.objects.filter(active=True)


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
    

class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        pk = int(self.kwargs['product_id'])
        product = get_object_or_404(Product, pk=pk)
        obj.product = product
        return super().form_valid(form)
    