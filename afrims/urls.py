from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # RapidSMS core URLs
    (r'^account/', include('rapidsms.urls.login_logout')),
    url(r'^settings/$', direct_to_template,
        {'template': 'afrims/not_implemented.html'}, name='settings'),
    url(r'^access_denied/$', direct_to_template,
        {'template': 'afrims/access_denied.html'}, name='access-denied'),

    url(r'^survey/export/(?P<tree_id>\d+)/$', 'decisiontree.views.export', name='export_tree'),

    # RapidSMS contrib app URLs
    (r'^ajax/', include('rapidsms.contrib.ajax.urls')),
    (r'^export/', include('rapidsms.contrib.export.urls')),
    (r'^httptester/', include('rapidsms.contrib.httptester.urls')),
    (r'^locations/', include('rapidsms.contrib.locations.urls')),
    (r'^messagelog/', include('rapidsms.contrib.messagelog.urls')),
    (r'^messaging/', include('rapidsms.contrib.messaging.urls')),
    (r'^registration/', include('rapidsms.contrib.registration.urls')),
    (r'^scheduler/', include('rapidsms.contrib.scheduler.urls')),
    (r'^broadcast/', include('afrims.apps.broadcast.urls')),
    (r'^reminders/', include('afrims.apps.reminders.urls')),
    (r'^test-messager/', include('afrims.apps.test_messager.urls')),
    (r'^crm/', include('afrims.apps.groups.urls')),
    (r'^rosetta/', include('rosetta.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),    
    (r'^', include('afrims.apps.reports.urls')),
)

if 'auditcare' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^', include('auditcare.urls')),
    )

if 'couchlog' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^couchlog/', include('couchlog.urls')),
    )


if settings.DEBUG:
    urlpatterns += patterns('',
        # helper URLs file that automatically serves the 'static' folder in
        # INSTALLED_APPS via the Django static media server (NOT for use in
        # production)
        (r'^', include('rapidsms.urls.static_media')),
        (r'^%s(?P<path>.*)' % settings.MEDIA_URL.lstrip('/'),
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}
        )
    )

