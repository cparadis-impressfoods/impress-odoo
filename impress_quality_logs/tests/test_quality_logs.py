from odoo.tests import common
from odoo.exceptions import UserError, ValidationError


class TestQualityLogs(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.LogLine = cls.env["log_line.mixin"]
        cls.QualityCheck = cls.env["quality.check"]
        cls.Production = cls.env["mrp.production"]
        cls.Product = cls.env["product.product"]
        cls.Lot = cls.env["stock.lot"]

    """
    def test_create_log_line(self):
        quality_check = self.QualityCheck.create({'name': 'Test Quality Check'})
        log_line = self.LogLine.create({'quality_check_id': quality_check.id})
        self.assertEqual(log_line.quality_check_id, quality_check)

    def test_lock_log_line(self):
        log_line = self.LogLine.create({})
        log_line.action_lock()
        self.assertTrue(log_line.is_locked)
        with self.assertRaises(ValidationError):
            log_line.write({'notes': 'Trying to write on a locked log line'})

    def test_unlock_log_line(self):
        log_line = self.LogLine.create({})
        log_line.action_lock()
        log_line.action_unlock()
        self.assertFalse(log_line.is_locked)
        log_line.write({'notes': 'Successfully wrote on an unlocked log line'})
        self.assertEqual(log_line.notes, 'Successfully wrote on an unlocked log line')

    def test_sign_log_line(self):
        log_line = self.LogLine.create({})
        log_line.sign_log_line()
        self.assertEqual(log_line.signature, self.env.user.sign_initials)
"""
