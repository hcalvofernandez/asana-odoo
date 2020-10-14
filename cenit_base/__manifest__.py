# -*- coding: utf-8 -*-
################################################################################
# Author      : Hanoi Calvo Fernandez
# Copyright(c): 2020-Present HanoiCalvo Fernandez hanoi.calvo@uic.cu
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    "name": "Cenit IO Integrations Client",
    "category": "Hidden",
    "version": "0.13.1",
    "application": True,
    "author": "NeoHan-solutions",
    "website": "https://asana.odooexperts.com.mx",
    # ~ "license": "LGPL-3",
    "category": "Extra Tools",
    "summary": "Odoo, Cenit, Integration, Connector",
    "description": """
        Integrate with third party systems through the Cenit platform
    """,
    "depends": ["base", "base_automation"],
    "external_dependencies": {
        "python": ["inflect", "pyasn1", "OpenSSL", "ndg"]
    },
    "data": [
        "security/ir.model.access.csv",
        "view/config.xml",
        "view/data_definitions.xml",
        "view/setup.xml",
    ],
    "images": [
        "static/screenshots/main.png"
    ],
    "installable": True
}
