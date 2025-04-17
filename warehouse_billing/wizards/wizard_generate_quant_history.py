import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class WizardGenerate_quant_history(models.TransientModel):
    _name = "wizard.generate_quant_history"
    _description = _("WizardGenerate_quant_history")

    name = fields.Char()

    @api.model
    def generate_quant_history(self):
        product_ids = self.env["product.product"].search(
            [("detailed_type", "=", "product")]
        )

        quants = self.env["stock.quant"].search(
            [
                ("product_id", "in", product_ids.ids),
                ("quantity", ">", 0),
                ("location_id.usage", "=", "internal"),
            ]
        )
        quant_history = self.env["warehouse.quant.history"].create_from_quant(quants)
        _logger.info("Generated quant history for %s quants", len(quant_history))
