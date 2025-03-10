# Copyright 2023 Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import re
import uuid

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ServerAction(models.Model):
    _inherit = "ir.actions.server"

    formio_ref = fields.Char(
        string="Forms Ref",
        help="Identifies a server action with related form builder.",
    )

    @api.onchange('model_id')
    def _onchange_formio_ref(self):
        form_model = self.env.ref('formio.model_formio_form')
        if self.model_id.id == form_model.id and not self.formio_ref:
            self.formio_ref = str(uuid.uuid4())
        elif self.model_id.id != form_model.id:
            self.formio_ref = False

    @api.constrains('formio_ref')
    def constaint_check_formio_ref(self):
        self.ensure_one
        if self.formio_ref:
            if re.search(r"[^a-zA-Z0-9_-]", self.formio_ref) is not None:
                raise ValidationError(_('Forms Ref is invalid. Use ASCII letters, digits, "-" or "_".'))

    @api.constrains('formio_ref')
    def _constraint_unique_formio_ref(self):
        for rec in self:
            domain = [("formio_ref", "=", rec.formio_ref)]
            if self.formio_ref and self.search_count(domain) > 1:
                msg = _(
                    'A Server Action with Forms Ref "%s" already exists.\nForms Ref should be unique.'
                ) % (rec.formio_ref)
                raise ValidationError(msg)
