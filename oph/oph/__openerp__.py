# -*- coding: utf-8 -*-

# fichier lu qd on install le module
# avec administration/module/import module.
#
{
    'name' : 'Ophthalmology',
    'version' : '0.1',
    'author' : 'Cabinet GOEEN',
    'category': 'Generic Modules/Others',
    'description': """
Module de consultation pour l'ophtalmologiste
=======================================================================================

Permet de faire pleins de choses absolument géniales
                """,
    'website': '',
    'depends' : [
                 "base",
                 "account",
                 "account_voucher",
                 "account_accountant",
                 "account_cancel",
                 "crm",
                 "l10n_fr",
                 "sale",
                 "knowledge",
                 "document",
                 "portal",
                 ],
    'data': [
             'security/oph_security.xml',
             'custom/oph_res_partner_view.xml',
             'custom/oph_res_users_view.xml',
             'custom/oph_account_voucher_view.xml',
             'custom/oph_sale_order_view.xml',
             'oph_instrumentation_view.xml',
             'oph_measurement_view.xml',
             'oph_prescription_view.xml',
             'oph_agenda_view.xml',
             'wizard/oph_agenda_factory_view.xml',
             'data/oph_motive_data.xml',
             'data/product_data.xml',
             'data/measurement_type.xml',
             'custom/oph_account_invoice_view.xml',
             'wizard/oph_etat_factory_view.xml',
             'data/prescription_data.xml',
             
             
             
             ],
    'demo': [
             'demo/res_partner_demo.xml',
             ],
    #===========================================================================
    # 'demo': [
    #              'demo/oph_partner_demo.xml',
    #              'demo/bloc_agenda_demo.xml',
    #              'demo/oph_agenda_demo.xml',
    #              ],
    #===========================================================================
    'test': [],
    'installable': True,
    'active': False,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
