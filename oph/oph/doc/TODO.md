# res.partner
-[ ] onglet sales & purchase mettre le champ pour la liste de prix.

-[X] je ne peux pas entrer des caractères accentués dans le prénom.

pour obtenir l'encodage:

```python
import sys
sys.getdefaultencoding()
```
# res.partner form view

- Ajouter le bouton:
	- [ ] *LogBlocLine*
	- [ ] *LogReport*
	- [ ] *LogInvoices*
	- [x] *HistoryMesearument*
	- [x] *LogConsultations*
	- [x] *LogRefraction*
	- [x] *LogConclusion*
	- [X] *LogSLE*
	
- [ ] Comment faire pour avoir le nombre de ligne dans les boutons Log. Comme dans Opportunities et Meetings par exemple.

- [x] Effacer le boutton *Opportunities*

# Faciliter ou éviter la saisie du nom de la banque pour les cheques
- dans res.partner / onglet accounting / champ bank_ids. C'est là qu'il faudrait renseigner cette information. Mais y a deux champs qui sont à required = True inutile pour moi.
C'est dans l'objet res.partner.bank 
	- state
	- acc_number

# wizard agenda factory 
- [ ]  field **user_id** filtre sur les users du group doctor. (inutile d'afficher les secrétaires par exemple)

# wizard agenda factory 
- [ ] field **tag** filtre uniquement sur les tag du user. Chaque user pourrait avoir ses tag a lui, ses tag favoris.
- [ ] field **step** filled with the duration value of tag
- [ ] Il va falloir faire un objet **slot.tag** avec comme champ user_id many2many, name, comment, duration

# pricelist
- [ ] mettre en place le champ ? du model product.pricelist
Cette relation existe dans le form calendar.event. field name = pricelist many2one. S'en inspirer pour la mettre dans l'objet res.partner.

# calendar.event vue calendar
- [ ] affichage:
	* si occupé  fullname, name(du slot) et propriétaire du slot (= doctor) 
	* si libre	 tag et propriétaire du slot
	
Actuellement si le champ est occupé affiche uniquement heure de début et fullname, si le slot est libre affiche heure, ouvert, tag (cs ou tech) eg: 14:00 Ouvert,cs 

# calendar.event form view
-[x] supprimer le champ name de la tree view oph.measurement
je mets file oph_agenda_view.xml ligne 189 champ name invible="1" et cela ne marche pas.
J'ai du faire un update du module pour que cela marche.

# calendar.event form view
- [ ] il y a un probleme avec le champ **ors** (line 219) 

qui est à required=true alors que parfois ce champ n'est pas renseigné automatique lors du peuplement de medication_ids car cela n'est pas toujours nécessaire comme des comprimés par la bouche par exemple. Ce champ est requis uniquement pour les collyres concrétement. Et je le note dans l'objet oph.brandname champ **ors_needed** fichier oph_prescription.py.

# calendar.event form view
- [X] rendre invisible l'onglet **Options**
essayer quelque chose du genre:
```xml
<xpath expr="//page[@string='Options']" position="attributes">
   	<attribute name="invisible">True</attribute>
</xpath>              
```

# oph.measurement tree view
- [ ] la date de la consultation ne s'affiche pas.