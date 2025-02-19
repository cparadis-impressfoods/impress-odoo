
import werkzeug
from collections import OrderedDict
from operator import itemgetter

from odoo import conf, http, _
from odoo.addons.portal.controllers import portal
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.tools import groupby as groupbyelem


import logging

_logger = logging.getLogger(__name__)

class CustomerPortal(portal.CustomerPortal):

    @http.route(['/my/manufacturings','/my/manufacturings/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_manufacturings(self, page=1, date_begin=None, date_end=None, sortby='date', filterby='all', groupby='none', so=None, product=None):
        commercial_partner = request.env.user.partner_id.commercial_partner_id
        SaleOrder = request.env['sale.order']
        
        # If no SO is specified, get all SOs for the user
        if so == None:
            so_domain = [('partner_id', '=', commercial_partner.id)]
            so_ids = [so.id for so in SaleOrder.search(so_domain)]
        else:
            # If SO is specified, cast the SO id to an int and make it the search domain
            so_ids = [int(so)]
        
        domain = [('billing_sale_order_id', 'in', so_ids)]
        
        if product != None:
            product_domain = [('product_id', '=', int(product))]
            domain += product_domain
        
        values = self._prepare_manufacturings_values(domain, page, date_begin, date_end, sortby, filterby, groupby)

        return http.request.render('impress_production_billing.portal_my_manufacturings', values)

    @http.route("/my/manufacturings/<int:manufacturing_id>", type="http", auth="user", methods=['GET'], website=True)
    def portal_my_manufacturing(self, manufacturing_id):
        try:
            self._document_check_access('mrp.production', manufacturing_id)
        except (AccessError, MissingError):
            return request.redirect('/my')

        manufacturing = request.env['mrp.production'].browse(manufacturing_id)
        return request.render(
            'impress_production_billing.manufacturing_portal', 
            {'manufacturing': manufacturing}
        )

    @http.route("/my/manufacturings/<int:manufacturing_id>/manufacturing_portal", type="http", auth="user", methods=['GET'])
    def render_manufacturing_backend_view(self, manufacturing_id):
        try:
            manufacturing = self._document_check_access('mrp.production', manufacturing_id)
        except (AccessError, MissingError):
            raise werkzeug.exceptions.NotFound
       
        session_info = request.env['ir.http'].session_info()
        user_context = dict(request.env.context) if request.session.uid else {}
        mods = conf.server_wide_modules or []
        lang = user_context.get("lang")
        translation_hash = request.env['ir.http'].get_web_translations_hash(mods, lang)
        cache_hashes = {
            "translations": translation_hash,
        }
        production_company = manufacturing.company_id
        session_info.update(
            cache_hashes=cache_hashes,
            action_name='impress_production_billing.manufacturing_portal_view_production_action',
            manufacturing_id=manufacturing.id,
            user_companies={
                'current_company': production_company.id,
                'allowed_companies': {
                   production_company.id: {
                       'id': production_company.id,
                        'name': production_company.name,
                    },
                },
            }
        )


        return request.render(
            'impress_production_billing.manufacturing_portal_embed',
            {'session_info': session_info},
        )


    def _get_searchbar_filters(self):
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'done': {'label': _('Done'), 'domain': [('state', '=', 'done')]},
            'confirmed': {'label': _('Confirmed'), 'domain': [('state', '=', 'confirmed')]},
        }
        return searchbar_filters

    def _get_searchbar_groupby(self):

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'product': {'input':'product', 'label': _('Product')},
            'purchase_order': {'input':'purchase_order', 'label': _('Purchase Order')},
            'state': {'input':'state', 'label': _('Status')}
        }
        return searchbar_groupby

    def _get_searchbar_sortings(self):
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc, id desc'},
            'name': {'label': _('Name'), 'order': 'name asc, id asc'},
        }
        return searchbar_sortings

    def _production_get_groupby_mapping(self):
        return {
            'product': 'product_id',
            'purchase_order': 'billing_sale_order_id',
            'state': 'state'
        }

    def _prepare_manufacturings_values(self, domain, page, date_begin, date_end, sortby, filterby, groupby):
        ProductionOrder = request.env['mrp.production']

        searchbar_filters = self._get_searchbar_filters()
        searchbar_groupby = self._get_searchbar_groupby()
        searchbar_sortings = self._get_searchbar_sortings()
        
        domain += searchbar_filters[filterby]['domain']
        order = searchbar_sortings[sortby]['order']


        # Default sort by value
        if not sortby or sortby not in searchbar_sortings:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']



        count = 0
        pager = portal_pager(
            url='/my/manufacturings',
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=count,
            page=page,
            step=self._items_per_page
        )

        mo_ids = ProductionOrder.search(
            domain, 
            order=order, 
            limit=self._items_per_page, 
            offset=pager['offset']
        )


        def get_grouped_manufacturings(pager_offset):
            productions = ProductionOrder.search(
                domain, 
                order=order, 
                limit=self._items_per_page, 
                offset=pager_offset
            )
        
            groupby_mapping = self._production_get_groupby_mapping()
            group = groupby_mapping.get(groupby)
            if group:
                grouped_productions = [ProductionOrder.concat(*g) for k, g in groupbyelem(productions, itemgetter(group))]
            else:
                grouped_productions = [productions] if productions else []
            
            production_states = dict(ProductionOrder._fields['state']._description_selection(request.env))
            if sortby == "status":
                if groupby == 'none' and grouped_productions:
                    grouped_productions[0] =  grouped_productions[0].sorted(lambda productions: production_states.get(productions[0].state))
                else:
                    grouped_productions.sort(key=lambda productions: production_states.get(productions[0].state))
            return grouped_productions


        count = ProductionOrder.search_count(domain)
        values = {
            'date': date_begin,
            'manufacturings': mo_ids,
            'grouped_productions': get_grouped_manufacturings,
            'page_name': 'manufacturing',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'searchbar_groupby': searchbar_groupby,
            'groupby': groupby,
            'default_url': '/my/manufacturings',
            
        }
        #_logger.warning(values)
        return values