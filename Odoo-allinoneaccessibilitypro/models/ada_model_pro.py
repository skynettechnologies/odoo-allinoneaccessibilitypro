# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import requests
from urllib.parse import urlparse
from odoo.exceptions import UserError, ValidationError
img = '<img  src="https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-1.svg" width="65" height="65" />'
CHOICES = [
    ('aioa-icon-type-1', 'Icon Type-1'),
    ('aioa-icon-type-2', 'Icon Type-2'),
    ('aioa-icon-type-3', 'Icon Type-3'),
    ('aioa-icon-type-4', 'Icon Type-4'),
    ('aioa-icon-type-5', 'Icon Type-5'),
    ('aioa-icon-type-6', 'Icon Type-6'),
    ('aioa-icon-type-7', 'Icon Type-7'),
    ('aioa-icon-type-8', 'Icon Type-8'),
    ('aioa-icon-type-9', 'Icon Type-9'),
    ('aioa-icon-type-10', 'Icon Type-10'),
    ('aioa-icon-type-11', 'Icon Type-11'),
    ('aioa-icon-type-12', 'Icon Type-12'),
    ('aioa-icon-type-13', 'Icon Type-13'),
    ('aioa-icon-type-14', 'Icon Type-14'),
    ('aioa-icon-type-15', 'Icon Type-15'),

]

