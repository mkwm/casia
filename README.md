Casia
=====

CAS server based on Django

Installation
------------

At the moment installation is a bit complicated. Look only if you dare...

Clone this repository:
``git clone https://github.com/mkwm/casia.git``

Change directory:
``cd casia``

Install dependencies:
``pip install -r requirements.txt``

Then you need to copy contents of ``casia/conf/instance_template`` and adjust
their contents to your needs (substitute instance_name with instance name).

Remember that ``casia`` folder has to be in your ``PYTHONPATH``!

Authors
-------

**Mateusz Małek**
+ [http://mkwm.eu.org/](http://mkwm.eu.org/)

Copyright and license
---------------------

Copyright (C) 2013 Mateusz Małek

Casia is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

Casia is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.