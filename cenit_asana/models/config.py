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

import logging

from odoo import models, fields, api


_logger = logging.getLogger(__name__)

COLLECTION_NAME = "asana"
COLLECTION_VERSION = "1.0.0"
COLLECTION_PARAMS = {
    'Personal token':'personal_token',
}

class CenitIntegrationSettings(models.TransientModel):
    _name = "cenit.asana.settings"
    _inherit = 'res.config.settings'

    ############################################################################
    # Pull Parameters
    ############################################################################
    personal_token = fields.Char('Personal token')

    ############################################################################
    # Default Getters
    ############################################################################
    def get_values_personal_token(self, context):
        personal_token = self.env['ir.config_parameter'].get_param(
            'odoo_cenit.asana.personal_token', default=None
        )
        return {'personal_token': personal_token or ''}


    ############################################################################
    # Default Setters
    ############################################################################
    def set_values(self):
        config_parameters = self.env['ir.config_parameter']
        for record in self.browse(self.ids):
            config_parameters.set_param (
                'odoo_cenit.asana.personal_token', record.personal_token or ''
            )


    ############################################################################
    # Actions
    ############################################################################
    def execute(self):
        rc = super(CenitIntegrationSettings, self).execute()

        if not self.env.context.get('install', False):
            return rc

        objs = self.browse(self.ids)
        if not objs:
            return rc
        obj = objs[0]

        installer = self.env['cenit.collection.installer']
        data = installer.get_collection_data(
            COLLECTION_NAME,
            version = COLLECTION_VERSION
        )

        params = {}
        for p in data.get('pull_parameters'):
            k = p['label']
            id_ = p.get('id')
            value = getattr(obj,COLLECTION_PARAMS.get(k))
            params.update ({id_: value})

        installer.pull_shared_collection(data.get('id'), params=params)
        installer.install_common_data(data['data'])

        return rc
