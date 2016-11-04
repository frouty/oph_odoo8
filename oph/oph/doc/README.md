le module base_calendar n'existe pas dans la 8.0

je cherche la valeur de ref
=============

```xml
<field name="inherit_id" ref="base.view_partner_form"/\> 
```

mode debug --> Edit form view --> External ID == ref


```xml
<field name="arch" type="xml">
            <data>
            <xpath expr="//notebook/page[@string='Journals']" position="replace">
            </xpath>
            <xpath expr="//field[@name='target_move']" position="after">
                <field name="display_account"/>
                <newline/>
            </xpath>
            </data>
</field>
```

Comment supprimer le "create and edit"
========         

Dans un champ : many2one
le widget ressemble à celui d'un champ selection
on peut supprimer le "create and edit" avec :

```xml
<xpath expr="//field[@name='title']" position="attributes">
                        <attribute name="widget">selection</attribute><!-- pour éliminer "create et modifier"-->
                        <!--<attribute name="required">True</attribute>NEMARCHEPAS -->                
</xpath>
```

Comment vérifier un champ et afficher une pop up?
===============
voir la méthode : 

```python
def check_partners_email
```    

Le format des dates dans Odoo
=======================
On trouve le format des dates dans : openerp/tools/misc.py
On a les constantes :

```python
DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_TIME_FORMAT = "%H:%M:%S"
DEFAULT_SERVER_DATETIME_FORMAT = "%s %s" % (DEFAULT_SERVER_DATE_FORMAT,DEFAULT_SERVER_TIME_FORMAT)
```

Comment on appelle ces constantes: 

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


calendar.event
======
start fields.function(_compute, .......required = True....)  
stop fields.function(_compute, ...... required = True)  

partner_id Partner many2one  
partner_ids Attendees many2many  

rrule : recurrent rule

le logging
=======
Je vais essayer à la place de mettre des prints

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
```

après cela s'utilise comme cela :
~~~python
logger.info('blablabla')
logger.debug('Records: %s', records)
logger.info('updating records')
~~~

Il y a plusieurs niveaux de logging:  
- info  
- debug  

- warning  
- error  
- critical  


logger.setLevel()
-------
Spécifie le plus bas niveau de messages de log qui sera traité. DEBUG est le plus bas niveau et critical le plus haut. EG si le level est INFO, les INFO, WARNING, ERROR, CRITICAL seront traitées et DEBUG ignoré..


selection
======
Qd on a un champ selection avec comme selection la liste de tuple: 
~~~python
STATE_SELECTION = [
        ('needsAction', 'Needs Action'),
        ('tentative', 'Uncertain'),
        ('declined', 'Declined'),
        ('accepted', 'Accepted'),
    ]
    
'state': fields.selection(STATE_SELECTION, 'Status', readonly=True, help="Status of the attendee's participation"),    
~~~
On peut utiliser *default* comme cela:
~~~python
  _defaults = {
        'state': 'needsAction',
    }
~~~
  on passe donc la key
  
Method overriding - Super
=====

~~~python
class Parent(object):
	def __init__(self):
		self.value = 5
	def get_value(self):
		return self.value
		
class Child(object):
	def get_value(self):
		return self.value +1
~~~

On réécrit tout simplement la méthode avec le meme nom.

Qd on surcharge une méthode il faut se demander:

- si l'on veut filtrer les arguments : pre-traitement  
- si l'on veut filtrer les résultats : post-traitement.  
- ou les deux  

* prefiltering
~~~python
import datetime

class Logger(object):
    def log(self, message):
        print message

class TimestampLogger(Logger):
    def log(self, message):
        message = "{ts} {msg}".format(ts=datetime.datetime.now().isoformat(),
                                      msg=message)
        super(TimestampLogger, self).log(message)
~~~

*post-processing

~~~python
import os

class FileCat(object):
    def cat(self, filepath):
        f = file(filepath)
        lines = f.readlines()
        f.close()
        return lines

class FileCatNoEmpty(FileCat):
    def cat(self, filepath):
        lines = super(FileCatNoEmpty, self).cat(filepath)
        nonempty_lines = [l for l in lines if l != '\n']
        return nonempty_lines 
~~~

La syntaxe c'est: *super(NomChildClass, self).nomdelafonctionparent(args)*


model_obj.read(cr,uid,ids(liste des records à lire), [liste des champs à lire],context=context)
=====
return une liste de dictionnaire de la forme:

[{'start_datetime': False, 'start_date': '2016-05-30', 'id': 1}, {'start_datetime': '2016-05-29 21:00:00', 'start_date': False, 'id': 13}]


model_obj.browse(cr,uid,[liste des id des records]ids,context=context)
===========

return in iterable 
for record in browse_obj:
	record.fieldname1.id
	record.fieldname2
	.... 

	
pour récuper un model
self.pool['nom_ du_model]


Report
====
pour créer un report sur un model particulier il faut créer :

- Ce report
- report template

Si on veut accéder à plusieurs models il faut créer un custom reports class qui nous acces à plusieurs modeles dans le template.

Il y a un fichier  addons/views/report_invoice.xml qui contient les templates.

Il y a un fichier addons/account_report.xml avec
~~~xml
 <report 
	id= ...
	model=...
	string=...
	xml='account/report/....'
	xsl='
	/>
~~~
des liens
---
- https://www.odoo.com/documentation/8.0/reference/qweb.html  
- https://www.odoo.com/documentation/8.0/reference/reports.html  

- http://www.solibre.info/odoo_doc/_build/html/howtos/backend.html

Buttons
===
- http://www.slideshare.net/openobject/odoo-smart-buttons

Views
===
- https://www.odoo.com/documentation/8.0/reference/views.html