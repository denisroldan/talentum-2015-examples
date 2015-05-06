from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
	# Examples:
	# url(r'^$', 'gamequiz.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'game.views.getChallenge', name='get_challenge'),
	url(r'^solve/', 'game.views.solveChallenge', name='solve_challenge'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
