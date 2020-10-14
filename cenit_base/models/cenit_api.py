# -*- coding: utf-8 -*-
## -*- coding: utf-8 -*-
################################################################################
# Author      : Hanoi Calvo Fernandez
# Copyright(c): 2020-Present HanoiCalvo Fernandez hanoi.calvo@uic.cu
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

import requests
import json
import logging

from odoo import models, api, exceptions


_logger = logging.getLogger(__name__)

API_PATH = "/api/v2"


class CenitApi(models.AbstractModel):
    """
       Model to connect to Cenit's API
    """
    _name = "cenit.api"
    _description = "Cenit Api"

    def _get_values(self):
        vals = self.read([])[0]
        vals.pop('create_uid')
        vals.pop('create_date')
        vals.pop('__last_update')
        vals.pop('write_uid')
        vals.pop('write_date')
        vals.pop('display_name')
        vals.pop('id')

        return vals

    def _calculate_update(self, values):
        update = {}
        for k, v in values.items():
            _logger.info("\n\n[K] %s :: [V] %s\n", k, v)
            if k == "%s" % (self.cenit_models,):
                update = {
                    'cenitID': v[0]['id']
                }

        return update

    def push_to_cenit(self):
        path = "/setup/push"
        vals = self._get_values()
        if isinstance(vals, list):
            vals = vals[0]
        values = {
            self.cenit_model: vals
        }
        if 'namespace' in values[self.cenit_model] and isinstance(values[self.cenit_model]['namespace'], int):
            values[self.cenit_model]['namespace'] = self.namespace.name
        rc = False
        try:
            rc = self.post(path, values)
            _logger.info("\n\nRC:: %s\n", rc)

            if rc.get('success', False):
                update = self._calculate_update(rc['success'])
                if isinstance(update, list):
                    update = update[0]
                # rc = self.with_context(local=True).write(update)
                for key, value in update.items():
                    self.with_context(local=True)[key] = value
                rc = True
            else:
                _logger.error(rc.get('errors'))
                return False
        except Warning as e:
            _logger.exception(e)

        return rc

    def drop_from_cenit(self):
        path = "/setup/%s/%s" % (self.cenit_model, self.cenitID)

        rc = self.delete(path)
        return rc

    @api.model
    def post(self, path, vals):
        config = self.instance()

        payload = json.dumps(vals)
        url = config.get('cenit_url') + API_PATH + path
        headers = self.headers(config)

        try:
            _logger.info("[POST] %s ? %s {%s}", url, payload, headers)
            r = requests.post(url, data=payload, headers=headers)
        except Exception as e:
            _logger.error(e)
            raise exceptions.AccessError("Error trying to connect to Cenit.")
        if 200 <= r.status_code < 300:
            return r.json()

        try:
            error = r.json()
            _logger.error(error)
        except Exception as e:
            _logger.error(e)
            raise exceptions.ValidationError("Cenit returned with errors")

        if 400 <= error.get('code', 400) < 500:
            raise exceptions.AccessError("Error trying to connect to Cenit.")

        raise exceptions.ValidationError("Cenit returned with errors")

    @api.model
    def get(self, path, params=None):
        config = self.instance()

        url = config.get('cenit_url') + API_PATH + path
        headers = self.headers(config)
        try:
            _logger.info("[GET] %s ? %s {%s}", url, params, headers)
            r = requests.get(url, params=params, headers=self.headers(config))
        except Exception as e:
            _logger.error(e)
            raise exceptions.AccessError("Error trying to connect to Cenit.")

        if 200 <= r.status_code < 300:
            return r.json()

        try:
            error = r.json()
            _logger.error(error)
        except Exception as e:
            _logger.error(e)
            _logger.info("\n\n%s\n", r.content)
            raise exceptions.ValidationError("Cenit returned with errors")

        if 400 <= error.get('code', 400) < 500:
            raise exceptions.AccessError("Error trying to connect to Cenit.")

        raise exceptions.ValidationError("Cenit returned with errors")

    @api.model
    def put(self, path, vals):
        config = self.instance()

        payload = json.dumps(vals)
        url = config.get('cenit_url') + API_PATH + path
        headers = self.headers(config)

        try:
            _logger.info("[PUT] %s ? %s {%s}", url, payload, headers)
            r = requests.put(url, data=payload, headers=headers)
        except Exception as e:
            _logger.error(e)
            raise exceptions.AccessError("Error trying to connect to Cenit.")

        if 200 <= r.status_code < 300:
            return r.json()

        try:
            error = r.json()
            _logger.error(error)
        except Exception as e:
            _logger.error(e)
            raise exceptions.ValidationError("Cenit returned with errors")

        if 400 <= error.get('code', 400) < 500:
            raise exceptions.AccessError("Error trying to connect to Cenit.")

        raise exceptions.ValidationError("Cenit returned with errors")

    @api.model
    def delete(self, path):
        config = self.instance()

        url = config.get('cenit_url') + API_PATH + path
        headers = self.headers(config)

        try:
            _logger.info("[DEL] %s ? {%s}", url, headers)
            r = requests.delete(url, headers=headers)
        except Exception as e:
            _logger.error(e)
            raise exceptions.AccessError("Error trying to connect to Cenit.")

        if 200 <= r.status_code < 300:
            return True

        try:
            error = r.json()
            _logger.error(error)
        except Exception as e:
            _logger.error(e)
            raise exceptions.ValidationError("Cenit returned with errors")

        if 400 <= error.get('code', 400) < 500:
            raise exceptions.AccessError("Error trying to connect to Cenit.")

        raise exceptions.ValidationError("Cenit returned with errors")

    @api.model
    def instance(self):
        icp = self.env['ir.config_parameter']

        config = {
            'cenit_url': icp.get_param(
                "odoo_cenit.cenit_url", default='https://cenit.io'
            ),
            'cenit_user_key': icp.get_param(
                "odoo_cenit.cenit_user_key", default=None
            ),
            'cenit_user_token': icp.get_param(
                "odoo_cenit.cenit_user_token", default=None
            ),
        }

        return config

    @api.model
    def headers(self, config):
        return {
            'Content-Type': 'application/json',
            'X-User-Access-Key': config.get('cenit_user_key'),
            'X-User-Access-Token': config.get('cenit_user_token')
        }

    @api.model
    def create(self, vals):
        obj = super(CenitApi, self).create(vals)

        local = self.env.context.get('local', False)
        if local:
            return obj

        rc = False
        try:
            rc = obj.push_to_cenit()
        except requests.ConnectionError as e:
            _logger.exception(e)
            raise exceptions.AccessError("Error trying to connect to Cenit.")
        except exceptions.AccessError:
            raise exceptions.AccessError("Error trying to access to Cenit.")
        except Exception as e:
            _logger.exception(e)
            raise exceptions.ValidationError("Cenit returned with errors")

        if not rc:
            raise exceptions.ValidationError("Cenit returned with errors")

        return obj

    def write(self, vals):
        res = super(CenitApi, self).write(vals)

        local = self.env.context.get('local', False)
        if local:
            return res

        cp = vals.copy()
        if cp.pop('cenitID', False):
            if len(cp.keys()) == 0:
                return res

        try:
            self.push_to_cenit()
        except requests.ConnectionError as e:
            _logger.exception(e)
            raise exceptions.AccessError("Error trying to connect to Cenit.")
        except exceptions.AccessError:
            raise exceptions.AccessError("Error trying to connect to Cenit.")
        except Exception as e:
            _logger.exception(e)
            raise exceptions.ValidationError("Cenit returned with errors")

        return res

    def unlink(self, **kwargs):
        rc = True
        for record in self:
            try:
                rc = record.drop_from_cenit()
            except requests.ConnectionError as e:
                _logger.exception(e)
                raise exceptions.AccessError("Error trying to connect to Cenit.")
            except exceptions.AccessError:
                raise exceptions.AccessError("Error trying to connect to Cenit.")
            except Exception as e:
                _logger.exception(e)
                raise exceptions.ValidationError("Cenit returned with errors")

            if not rc:
                raise exceptions.ValidationError("Cenit returned with errors")

        rc = super(CenitApi, self).unlink(**kwargs)
        return rc