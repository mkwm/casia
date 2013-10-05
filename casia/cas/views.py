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
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.views import redirect_to_login
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import resolve, reverse
from django.dispatch import receiver
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from casia.cas.exceptions import Error
from casia.cas.models import Service, TicketRequest
from casia.cas.utils import validate_ticket, issue_service_ticket
from casia.http.response import XMLResponse

def validate(request):
    st = None
    try:
        st = validate_ticket(request)
    except Error:
        pass
    return HttpResponse('yes\n%s\n' % st.user if st else 'no\n\n')

def service_validate(request):
    response = Element('cas:serviceResponse',
                       attrib={'xmlns:cas': 'http://www.yale.edu/tp/cas'})
    try:
        st = validate_ticket(request)
        auth_success = SubElement(response, 'cas:authenticationSuccess')
        user = SubElement(auth_success, 'cas:user')
        user.text = st.user.get_username()
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
    ticket_request = TicketRequest()
    ticket_request.url = request.GET.get('service')
    ticket_request.renewed = 'renew' in request.GET
    if ticket_request.url:
        try:
            service = Service.objects.get_by_url(ticket_request.url)
            if not service.is_active:
                context.update({'error': 'This service is inactive'})
                return TemplateResponse(request, 'cas/security_error.html',
                                        context)
            ticket_request.service = service
            if not request.user.is_authenticated() or 'renew' in request.GET:
                if 'gateway' in request.GET:
                    return redirect(ticket_request.url)
            else:
                ticket_request.session_id = request.session.session_key
                ticket_request.user = request.user
            ticket_request.save()
            target = reverse('cas_issue',
                             kwargs={'ticket_request_id': ticket_request.id})
            return redirect(target)
        except Service.DoesNotExist:
            context.update({'error': 'This service is unknown'})
            return TemplateResponse(request, 'cas/security_error.html',
                                    context)
    else:
        return redirect('index')

def issue(request, ticket_request_id):
    ticket_request = get_object_or_404(TicketRequest, id=ticket_request_id)
    if ticket_request.user:
        return issue_service_ticket(ticket_request)
    else:
        target = reverse('cas_issue',
                         kwargs={'ticket_request_id': ticket_request.id})
        return redirect_to_login(target)

@receiver(user_logged_in)
def ticket_request_updater(sender, request, user, **kwargs):
    target = request.GET.get(REDIRECT_FIELD_NAME)
    if target:
        target = resolve(target)
        if target.url_name == 'cas_issue':
            ticket_request_id = target.kwargs.get('ticket_request_id')
            ticket_request = TicketRequest.objects.get(id=ticket_request_id)
            ticket_request.user = request.user
            ticket_request.session_id = request.session.session_key
            ticket_request.save()

def logout(request):
    return redirect('logout')
