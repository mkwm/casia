# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.utils.translation import ugettext_lazy as _

from casia.template import menu, MenuItem

menu['navbar'].append(MenuItem('password_change', _('Change password'), icon='key'))
menu['navbar'].append(MenuItem('admin:index', _('Admin site'), lambda request: request.user.is_staff, icon='star'))
menu['navbar'].append(MenuItem('logout', _('Log out'), icon='sign-out'))