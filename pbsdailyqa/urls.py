from django.conf.urls import patterns, url  # include
from django.views.decorators.cache import cache_page
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    # Examples:
    # url(r'^$', 'pbsdailyqa.views.home', name='home'),
    # url(r'^pbsdailyqa/', include('pbsdailyqa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^', 'pbsdailyqa.views.index'),
    '',
    url(r"^$", views.PBSDailyQAReview.as_view(),
        name="pbsdailyqa"),
    url(r"^units/$",
        views.get_unitlist,
        name="unitlist"),
    url(r"^testlistinstance/$",
        views.get_testlistinstancelist,
        name="testlistinstancelist"),
    url(r"^testlistinstance/(?P<pk>\d+)/$",
        views.get_testlistinstance,
        name="testlistinstance"),
    url(r"^plot.png",
        cache_page(60 * 60)(views.get_plot),
        # views.get_plot,
        name="pbsanalysis_plot"),
)
