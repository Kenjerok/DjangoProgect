from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import Article, Category

class HomePageView(ListView):
    model = Category
    template_name = 'index.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(main_page=True).order_by('-pub_date')[:5]
        return context

    def get_queryset(self, *args, **kwargs):
        return Category.objects.all()

class ArticleDetail(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'item'
    date_field = 'pub_date'
    query_pk_and_slug = True
    month_format = '%m'
    allow_future = True

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetail, self).get_context_data(*args, **kwargs)
        try:
            context['images'] = context['item'].images.all()
        except:
            pass
        return context

    def get_object(self):
        return get_object_or_404(Article, 
                                 pub_date__year=self.kwargs['year'],
                                 pub_date__month=self.kwargs['month'],
                                 pub_date__day=self.kwargs['day'],
                                 slug=self.kwargs['slug'])

class ArticleList(ListView):
    model = Article
    template_name = 'articles_list.html'
    context_object_name = 'items'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleList, self).get_context_data(*args, **kwargs)
        try:
            context['category'] = Category.objects.get(slug=self.kwargs.get('slug'))
        except Exception:
            context['category'] = None
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        return Article.objects.all().order_by('-pub_date')

class ArticleCategoryList(ArticleList):

    def get_queryset(self, *args, **kwargs):
        return Article.objects.filter(category__slug=self.kwargs['slug']).order_by('-pub_date')