CHOICES1 = [('aioa-big-icon', 'Big Icon'), ('aioa-medium-icon', 'Medium Icon'), ('aioa-default-icon', 'Default Icon'), ('aioa-small-icon', 'Small Icon'), ('aioa-extra-small-icon', 'Extra Small Icon')]

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        called = self.env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.api_called')
        if not called:
            from .register_domain_api import run_accessibility_api_once
            run_accessibility_api_once(self.env)
            self.env['ir.config_parameter'].sudo().set_param('odoo-allinoneaccessibilitypro.api_called', 'True')
        return res

    place_pro = fields.Selection([('top_left', 'Top left'),
                                  ('top_center', 'Top Center'),
                                  ('top_right', 'Top Right'),
                                  ('middle_left', 'Middle left'),
                                  ('middle_right', 'Middle Right'),
                                  ('bottom_left', 'Bottom left'),
                                  ('bottom_center', 'Bottom Center'),
                                  ('bottom_right', 'Bottom Right')], 
                                 help='Select Background Theme', store=True)

    aioa_color_code_pro = fields.Char(string="Hex color code", store=True)
    aioa_icon_type_pro = fields.Selection(CHOICES, store=True)
    aioa_icon_size_desktop_pro = fields.Selection(CHOICES1, store=True)
    aioa_size_pro = fields.Selection([('regular', 'Regular Size'),
                                      ('oversize', 'Oversize')], store=True, default='regular')
    aioa_precise_position_pro = fields.Boolean(string="Enable Precise accessibility widget icon position", default=False)
    aioa_offset_right_pro = fields.Integer(string="Right offset (PX)", default=20, help="0 - 250px are permitted values")
    aioa_offset_right_dir_pro = fields.Selection([('to_the_left', 'To the left'),
                                                  ('to_the_right', 'To the right')],
                                                 string="To the left", default='to_the_left')
    aioa_offset_bottom_pro = fields.Integer(string="Bottom offset (PX)", default=20, help="0 - 250px are permitted values")
    aioa_offset_bottom_dir_pro = fields.Selection([('to_the_bottom', 'Top the bottom'),
                                                   ('to_the_top', 'To the top')],
                                                  string="To the bottom", default='to_the_bottom')
    aioa_custom_icon_size_pro = fields.Boolean(string="Enable Icon Custom Size", default=False)
    aioa_custom_icon_size_px_pro = fields.Integer(string="Select exact icon size (PX)",
                                                  default=50, help="20 - 150px are permitted values")
    base_url_pro = fields.Char(string="Base_url", store=True)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        param = self.env['ir.config_parameter'].sudo()

        res.update({
            'aioa_color_code_pro': param.get_param('odoo-allinoneaccessibilitypro.aioa_color_code_pro', default='#420083'),
            'aioa_icon_type_pro': param.get_param('odoo-allinoneaccessibilitypro.aioa_icon_type_pro', default='aioa-icon-type-1'),
            'aioa_icon_size_desktop_pro': param.get_param('odoo-allinoneaccessibilitypro.aioa_icon_size_desktop_pro', default='aioa-default-icon'),
            'place_pro': param.get_param('odoo-allinoneaccessibilitypro.place_pro', default='bottom_right'),
            'aioa_size_pro': param.get_param('odoo-allinoneaccessibilitypro.aioa_size_pro', default='regular'),
            'aioa_precise_position_pro': param.get_param('odoo-allinoneaccessibilitypro.aioa_precise_position_pro', default='False') == 'True',
            'aioa_offset_right_pro': int(param.get_param('odoo-allinoneaccessibilitypro.aioa_offset_right_pro', default='20')),
            'aioa_offset_right_dir_pro': param.get_param('odoo-allinoneaccessibilitypro.aioa_offset_right_dir_pro', default='to_the_left'),
            'aioa_offset_bottom_pro': int(param.get_param('odoo-allinoneaccessibilitypro.aioa_offset_bottom_pro', default='20')),
            'aioa_offset_bottom_dir_pro': param.get_param('odoo-allinoneaccessibilitypro.aioa_offset_bottom_dir_pro', default='to_the_bottom'),
            'aioa_custom_icon_size_pro': param.get_param('odoo-allinoneaccessibilitypro.aioa_custom_icon_size_pro', default='False') == 'True',
            'aioa_custom_icon_size_px_pro': int(param.get_param('odoo-allinoneaccessibilitypro.aioa_custom_icon_size_px_pro', default='50')),
            'base_url_pro': "https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode={}&token={}&t={}&position={}.{}.{}"
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        pro_set_baseURL = "https://www.skynettechnologies.com/accessibility/js/all-in-one-accessibility-js-widget-minify.js?colorcode={}&token={}&t={}&position={}.{}.{}"
        # Set values to parameters
        param.set_param('odoo-allinoneaccessibilitypro.aioa_color_code_pro', self.aioa_color_code_pro or '')
        param.set_param('odoo-allinoneaccessibilitypro.aioa_icon_type_pro', self.aioa_icon_type_pro or '')
        param.set_param('odoo-allinoneaccessibilitypro.aioa_icon_size_desktop_pro', self.aioa_icon_size_desktop_pro or '')
        param.set_param('odoo-allinoneaccessibilitypro.place_pro', self.place_pro or '')
        param.set_param('odoo-allinoneaccessibilitypro.aioa_size_pro', self.aioa_size_pro or 'regular')

        # Store booleans as string
        param.set_param('odoo-allinoneaccessibilitypro.aioa_precise_position_pro', str(bool(self.aioa_precise_position_pro)))
        param.set_param('odoo-allinoneaccessibilitypro.aioa_offset_right_pro', str(self.aioa_offset_right_pro or 20))
        param.set_param('odoo-allinoneaccessibilitypro.aioa_offset_right_dir_pro', self.aioa_offset_right_dir_pro or 'to_the_left')
        param.set_param('odoo-allinoneaccessibilitypro.aioa_offset_bottom_pro', str(self.aioa_offset_bottom_pro or 20))
        param.set_param('odoo-allinoneaccessibilitypro.aioa_offset_bottom_dir_pro', self.aioa_offset_bottom_dir_pro or 'to_the_bottom')
        param.set_param('odoo-allinoneaccessibilitypro.aioa_custom_icon_size_pro', str(bool(self.aioa_custom_icon_size_pro)))
        param.set_param('odoo-allinoneaccessibilitypro.aioa_custom_icon_size_px_pro', str(self.aioa_custom_icon_size_px_pro or 50))
        param.set_param('odoo-allinoneaccessibilitypro.base_url_pro', pro_set_baseURL)

        # Call the external API method after saving the configuration
        self._send_to_external_api()


    def _send_to_external_api(self):
        # Get the base URL
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        
        # Parse the URL
        parsed_url = urlparse(base_url)
        
        # Get hostname and scheme without the port
        hostname = parsed_url.hostname
        scheme = parsed_url.scheme
        
        # Rebuild the URL without port
        domain_only_url = f'{scheme}://{hostname}'
        
        # Build external payload
        data = {
            "u": domain_only_url,
            "widget_color_code": self.aioa_color_code_pro,
            "is_widget_custom_position": int(self.aioa_precise_position_pro),
            "is_widget_custom_size": int(self.aioa_custom_icon_size_pro),
        }

        # Position logic
        if not self.aioa_precise_position_pro:
            data.update({
                "widget_position_top": None,
                "widget_position_right": None,
                "widget_position_bottom": None,
                "widget_position_left": None,
                "widget_position": self.place_pro,  # Use aioa_place
            })
        else:
            widget_position = {
                "widget_position_top": None,
                "widget_position_right": None,
                "widget_position_bottom": None,
                "widget_position_left": None,
            }

            # Horizontal offset
            if self.aioa_offset_right_dir_pro == "to_the_left":
                widget_position["widget_position_left"] = self.aioa_offset_right_pro
            elif self.aioa_offset_right_dir_pro == "to_the_right":
                widget_position["widget_position_right"] = self.aioa_offset_right_pro

            # Vertical offset
            if self.aioa_offset_bottom_dir_pro == "to_the_bottom":
                widget_position["widget_position_bottom"] = self.aioa_offset_bottom_pro
            elif self.aioa_offset_bottom_dir_pro == "to_the_top":
                widget_position["widget_position_top"] = self.aioa_offset_bottom_pro

            data.update(widget_position)
            data["widget_position"] = ""

        # Icon size
        if not self.aioa_custom_icon_size_pro:
            data.update({
                "widget_icon_size": self.aioa_icon_size_desktop_pro,
                "widget_icon_size_custom": 0,
            })
        else:
            data.update({
                "widget_icon_size": "",
                "widget_icon_size_custom": self.aioa_custom_icon_size_px_pro,
            })

        # General widget size
        widget_size_value = 1 if self.aioa_size_pro == "oversize" else 0
        data.update({
            "widget_size": widget_size_value,
            "widget_icon_type": self.aioa_icon_type_pro,
        })
        # Send data to the external API
        try:
            response = requests.post("https://ada.skynettechnologies.us/api/widget-setting-update-platform", json=data)
            if response.status_code != 200:
                raise Exception(f"Failed to update external API {response.status_code}")
        except Exception as e:
            raise UserError(f"API Error: {str(e)}")

    @api.constrains('aioa_offset_right_pro', 'aioa_offset_bottom_pro', 'aioa_custom_icon_size_px_pro')
    def _check_pixel_ranges(self):
        for record in self:
            if record.aioa_precise_position_pro:
                if not (0 <= record.aioa_offset_right_pro <= 250):
                    raise ValidationError(_("Right offset (PX) must be between 0 and 250."))
                if not (0 <= record.aioa_offset_bottom_pro <= 250):
                    raise ValidationError(_("Bottom offset (PX) must be between 0 and 250."))
            if record.aioa_custom_icon_size_pro:
                if not (20 <= record.aioa_custom_icon_size_px_pro <= 150):
                    raise ValidationError(_("Custom icon size must be between 20 and 150 pixels."))

















   







