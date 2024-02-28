from django.contrib.sitemaps import Sitemap

from men.models import Men, Category


class PostSitemap(Sitemap):
    chagefreq = 'monthly'
    prioroty = 0.9


    def items(self):
        return Men.published.all()

    def lastmod(self, obj):
        return obj.time_update


class CategorySitemap(Sitemap):
    chagefreq = 'monthly'
    prioroty = 0.9


    def items(self):
        return Category.objects.all()

