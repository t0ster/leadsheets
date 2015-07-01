This project is a hypothetical scoring engine for sales leads.

Usage
=====

::

  leadsheets <csvfile>


Testing
=======

To run tests do the following::

  pip install -r requirements.txt
  nosetests


CSV Format
==========

::

  contact id - integer
  event - string of values {web, email, social, webinar}
  score - a rational number with up to 2 digits after the decimal

  Example:
  1, web, 34.33
  1, email, 3.4
  1, social, 4
  2, webinar, 55.4
  2, social, 15