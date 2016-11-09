# -*- coding: utf-8 -*-

from openerp.tools.translate import _
from openerp.osv import osv, fields
from datetime import datetime, timedelta
import pytz
import arrow
import inspect
import logging

_logger = logging.getLogger( __name__ )
_logger.setLevel( logging.DEBUG )


class agenda_factory( osv.osv_memory ):
    '''
    '''
    _name = "agenda.factory"
    _description = "Agenda factory. Set up of slots"  # Mise en place des crénaux"


#     def _get_tag_agenda( self, cursor, user_id, context = None ):
#         return ( 
#                 ( 'cs', 'Consultation' ),
#                 ( 'tech', 'Technique' ),
#                 ( 'close', 'Close' ),
#                 )

    def onetotwodigit( self, hm ):
        """
        hm type : str
        """
        f = '0{0}'
        if len( hm ) < 2:
            return f.format( *hm )
        else:
            return hm

    def complete( self, hm ):
        """Return a complete hm with 
        HH:mm:ss 
        filling with 00 as necessary
        
        hm : list of string
        
        return : list of string 
        """
        while len( hm ) < 3:
            hm.append( '00' )
        return hm

    def hm_format( self, hm ):
        """Format a string time to : HH:mm:ss
        
        hm : str 
        hm : eg 8 ; 08 ; 8:20
        
        return : str '08:00:00' ; '08:00:00', '08:20:00'
        
        """
        #=======================================================================
        # res=hm.split(':') # decoupe et crée une liste
        # res=map(self.onetotwodigit, res) # rajoute des zero si nécessaire dans les élément de la liste.
        # res=complete(res) # rajoute des '00' à la liste temps que len <3
        # res=res.join(':') # recrée la str 00:00:00
        #=======================================================================
        _logger.info( 'hm is : %s', hm )
        res = ''
        try:
            res = self.complete( map( self.onetotwodigit, hm.split( ':' ) ) )
            res = ':'.join( res )  # convert list to string
            _logger.info( "complete(map(self,onetotwodigit,hm.split(':'))) %s", hm )
        except AttributeError:
            _logger.warning( 'the %s is not good', hm )
        
        _logger.info( 'returning res: %s', res )
        return res

    def shift( self, aw, step ):
        """
        Skip aw ahead of step
        
        :param aw: arrow object
        :param step: integer (minutes)
        :returns: arrow object, step minutes later
        :rtype: arrow
        """
        return aw.replace( minutes = +step )

    def onchange_start( self, cr, uid, ids, hm, context = None ):
        """
        TODO Pourquoi il n'y pas de changement dans les views
        
        """
        # print "ONCHANGE_START"
        if context is None:
            context = {}
        res = {'values':{}}
        res['values'] = {
                       'start_h':self.hm_format( hm ),
                       }
        return res

    def onchange_end( self, cr, uid, ids, hm, context = None ):
        """
        TODO Pourquoi il n'y pas de changement dans les views
        """
        # print "ONCHANGE_END"
        if context is None:
            context = {}
        res = {'values':{}}
        res['values'] = {'end_h':self.hm_format( hm ), }
        _logger.info( "returning : %s", res )
        # print "RES:%s" % res
        return res

    def strdate2arrow( self, dt, hm = None, context = None ):
        """
        Return an arrow object in UTC
        
        :param dt: datetime.
        :type dt: string can be a string with or without time informations
        :param hm: time 
        :type hm: string can be "8" or "08" for 8h must be converted to a formated time "HH-mm-ss"
        :returns date wih time
        :rtype: arrow
        :example:
        
        strdate2arrow('2012-10-18', 08:30')
        <arrow
        """
        #=======================================================================
        # Est ce qu'un champ date subit une modification à cause des TZ
        # quand il est inséré dans la database.
        # si on veut utiliser le hm (HH:mm:ss)
        # Comme on récupère une string en UTC
        #
        #=======================================================================
        if context is None:
            context = {}
        _logger.info( 'context is : %s', context )

        if hm:
            hm = self.hm_format( hm )
            hm = dict( zip( ['hour', 'minute'], [int( x ) for x in hm.lstrip( '0' ).split( ':' ) ] ) )
            _logger.info( "hm is : %s", hm )
            arw = arrow.get( dt ).replace( hour = hm['hour'], minute = hm['minute'] ).replace( tzinfo = context.get( 'tz', None ) ).to( 'UTC' )
            _logger.info( "Return Arrow: %s", aw )
            return arw
        else:
            return arrow.get( dt )
            _logger.info( "Return Arrow : %s", arrow.get( dt ) )

    def make_slots( self, rec, fmt = 'YYYY-MM-DD HH:mm:ss' ):
        """
        Make the slots as arrow object
        
        :param rec: record from database 
        :type rec: dictionnary
        .. warning:: rec must have the 'start' and 'stop' and 'step' keys
        :param fmt: formatting string
        .. note:: fmt is always 'YYYY-MM-DD HH:mm:ss'
        :type fmt: str
        :return an iterable of the start and stop datetime for the slots.
        :rtype list of tuple
        
        :example:
        
        make_slots({'start':'2013-10-18 08:30:00', 'stop':'2013-10-18 10:00:00','step':15})
        [(<Arrow [2013-10-18T08:30:00+00:00]>, <Arrow [2013-10-18T08:45:00+00:00]>), 
        (<Arrow [2013-10-18T08:45:00+00:00]>, <Arrow [2013-10-18T09:00:00+00:00]>), 
        (<Arrow [2013-10-18T09:00:00+00:00]>, <Arrow [2013-10-18T09:15:00+00:00]>), 
        (<Arrow [2013-10-18T09:15:00+00:00]>, <Arrow [2013-10-18T09:30:00+00:00]>), 
        (<Arrow [2013-10-18T09:30:00+00:00]>, <Arrow [2013-10-18T09:45:00+00:00]>), 
        (<Arrow [2013-10-18T09:45:00+00:00]>, <Arrow [2013-10-18T10:00:00+00:00]>)]
        """
        l = list()
        ll = list()

        for key in ['start', 'stop']:
            val = arrow.get( rec[key], fmt )
            rec[key] = val
        while ( rec['start'] < rec['stop'] ):
            l.append( rec['start'] )
            rec['start'] = self.shift( rec['start'], rec['step'] )
            ll.append( rec['start'] )
            _logger.info( 'zip(I,II) : %s', zip( I, II ) )
        return zip( l, ll )

    def create_slot( self, cr, uid, ids, context = None ):
        """ Create slots calendar.event meeting
        step: slot duration
        
        JE PEnSE QUE Le SYSTEME RENVOIE DEJA DES ARROW
        """
        print "PASSING in %s / CONTEXT:%s" % ( inspect.stack()[0][3], context )

        fmt = 'YYYY-MM-DD HH:mm:ss'
        l = list()
        ll = list()
        if context is None:
            context = {}
        res = self.read( cr, uid, ids, ['date', 'start_dt', 'stop_dt', 'step', 'ampm', 'start_h', 'end_h', 'day_on', 'day_off', 'name', 'tag', 'state', 'user_id'], context = None )
        _logger.info( "data of the wizard: %s", res )
        _logger.info( "type of res : %s", type( res ) )
        # from pdb import set_trace;set_trace()
        res = res[0]  # seul le premier enregistrement nous intéresse
        # --
        if res['ampm'] == 'afternoon' or res['ampm'] == 'morning':
            for key in ( 'start_h', 'end_h' ):
                dt = res['date'] + ' ' + self.hm_format( res[key] )  # dt eg u'2016-06-03 12:00:00'
                val = arrow.get( dt, fmt ).replace( tzinfo = context.get( 'tz', None ) ).to( 'UTC' )  # convert to arrow aware of tz eg <Arrow [2016-06-03T01:00:00+00:00]>
                res[key] = val  # récupére les datetime pour en faire des arrow obj et les injecte dans le dictionnaire
            while ( res['start_h'] < res['end_h'] ):
                l.append( res['start_h'] )
                res['start_h'] = self.shift( res['start_h'], res['step'] )
                ll.append( res['start_h'] )
                _logger.info( "II.append is : %s ", ll )
            p = zip( l, ll )
            _logger.info( 'zip(I,II): %s', zip( l, ll ) )
            for ( begin, end ) in p:
                _logger.info( "begin, end: %s ; %s", begin, end )
                if res['tag'] in ['cs', 'tech']:
                    tag = res['tag']
                else:
                    tag = False
               # _logger.info('begin:%s, stop_datetime: %s ,name: %s, state: %s, tag: %s', (begin,end,res['name'],res['state'], tag,))
                vals = {
                      'start_datetime':begin.format( fmt ),
                      'stop_datetime':end.format( fmt ),
                      'name':res['name'],
                      'tag': tag,
                      'state':res['state'],
                      'user_id':res['user_id'][0]
                      }
                _logger.info( 'vals: %s', vals )
                self.pool.get( 'calendar.event' ).create( cr, uid, vals, context = None )
        # --
        elif ( res['ampm'] == 'daylong' ):
            for key in ( 'day_on', 'day_off', 'start_h', 'end_h' ):
                dt = res['date'] + ' ' + self.hm_format( res[key] )
                val = arrow.get( dt, fmt ).replace( tzinfo = context.get( 'tz', None ) ).to( 'UTC' )
                _logger.info( 'val: %s', val )
                res[key] = val
                
            # -- morning
            while ( res["day_on"] < res['start_h'] ):
                l.append( res['day_on'] )
                res['day_on'] = self.shift( res['day_on'], res['step'] )
                ll.append( res['day_on'] )
            p = zip( l, ll )
            _logger.info( "zip(l,ll): %s", p )
            for ( begin, end ) in p:
                if res['state'] in ['cs', 'tech']:
                    tag = res['state']
                else:
                    tag = False
                _logger.info( "begin, end; %s, %s", begin, end )
                vals = {
                      'start_datetime':begin.format( fmt ),
                      'stop_datetime':end.format( fmt ),
                      'name':res['name'],
                      'state':res['state'],
                      'tag': tag,
                      'state':res['state'],
                      'user_id':res['user_id'][0]
                      }
                _logger.info( 'vals : %s', vals )
                self.pool.get( 'calendar.event' ).create( cr, uid, vals, context = None )

            l = list()
            ll = list()
            while ( res["end_h"] < res['day_off'] ):
                l.append( res['end_h'] )
                res['end_h'] = self.shift( res['end_h'], res['step'] )
                ll.append( res['end_h'] )
            p = zip( l, ll )
            # import pdb;pdb.set_trace()
            for ( begin, end ) in p:
                if res['state'] in ['cs', 'tech']:
                    tag = res['state']
                else:
                    tag = False
                vals = {
                      'start_datetime':begin.format( fmt ),
                      'stop_datetime':end.format( fmt ),
                      'name':res['name'],
                      'state':res['state'],
                      'tag': tag,
                      'state':res['state'],
                      'user_id':res['user_id'][0]}
                _logger.info( 'vals : %s', vals )
                self.pool.get( 'calendar.event' ).create( cr, uid, vals, context = None )
            return True
        else:
                return {}

    _columns = {
                'name':fields.char( 'Name', size = 8, help = "Name for the open slots to be created" ),
                'date':fields.date( 'Date', help = 'Day for slot to create' ),
                "start_dt" : fields.datetime( "Start", help = "First appointment  datetime" ),
                "stop_dt": fields.datetime( "Stop", help = "Last appointement  datetime" ),
                "step" : fields.integer( "Duration", help = "Duration of the slot (minutes)" ),
                "ampm": fields.selection( ( ( "morning", _( "Morning" ) ), ( "afternoon", _( "Afternoon" ) ), ( "daylong", _( "All day" ) ) ), "Day" ),
                "start_h":fields.char( 'Start', size = 16, help = "Starting hour, eg: 08:00. Or starting of breakfast time for All day" ),
                "end_h":fields.char( 'Stop', size = 16, help = "End period. eg: 12:00. This will be the end of the last slot, not the last slot. Or end of brakfast time for the All day" ),
                "day_on":fields.char( 'Day On', size = 16, help = "Start of the day" ),
                "day_off":fields.char( 'Day Off', size = 16, help = "End of the day" ),
                "tag": fields.selection( [
                                            ( 'cs', 'Consultation' ),
                                            ( 'tech', 'Technique' ),
                                            # ( 'close', 'Close' ),
                                            ],
                                           'Type', readonly = False ),
                'state':fields.selection( [
                                          ( 'open', 'Open' ),
                                          ( 'close', 'Close' )
                                          ], "State" ),
                "user_id": fields.many2one( 'res.users', 'Responsible' ),
                }
    _defaults = {
                 'step': 15,
                 'name': 'Ouvert',
                 'ampm':'daylong',
                 'day_on':'08:00',
                 'day_off':'15:30',
                 'state':'open',
                }

agenda_factory()

# create(cr, user, vals, context=None)
# write(cr, user, ids, vals, context=None)¶


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
