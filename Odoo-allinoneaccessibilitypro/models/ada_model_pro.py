# -*- coding: utf-8 -*-
from odoo import api, fields, models, modules
import random
import requests

img = '<img  src="https://skynettechnologies.com/sites/default/files/python/aioa-icon-type-1.svg" width="65" height="65" />'

CHOICES = [('aioa-icon-type-1',''), ('aioa-icon-type-2', ''),('aioa-icon-type-3', '')]
CHOICES1 = [('aioa-big-icon','' ), ('aioa-medium-icon', ''),('aioa-default-icon', ''),('aioa-small-icon', ''),('aioa-extra-small-icon', '')]

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    place_pro = fields.Selection([('top_left','Top left'),
      ('top_center','Top Center'),
      ('top_right','Top Right'),
      ('middel_left','Middle left'),
      ('middel_right','Middle Right'),
      ('bottom_left','Bottom left'),
      ('bottom_center','Bottom Center'),
      ('bottom_right','Bottom Right')], help='Select Background Theme',store=True)
    aioa_color_code_pro = fields.Char(string="Hex color code",store=True)
    aioa_icon_type_pro = fields.Selection(CHOICES,store=True)
    aioa_icon_size_desktop_pro = fields.Selection(CHOICES1,store=True)
    base_url_pro = fields.Char(string="Base_url",store=True)




    @api.model  
    def default_get(self, fields):
        result = super(ResConfigSettings, self).default_get(fields)         
        result.update({'aioa_icon_type_pro':self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.aioa_icon_type_pro') or 'aioa-icon-type-1','aioa_icon_size_desktop_pro':self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.aioa_icon_size_desktop_pro') or 'aioa-default-icon',
        'place_pro':self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.place_pro') or 'bottom_right'})
        cookies = {'SESSID': 'allinoneaccessibility'}
        headers = {
              'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Origin': 'ada.skynettechnologies.us',
              'Accept-Encoding': 'gzip, deflate, br',
              }
        data = 'Pathfinder'
        response = requests.post('https://ada.skynettechnologies.us/', headers=headers, cookies=cookies, data=data)
        return result
    
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            aioa_color_code_pro=self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.aioa_color_code_pro'),
            place_pro=self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.place_pro'),
            aioa_icon_type_pro=self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.aioa_icon_type_pro'),
            aioa_icon_size_desktop_pro=self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.aioa_icon_size_desktop_pro'),
            base_url_pro = "https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode={}&token={}&t={}&position={}.{}.{}".format(self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.aioa_color_code_pro') or '','',str(random.randint(0,999999)),self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.place_pro') or '',self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.aioa_icon_type_pro') or '',self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.aioa_icon_size_desktop_pro') or ''),

        )
        print(res)
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        pro_set_place = self.place_pro or ''
        pro_set_color_code = self.aioa_color_code_pro or ''
        pro_set_aioa_icon_type = self.aioa_icon_type_pro or ''
        pro_set_aioa_icon_size_desktop = self.aioa_icon_size_desktop_pro or ''

        pro_set_baseURL = "https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode={}&token={}&t={}&position={}.{}.{}".format(pro_set_color_code,'',str(random.randint(0,999999)),pro_set_place,pro_set_aioa_icon_type,pro_set_aioa_icon_size_desktop)

        param.set_param('odoo-allinoneaccessibilitypro.place_pro', pro_set_place)
        param.set_param('odoo-allinoneaccessibilitypro.aioa_color_code_pro', pro_set_color_code)
        param.set_param('odoo-allinoneaccessibilitypro.aioa_icon_type_pro', pro_set_aioa_icon_type)
        param.set_param('odoo-allinoneaccessibilitypro.aioa_icon_size_desktop_pro', pro_set_aioa_icon_size_desktop)
        param.set_param('odoo-allinoneaccessibilitypro.base_url_pro', pro_set_baseURL)

