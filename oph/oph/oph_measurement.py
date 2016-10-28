# -*- coding: utf-8 -*-
import logging
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import time
from datetime import datetime
import settings
from decimal import Decimal

_logger = logging.getLogger( __name__ )

# #-- objects intermédiaires
# #-- configurable.
def seq( start, stop, step = 1 ):
    """Return a list of float
    return eg : [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    with start=2 ; end=10; step =0.5
    """
    n = int( round( ( stop - start ) / float( step ) ) )
    if n > 1:
        return( [start + step * i for i in range( n + 1 )] )
    else:
        return( [] )

class oph_measurement_type( orm.Model ):
    """
    Table for all the measurement type
    EG: Tonometry, Keratometry, VA, Slit Lamp exam...
    """
    _name = "oph.measurement.type"
    _columns = {
              'name':fields.char( 'Name', size = 64 ),
              'code':fields.char( 'Code', size = 64 ),
              }

class oph_va_tech( orm.Model ):
    """
    Can be everything you want
    Usely red-green test and Jackson Cross cylinder
    """
    _name = 'oph.va.tech'
    _columns = {
              'name':fields.char( 'Name', size = 32 ),
              }

class oph_todolist_tag( orm.Model ):
    """
    Set the desired priority for todolist.
    Can be everything you want
    Usely: High, Low, Normal
    
    """
    _name = 'oph.todolist.tag'

    def onchange_set_default( self, cr, uid, ids, context ):
        if context is None:
            context = {}
        res = self.search( cr, uid, [( 'default', '=', True )], context = context )
        self.write( cr, uid, res, {'default':False}, context = context )
        return {'value':{'default':True}}

    _columns = {
              'name':fields.char( 'Name', size = 32 ),
              'default':fields.boolean( 'Default', help = 'Thick the box if you want it to be default if not thick another' ),
              }


