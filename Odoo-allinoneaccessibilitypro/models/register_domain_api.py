import requests
from odoo.http import request
from urllib.parse import urlparse
from datetime import datetime
import base64

def run_accessibility_api_once(env):
    """Runs the accessibility API only once after module installation or settings access"""
    
    # Check if the API has already been called (using ir.config_parameter)
    api_called = env['ir.config_parameter'].sudo().get_param('odoo-allinoneaccessibilitypro.api_called', 'False')

    # If already called, do nothing
    if api_called == 'True':
        return
    
    error_content = None
    try:
        # -------- Fetch the website base URL from ir.config_parameter
        base_url = env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        
        # Parse the base URL to get domain
        parsed_url = urlparse(base_url)
        domain_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
        domain_name = parsed_url.hostname

       
        headers = {}
        # -------- Build the payload for the API registration
        payload = {
            "name": domain_name,
            "email": f"no-reply@{domain_name}",
            "company_name": "",
            "website": base64.b64encode(domain_url.encode()).decode(),
            "package_type": "paid-widget",
            "start_date": datetime.utcnow().isoformat(),
            "end_date": "",
            "price": "",
            "discount_price": "0",
            "platform": "Odoo",
            "api_key": "",
            "is_trial_period": "",
            "is_free_widget": "0",
            "bill_address": "",
            "country": "",
            "state": "",
            "city": "",
            "post_code": "",
            "transaction_id": "",
            "subscr_id": "",
            "payment_source": "",
            "no_required_eu": 1
        }
        
        # -------- Send the registration payload to your external service
        register_resp = requests.post(
            "https://ada.skynettechnologies.us/api/add-user-domain",
            json=payload,
            headers=headers
        )
        # -------- Save the 'called' flag in ir.config_parameter to prevent future calls
        env['ir.config_parameter'].sudo().set_param('odoo-allinoneaccessibilitypro.api_called', 'True')

    except requests.exceptions.RequestException as e:
        error_content = f"Request error: {str(e)}"

    except Exception as e:
        error_content = f"Unexpected error: {str(e)}"
        
