# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.


from django.contrib import messages
from django.contrib.auth import logout as auth_logout, REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.debug import sensitive_post_parameters

from casia.server.utils import issue_ticket
from casia.webapp.forms import AuthenticationForm, ReauthenticationFormWrapper
from casia.webapp.models import TicketRequest


@sensitive_post_parameters()
def login(request):
    from django.contrib.auth.views import login
    if not request.user.is_authenticated():
        return login(request, template_name='webapp/login.html',
            authentication_form=AuthenticationForm)
    elif request.GET.get(REDIRECT_FIELD_NAME):
        return login(request, template_name='webapp/relogin.html',
            authentication_form=ReauthenticationFormWrapper(user=request.user))
    else:
        return TemplateResponse(request, 'webapp/logged_in.html')


def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
        messages.success(request, 'You have been logged out successfully.')
    else:
        messages.error(request, 'You have to be logged in to log out. '
                       'Please log in to log out.')
    return redirect('login')


def cas_login(request):
    ticket_request = TicketRequest()
    ticket_request.renewed = 'renew' in request.GET
    ticket_request.url = request.GET.get('service')
    if ticket_request.url:
        if not request.user.is_authenticated() or 'renew' in request.GET:
            ticket_request.save()
            target = reverse('cas_issue',
                             kwargs={'ticket_request_uuid': ticket_request.id})
            return redirect_to_login(target)
        else:
            ticket_request.user = request.user
            ticket_request.session_id = request.session.session_key
            return issue_ticket(ticket_request)
    else:
        return redirect('login')


def cas_issue(request, ticket_request_uuid):
    ticket_request = get_object_or_404(TicketRequest, id=ticket_request_uuid)
    if ticket_request.user:
        return issue_ticket(ticket_request)
    else:
        target = reverse('cas_issue',
                         kwargs={'ticket_request_uuid': ticket_request.id})
        return redirect_to_login(target)