class oph_measurement( orm.Model ):
    _name = "oph.measurement"
    _order = "date"

    def on_change_near( self, cr, uid, ids, sph, add, context = None ):
        """
        """
        _logger.info( 'In on_chang_near' )
        pass
    
    def on_change_va( self, cr, uid, ids, va_or, context = None ):
        """copy va_or to va_os"""
        return {'value':{'va_os':va_or}
                }

    def on_change_add( self, cr, uid, ids, add_or, context = None ):
        return {'value':{'add_os':add_or}
                }

    def on_change_nv( self, cr, uid, ids, nv_or, context = None ):
        return {'value':{'nv_os':nv_or}
                }

    def on_change_sph( self, cr, uid, ids, sph_or, context = None ):
        return {'value':{'sph_os':sph_or}
                }

    def on_change_m( self, cr, uid, ids, m_or, context = None ):
        return {'value':{'m_os':m_or}
                }

    def on_change_axis( self, cr, uid, ids, axis_or, context = None ):
        return {'value':{'axis_os':axis_or}
                }

    def on_change_cyl( self, cr, uid, ids, cyl_or, context = None ):
        return {'value':{'cyl_os':cyl_or}
                }

    def on_change_kod( self, cr, uid, ids, k_or, context = None ):
        return {'value':{'k2_or':k_or}
                }

    def on_change_kos( self, cr, uid, ids, k_os, context = None ):
        return {'value':{'k2_os':k_os}
                }

    def _get_type( self, cr, uid, context = None ):
        # print "JE PASSE PAR _GET_TYPE. context.get('measurement_type') is:", context.get('measurement_type')
        # print "CONTEXT is:", context
        if context == None:
            context = {}
        res = False
        if context.get( 'measurement_type' ):
            res = self.pool.get( 'oph.measurement.type' ).search( cr, uid, [( 'code', '=', context.get( 'measurement_type' ) )], context = context )
            print "RES is:%s" % ( res, )
        # print "_GET_TYPE RETURN :", res and res[0] or False
        return res and res[0] or False

    def _get_va_type( self, cr, uid, context = None ):
        va_type_selection = ( 
                            ( 'UCVA', _( 'UCVA' ) ),  # uncorrected visual acuity
                            ( 'CVA', _( 'CVA' ) ),
                            ( 'BCVA', _( 'BCVA' ) ),  # best corrected visual acuity
                            ( 'MAVC sous cycloplegique', 'MAVC sous cycloplegique' ),
                            ( 'Rx', _( 'Refraction prescription' ) ),  # refraction prescrite
                            ( 'AR', _( 'AutoRefractometer' ) ),
                            )
        return va_type_selection

    def _get_va( self, cr, uid, context = None ):
        # print "JE PASSE PAR _GET_AV"
        va_selection = ( 
                      ( 'PL-', 'PL-' ),
                      ( 'PL+', 'PL+' ),
                      ( 'CLD', 'CLD' ),
                      ( 'VLMB', 'VLMB' ),
                      ( '0.5/10', '0.5/10' ),
                      ( '1/10', '1/10' ),
                      ( '2/10', '2/10' ),
                      ( '3/10', '3/10' ),
                      ( '4/10', '4/10' ),
                      ( '5/10', '5/10' ),
                      ( '6/10', '6/10' ),
                      ( '7/10', '7/10' ),
                      ( '8/10', '8/10' ),
                      ( '9/10', '9/10' ),
                      ( '10/10', '10/10' ),
                      ( '12/10', '12/10' ),
                      )
        return va_selection

    def _get_sph( self, cr, uid, context = None ):
        """
        Return a tuple of tuple
        of str with + if positive
        Wich will be cleaner for Rx prescription than without the + sign
        confusing with or without + could be - minus sign for opticiens
        """
        seq_sph = seq( settings.CONST.START_SPH, settings.CONST.STOP_SPH, settings.CONST.STEP_SPH )
        seq_sph = ['+' + str( i ) if i >= 0 else str( i ) for i in seq_sph ]
        # seq_sph = [str(i) for i in seq_sph]
        sph_selection = zip( seq_sph, seq_sph )
        return tuple( sph_selection )

    def _get_axis( self, cr, uid, context = None ):
        suffixe = '°'
        seq_axis = seq( settings.CONST.START_AXIS, settings.CONST.STOP_AXIS, settings.CONST.STEP_AXIS )
        seq_axis_suffixed = [str( i ) + '°' for i in seq_axis]
        seq_axis = [str( i ) for i in seq_axis]
        axis_selection = zip( seq_axis, seq_axis_suffixed )
        return tuple( axis_selection )

    def _get_cyl( self, cr, uid, context = None ):

        seq_cyl = seq( settings.CONST.START_CYL, settings.CONST.STOP_CYL, settings.CONST.STEP_CYL )
        seq_cyl = [str( i ) for i in seq_cyl]
        seq_cyl.reverse()
        cyl_selection = zip( seq_cyl, seq_cyl )
        return tuple( cyl_selection )

    def _get_nearva( self, cursor, user_id, context = None ):
        parinaud = ( 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P14', 'R1/2' )
        res = zip( parinaud, parinaud )
        res = tuple( res )
        return res

    def _ods_get( self, cr, uid, context = None ):
        return [
                ( 'OD', _( 'Right Eye' ) ),
                ( 'OS', _( 'Left Eye' ) ),
                ]

    def _get_add( self, cr, uid, context = None ):
        add = ( ( '+0.5', '0.5' ),
             ( '+0.75', '0.75' ),
             ( '+1.00', '1.00' ),
             ( '+1.25', '1.25' ),
             ( '+1.50', '1.50' ),
             ( '+1.75', '1.75' ),
             ( '+2.00', '2.00' ),
             ( '+2.25', '2.25' ),
             ( '+2.50', '2.50' ),
             ( '+2.75', '2.75' ),
             ( '+3.00', '3.00' ),
             )
        return add

    def _get_qualif( self, cursor, user_id, context = None ):
        return ( 
                ( '1l', '1 lettre' ),
                ( '2l', '2 lettres' ),
                ( '3l', '3 lettres' ),
                ( '4l', '4 lettres' ),
                )

    def _get_meta( self, cursor, user_id, context = None ):
        return ( ( 'M-', 'M-' ), ( 'M+', 'M+' ), ( 'M++', 'M++' ), )

    _columns = {
              'name':fields.char( 'Name', size = 64 ),
              'type_id':fields.many2one( 'oph.measurement.type', 'Type' ),
              'meeting_id':fields.many2one( "calendar.event", "Meeting" ),
              'partner_id':fields.related( "meeting_id", "partner_id", type = "many2one", relation = "res.partner", string = "Partner", store = True, readonly = True, ),
              'date':fields.related( 'meeting_id', 'start_date', type = 'date', string = 'Consultation Date', store = True ),
             # 'chief_complaint':fields.related('meeting_id', 'chief_complaint', type = 'char', string = 'Chief Complaint',),
             # 'motive':fields.related('meeting_id', 'motive', type = 'many2one', relation = 'oph.motive', store = True, string = "Motive"),
              # Tonometry
              'tonometer_id':fields.many2one( 'oph.instrumentation', 'Tonometer' ),
              'iop_or':fields.integer( 'IOP_OD' ),
              'iop_os':fields.integer( 'IOP_OS' ),
              'comment_iop':fields.text( 'Comment' ),
              # --keratometry
              'keratometer_id':fields.many2one( 'oph.instrumentation', 'Keratometer' ),
              'k1_or':fields.float( 'K1_OD', digits = ( 3, 2 ) ),
              'k2_or':fields.float( 'K2_OD', digits = ( 3, 2 ) ),
              'k1_os':fields.float( 'K1_OS', digits = ( 3, 2 ) ),
              'k2_os':fields.float( 'K2_OS', digits = ( 3, 2 ) ),
              # -- visual acuity
              'va_type':fields.selection( _get_va_type, 'VA TYPE', ),  # BVC, ...>
              'va_tech':fields.many2one( 'oph.va.tech', 'Technique', ),  # Cross cylinder, pifometre, brouillage, rouge-vert...
              'va_od':fields.selection( _get_va, 'VA_OD' ),
              'qualif_or':fields.selection( _get_qualif, 'QUALIF_OD', ),
              'va_os':fields.selection( _get_va, 'VA_OS' ),
              'qualif_os':fields.selection( _get_qualif, 'Qualif_OS' ),
              'nv_or':fields.selection( _get_nearva, 'NV_OD' ),
              'nv_os':fields.selection( _get_nearva, 'NV_OS' ),
              # -- visual acuity
              'va_or':fields.char( 'VA OR', size = 5 ),
              'va_ol':fields.char( 'VA OL', size = 5 ),
              'va_or_extended':fields.char( 'VA OR Ext', size = 7 ),
              'va_ol_extended':fields.char( 'VA OR Ext', size = 7 ),
              # -- binocular visual acuity
              'va_bin':fields.char( 'Binocular VA', size = 5 ),
              'va_bin_extended':fields.char( 'Binocular VA', size = 7 ),
              # --- metamorphopsia
              'm_or':fields.selection( _get_meta, 'METAMORPHOPSIA_OD', ),
              'm_os':fields.selection( _get_meta, 'METAMORPHOPSIA_OS', ),
              # -- refraction -- far SCA and ADD
              'sph_or':fields.selection( _get_sph, 'SPH_OD', ),
              'cyl_or':fields.selection( _get_cyl, 'CYL_OD', ),
              'axis_or':fields.selection( _get_axis, 'AXIS_OD', ),
              'add_or':fields.selection( _get_add, 'ADD_OD' ),
              'sph_os':fields.selection( _get_sph, 'SPH_OS', ),
              'cyl_os':fields.selection( _get_cyl, 'CYL_OS', ),
              'axis_os':fields.selection( _get_axis, 'AXIS_OS', ),
              'add_os':fields.selection( _get_add, 'ADD_OS' ),
              # -- for formula prescription only
              # rp (reading prescription) = sph + add
              'rp_or':fields.char( 'Reading Pres', size = 8 ),
              'rp_os':fields.char( 'Reading Pres', size = 8 ),
              # -- slit lamp exam
              'as_or':fields.text( 'AS_OR' ),
              'ps_or':fields.text( 'PS_OR' ),
              'as_os':fields.text( 'AS_OS' ),
              'ps_os':fields.text( 'PS_OS' ),
              # --pachymetry
              'cct_or':fields.integer( 'CCT_OR' ),  # CCT for Central Corneal Thickness
              'cct_os':fields.integer( 'CCT_OS' ),
              # --conclusion
              'conclusion':fields.text( 'Conclusion' ),
              'conclusion_or':fields.text( 'Conclusion OR' ),
              'conclusion_os':fields.text( 'Conclusion OS' ),
              'weight':fields.integer( 'Weight' ),
              'comment_misc':fields.text( 'Comment' ),
              }

    _defaults = {
        'type_id': lambda s, cr, uid, c: s._get_type( cr, uid, context = c ),
        'va_type':'BCVA',
                }

    def compute_rp( self, cr, uid, sph, add, context = None ):
        """
        param: sph type str
        param: add type str
        Return a str with + sign if positive
        """
        res = float( sph ) + float( add )
        if res >= 0:
            return '+' + str( res )
        else:
            return str( res )

    def mavc2cp( self, cr, uid, ids, context = None ):
        """Set a prescription formula record from MAVC
        """

        print "IN MAVC2CP"
        print "ids:%s" % ids
        print "context:%s" % context
        if context is None:
            context = {}
        cp = self.browse( cr, uid, ids, context = context )
        print "cp:%s" % cp

        for i in cp:
            print 'i.type_id: %s' % i.type_id.id
            print 'i type_id.code: %s' % i.type_id.code
            vals = {
               # 'type_id':2,
               'type_id': i.type_id.id,
               'va_type':'Rx',
               'partner_id':i.partner_id.id,
               'meeting_id':i.meeting_id.id,
               # OD
               'va_or':i.va_or,
               'sph_or':i.sph_or,
               'cyl_or':i.cyl_or,
               'axis_or':i.axis_or,
               'add_or':i.add_or,
               'rp_or':self.compute_rp( cr, uid, i.sph_or, i.add_or ),
               # OS
               'va_os':i.va_os,
               'sph_os':i.sph_os,
               'cyl_os':i.cyl_os,
               'axis_os':i.axis_os,
               'add_os':i.add_os,
               'rp_os':self.compute_rp( cr, uid, i.sph_os, i.add_os ),
               }
        self.create( cr, uid, vals, context = context )
        return True

class oph_todolist( orm.Model ):
    """
    TODO LIST for patients
    """
    _name = 'oph.todolist'

    def statechange_open( self, cr, uid, ids, context = None ):
        self.write( cr, uid, ids, {"state": "open"}, context = context )
        return True
    def statechange_close( self, cr, uid, ids, context = None ):
        self.write( cr, uid, ids, {"state": "close"}, context = context )
        return True
    def statechange_draft( self, cr, uid, ids, context = None ):
        self.write( cr, uid, ids, {"state": "draft"}, context = context )
        return True

    def _get_state( self, cr, uid, context = None ):
        todolist_selection = ( 
                            ( 'draft', _( 'Draft' ) ),
                            ( 'open', _( 'Open' ) ),
                            ( 'close', _( 'Close' ) ),
                            )
        return todolist_selection

    def _default_get( self, cr, uid, context = None ):
        """
        get the default value of tag_id
        """
        print "DEFAULT_GET"
        tag_obj = self.pool.get( 'oph.todolist.tag' )
        res = tag_obj.search( cr, uid, [( 'default', '=', True )], context = context )
        res = tag_obj.read( cr, uid, res, fields = ['name'], context = context )
        return str( res[0].get( 'id' ) ) or 1

    def _tag_id_selection( self, cr, uid, context = None ):
        tag_id_obj = self.pool.get( 'oph.todolist.tag' )
        # tag_ids = tag_id_obj.search(cr, uid, [('default', '=', True), ], context = context)
        tag_ids = tag_id_obj.search( cr, uid, [], context = context )
        if tag_ids:
            res = tag_id_obj.read( cr, uid, tag_ids, ['name'], context = context )
            return [( str( r['id'] ), r['name'] ) for r in res]
        return True

    _columns = {
              'name':fields.char( 'Name', size = 32 ),
              'state':fields.selection( _get_state, 'State', ),
              'meeting_id':fields.many2one( "calendar.event", "Meeting" ),
              'partner_id':fields.related( "meeting_id", "partner_id", type = "many2one", relation = "res.partner", string = "Partner", store = True, readonly = True, ),
              'date':fields.related( 'meeting_id', 'date', type = 'date', string = 'Consultation Date', store = True ),
              # 'tag_id':fields.many2one('oph.todolist.tag', 'Priority'),
              # switching to a selection for using the _default_get method
              'tag_id':fields.selection( _tag_id_selection, 'Priority' ),
              'comment':fields.char( 'Comment', size = 128 ),
              }

    _defaults = {
               'state':'draft',
               'tag_id':_default_get,
               }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
