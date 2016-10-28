# -*- coding: utf-8 -*-
#===============================================================================
# Custom res_users object
# Add Etablissment payeur and Titulaire du cheque
#===============================================================================
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class account_voucher(orm.Model):
    """
    Custom account_voucher object (== Payment)
    Add field chq_owner
    For bank use ref payment instead
    """
    _inherit = "account.voucher"

    def _get_process_status(self,cursor, uid,context=None):
        return 
    _columns = {
                'check_owner':fields.char('Check Owner', help = 'Owner of the check. Change it, if different of the customer"', size = 32),
                'check_deposit':fields.boolean('Check Deposit', help = 'Check Deposit'),
                'process_status':fields.selection([('process','In Process'),
                                                               ('done','Done'),
                                                               ('forprocess','For processing')],'Process',readonly=False),
                'bank_id':fields.many2one('res.bank','Bank Account'),
                        }
    _defaults={
               'process_status':'forprocess'}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
