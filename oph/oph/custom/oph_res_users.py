# -*- coding: utf-8 -*-
#===============================================================================
# Custom res_users object
# Add an CAFAT ID = convention ID for use in New Caledonia
# this CAFAT ID is for doctor not for patient

#===============================================================================
from openerp.osv import fields, osv

class res_users(osv.osv):
    """
    Custom res_users object
    Add a CAFAT ID for use in New Caledonia
    It's for odoo user not partner
    For partner you'll find the CAFAT ID in res.parner object
    """
    _inherit = "res.users"
    _columns = {
                'cafat_id':fields.char('CAFAT ID', size = 16, help = 'CAFAT ID of the doctor = convention number. This is not the CAFAT Number as for a patient'),
                }
