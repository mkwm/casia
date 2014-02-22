# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from xml.etree.ElementTree import Element, SubElement

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.views import redirect_to_login
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import resolve, reverse
from django.dispatch import receiver
from django.http import QueryDict
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.six.moves.urllib.parse import urlparse
from django.utils.timezone import now
from django.utils.translation import ugettext as _

from casia.cas import authenticate
from casia.cas.exceptions import Error, InvalidRequest
from casia.cas.forms import LoginConfirmationForm
from casia.cas.models import ProxyGrantingTicket, ServiceURL, CASLoginHistoryEntry
from casia.cas.utils import (validate_ticket, issue_proxy_ticket,
                             issue_service_ticket)
from casia.http.response import XMLResponse


def validate(request):
    st = None
    try:
        st = validate_ticket(request)
        service = authenticate(service=st.service, request=request)
        if service is None:
            raise InvalidRequest('Request authentication failed.')
    except Error:
        pass
    return HttpResponse('yes\n%s\n' % st.user if st else 'no\n\n')


def service_validate(request, require_st=True):
    response = Element('cas:serviceResponse',
                       attrib={'xmlns:cas': 'http://www.yale.edu/tp/cas'})
    try:
        st = validate_ticket(request, require_st)
        service = authenticate(service=st.service, request=request)
        if service is None:
            raise InvalidRequest('Request authentication failed.')
        auth_success = SubElement(response, 'cas:authenticationSuccess')
        user = SubElement(auth_success, 'cas:user')
        user.text = st.user.get_username()
        if st.service.has_perm('proxy'):
            pgt = ProxyGrantingTicket.objects.create_for_request(request)
            if pgt:
                pgt_iou = SubElement(auth_success, 'cas:proxyGrantingTicket')
                pgt_iou.text = pgt.iou
        if st.pgt:
            proxies = SubElement(auth_success, 'cas:proxies')
            current = st
            while current.pgt:
                proxy = SubElement(proxies, 'cas:proxy')
                proxy.text = current.pgt.url
                current = current.pgt.st
    except Error as ex:
        auth_failure = SubElement(response, 'cas:authenticationFailure',
                                  attrib={'code': ex.code})
        auth_failure.text = ex.msg
    return XMLResponse(response)


def login(request):
    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': 'Authentication'
    }
    url = request.GET.get('service')
    if url:
        try:
            service = ServiceURL.objects.get_by_url(url)
            if not service.is_active:
                context.update({'error': _('This service is inactive')})
                return TemplateResponse(request, 'cas/security_error.html',
                                        context)
            if not request.user.is_authenticated() or 'renew' in request.GET:
                if 'gateway' in request.GET:
                    return redirect(url)
            else:
                entry = CASLoginHistoryEntry(user=request.user, service=service)
                entry.save()
            querystring = QueryDict('', mutable=True)
            querystring['service'] = url
            if 'renew' in request.GET:
                querystring['renew'] = 'true'
            target = reverse('cas:issue') + '?' + querystring.urlencode(safe='/')
            return redirect(target)
        except ServiceURL.DoesNotExist:
            context.update({'error': _('This service is unknown')})
            return TemplateResponse(request, 'cas/security_error.html',
                                    context)
    else:
        return redirect('index')


@login_required
def issue(request):
    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Confirmation')
    }
    url = request.GET.get('service')
    try:
        service = ServiceURL.objects.get_by_url(url)
        x = CASLoginHistoryEntry.objects.filter(user_id=request.user.id,
                                                service=service,
                                                used_at__isnull=True).latest('login_time')
        if service.is_trusted or 'continue' in request.POST:
            x.used_at = now()
            x.save()
            return issue_service_ticket(request.user, request.session, url, service, x.renewed)
        elif 'abort' in request.POST:
            return redirect('index')
        else:
            form = LoginConfirmationForm()
            context.update({'form': form, 'service': service})
            return TemplateResponse(request, 'cas/confirm.html', context)
    except CASLoginHistoryEntry.DoesNotExist:
        querystring = QueryDict('', mutable=True)
        querystring['service'] = url
        if 'renew' in request.GET:
            querystring['renew'] = 'true'
        target = reverse('cas:issue') + '?' + querystring.urlencode(safe='/')
        return redirect_to_login(target)


@receiver(user_logged_in)
def ticket_request_updater(sender, request, user, **kwargs):
    target = request.GET.get(REDIRECT_FIELD_NAME)
    if target:
        p = urlparse(target)
        target = resolve(p.path)
        querystring = QueryDict(p.query)
        if target.view_name == 'cas:issue' and 'service' in querystring:
            service = ServiceURL.objects.get_by_url(querystring['service'])
            entry = CASLoginHistoryEntry(user=user, service=service, renewed=True)
            entry.save()


def logout(request):
    return redirect('logout')


def proxy(request):
    response = Element('cas:serviceResponse',
                       attrib={'xmlns:cas': 'http://www.yale.edu/tp/cas'})
    try:
        pt = issue_proxy_ticket(request)
        service = authenticate(service=pt.pgt.st.service, request=request)
        if service is None:
            raise InvalidRequest('Request authentication failed.')
        proxy_success = SubElement(response, 'cas:proxySuccess')
        proxy_ticket = SubElement(proxy_success, 'cas:proxyTicket')
        proxy_ticket.text = pt.ticket
    except Error as ex:
        proxy_failure = SubElement(response, 'cas:proxyFailure',
                                   attrib={'code': ex.code})
        proxy_failure.text = ex.msg
    return XMLResponse(response)
