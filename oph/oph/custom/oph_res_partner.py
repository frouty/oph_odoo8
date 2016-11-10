# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from mx import DateTime

from openerp.osv import osv, fields
from openerp.tools.translate import _

import logging
_logger = logging.getLogger( __name__ )

class res_partner( osv.osv ):
    _name = 'res.partner'
    _description = 'Partner'
    _inherit = 'res.partner'

    def onchange_gender( self, cr, uid, id, gender, context = None ):
        """Set title according to gender
        ie gender == male ---> mister
        NE MARCHE PAS EN 80 POURQUOI?
        """

        _logger.info( 'in onchange_gender ...' )
        # import pdb;pdb.set_trace()
        if context is None:
            context = {}
        title_table = self.pool.get( 'res.partner.title' )
        if gender:
            if gender == 'M':  # va chercher l'id dans la table res.partner.title est Mister
                ID = title_table.search( cr, uid, [( 'name', '=', 'Mister' )] )
            if gender == 'F':
                ID = title_table.search( cr, uid, [( 'name', '=', 'Madam' )] )
#         else:
#             warning = {
#                      'title':_( 'Caution Oulala' ),
#                      'message':_( 'You must choose a gender', )
#                      }
#             return {'warning':warning, }
        return {'value':{'title':ID[0]}, }

    def onchange_name( self, cr, uid, id, firstname, lastname, dob, context = None ):
        """Will put fullname = LASTNAME, Firstname in field name of table res.partner
        """
        if context == None:
            context = {}
        fullname = ''
        warning = False
        if dob:
            """Looking for an hononymus in database
            """
            partner_ids = self.search( cr, uid, [( 'dob', '=', dob ), ( 'name', 'like', lastname ), ( 'firstname', 'like', firstname )], limit = 1, context = context )
            if partner_ids:
                warning = {}
                warning['title'] = _( 'Caution' )
                warning['message'] = _( 'There is already an homonyme with the same birthdate' )
        # return {'value' : {'name': (lastname.upper() if lastname else ''), 'firstname': (firstname.capitalize() if firstname else '')}, 'warning': warning}
        return {'value': {'name':( lastname.upper() if lastname else '' ), 'firstname':( ' '.join( map( str, map( lambda w:w.capitalize(), firstname.split() ) ) ) if firstname else '' )}, 'warning':warning}

    def _format_fullname( self, cr, uid, ids, name, args, context = None ):
        """
        Will put fullname = LASTNAME, Firstname 
        in field name of table res.partner
        """
        res = {}
        for m in self.browse( cr, uid, ids, context = context ):
            firstname = m.firstname
            lastname = m.name
            fullname = ''
            if lastname:
                # fullname=(lastname.upper() if lastname else '') + (", " +firstname.capitalize() if firstname else '')
                fullname = ( lastname.upper() if lastname else '' ) + ( ", " + ' '.join( map( str, map( lambda w:w.capitalize(), firstname.split() ) ) ) if firstname else '' )
            res[m.id] = fullname
        return res

    def _get_age( self, cr, uid, ids, field_name, arg, context = {} ):
        # print 'JE PASSE PAR _GET_AGE et CONTEXT is:', context
        res = {}
        records = self.browse( cr, uid, ids, context )
        date = DateTime.today()
        for record in records :
            age = ''
            res[record.id] = {
                'age' : '',
            }
            birthdate = False
            if record.dob:
                birthdate = DateTime.strptime( record.dob, '%Y-%m-%d' )
                year, month, day = birthdate.year, birthdate.month, birthdate.day
            if birthdate:
                day = int( day )
                month = int( month )
                year = int( year )
                if ( date.month > month ) or ( date.month == month and date.day >= day ):
                    if ( date.year - year ) >= 2:
                        age = str( date.year - year ) + _( ' YO' )
                    else:
                        if date.year == year:
                            age = str( date.month - month ) + _( ' month' )
                        else:
                            age = str( 12 + date.month - month ) + _( ' month' )
                else:
                    if ( date.year - year - 1 ) >= 2:
                        age = str( date.year - year - 1 ) + _( ' YO' )
                    else:
                        months = date.month - month
                        if date.month == month:
                            months = -1
                        if date.year == year:
                            age = str( months ) + _( ' month' )
                        elif date.year == year + 1:
                            age = str( 12 + months ) + _( ' month' )
                        elif date.year == year + 2:
                            age = str( 24 + months ) + _( ' month' )
            res[record.id]['age'] += age
        return res

    _columns = {
               'firstname': fields.char( "Firstname", size = 64 ),
               'fullname':fields.function( _format_fullname, type = 'char', size = 128, string = 'Fullname', store = True, method = True ),
               'gender':fields.selection( [( 'M', 'Male' ), ( 'F', 'Female' )], 'Gender', ),
               'dob': fields.date( 'Date of Birth' ),
               'cafatid': fields.char( 'CAFAT Number', size = 64 ),
               'amgid': fields.char( "N°AMG", size = 64 ),
               'PO_box':fields.char( 'PO box', size = 8 ),
               'partner_ids': fields.many2many( 'res.partner', 'res_partner_relation_rel', 'partner_id', 'related_id', 'Relations', domain = [( 'colleague', '=', True )] ),
               # domain pour n'avoir que les colleagues dans l'onglet Relations.
               'colleague': fields.boolean( 'Colleague' ),
               'trusted_partner_ids': fields.many2many( 'res.partner', 'res_partner_trusted_rel', 'partner_id', 'trusted_id', 'Trusted Partner', domain = ['|', '|', ( 'customer', '=', True ), ( 'trusted', '=', True ), ( 'colleague', '=', True )] ),
               'amgid': fields.char( "N°AMG", size = 64 ),
               'PO_box':fields.char( 'PO box', size = 8 ),
               'partner_ids': fields.many2many( 'res.partner', 'res_partner_relation_rel', 'partner_id', 'related_id', 'Relations', domain = [( 'colleague', '=', True )] ),
               # domain pour n'avoir que les colleagues dans l'onglet Relations.
               'colleague': fields.boolean( 'Colleague' ),
               'trusted':fields.boolean( 'Trusted', help = 'Used for partner which are a trusted budy for an other patient' ),
               'trusted_partner_ids': fields.many2many( 'res.partner', 'res_partner_trusted_rel', 'partner_id', 'trusted_id', 'Trusted Partner', domain = ['|', '|', ( 'customer', '=', True ), ( 'trusted', '=', True ), ( 'colleague', '=', True )] ),
               'comment_secure':fields.text( 'Secured Comment', help = 'Comment not to be shared' ),
               'age': fields.function( _get_age, method = True, type = 'char', string = 'Age', multi = 'all' ),
               }
    def name_get( self, cr, uid, ids, context = None ):
        """
        Returns the preferred display value (text representation) 
        for the records with the given ids. 
        By default this will be the value of the "name" column, 
        unless the model implements a custom behavior.
        
        @Return: type:list(tuple)
        @Returns: list of pairs (id,text_repr) for all records with the given ids.
        """
        _logger.info( 'in name_get of res.partner model ...' )
        if context is None:
            context = {}
        if isinstance( ids, ( int, long ) ):
            ids = [ids]
        res = []
        for record in self.browse( cr, uid, ids, context = context ):
            name = record.name
            if record.firstname:
                name += ', ' + record.firstname
            if record.dob:
                name += ', (' + str( record.dob ) + ')'
            if record.parent_id:
                name = "%s (%s)" % ( name, record.parent_id.name )
            if context.get( 'show_address' ):
                name = name + "\n" + self._display_address( cr, uid, record, without_company = True, context = context )
                name = name.replace( '\n\n', '\n' )
                name = name.replace( '\n\n', '\n' )
            if context.get( 'show_email' ) and record.email:
                name = "%s <%s>" % ( name, record.email )
            if record.age:
                name += ' / (' + str( record.age ) + ')'
            if record.gender:
                name += '(' + record.gender + ')'
            res.append( ( record.id, name ) )
            _logger.info( 'getting out of res.partner name_get' )
        return res
    
    def schedule_meeting_all( self, cr, uid, ids, context = None ):
        partner_ids = list( ids )
        partner_ids.append( self.pool.get( 'res.users' ).browse( cr, uid, uid ).partner_id.id )
        res = self.pool.get( 'ir.actions.act_window' ).for_xml_id( cr, uid, 'calendar', 'action_calendar_event', context )
        res['context'] = {
                          'default_partner_ids':partner_ids,
                          'default_partner_id':partner_ids and partner_ids[0] or False,
                          'search_default_open_meeting':True
                          }
        return res
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
