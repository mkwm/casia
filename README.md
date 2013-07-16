Casia
=====

CAS server based on Django

Installation
------------

Python 3 is currently not supported. You have to use Python 2.

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

Now, create Django database tables:
``python manage.py syncdb``

And then apply Casia South migrations:
``python manage.py migrate``

Authors
-------

**Mateusz Małek**
+ [http://mkwm.eu.org/](http://mkwm.eu.org/)

External components
-------------------

Casia includes the following external components:
+ [Twitter Bootstrap](http://twitter.github.io/bootstrap/) by [@mdo](http://twitter.com/mdo) and [@fat](http://twitter.com/fat) which is licensed under the Apache License, Version 2.0
+ [Font Awesome](http://fontawesome.github.io/) by Dave Gandy which is licensed under SIL OFL 1.1 (font) and the MIT License (code)
+ [HTML5 Shiv](https://github.com/aFarkas/html5shiv) by [@afarkas](http://twitter.com/afarkas), [@jdalton](http://twitter.com/jdalton), [@jon_neal](http://twitter.com/jon_neal) and [@rem](http://twitter.com/rem) which is dual licensed under the MIT License or GNU GPL, Version 2.0
+ [jQuery](http://jquery.org/) by jQuery Foundation, Inc. which is licensed under the MIT License

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
