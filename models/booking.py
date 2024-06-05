import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError
class Booking (models.Model):
    _name = "booking.freight"
    _description = "Booking details "

    origin = fields.Selection([("MAA", "Chennai"), ("BOM", "Mumbai"), ("DEL", "Delhi"), ("HYD", "Hyderabad"), ("BLR", "Bangalore"), ("CCU", "Kolkata"), ("COK", "Kochi"), ("GOI", "Goa"), ("ATQ", "Amritsar"), ("IXM", "Madurai")],string='origin', required=True)
    destination = fields.Selection([("MAA", "Chennai"), ("BOM", "Mumbai"), ("DEL", "Delhi"), ("HYD", "Hyderabad"), ("BLR", "Bangalore"), ("CCU", "Kolkata"), ("COK", "Kochi"), ("GOI", "Goa"), ("ATQ", "Amritsar"), ("IXM", "Madurai")],string='destination', required=True)
    date = fields.Date(string='flight_date', required=True)
    gross_weight = fields.Integer(string='gross_weight', required=True)
    volume_weight = fields.Integer(string='volume_weight', required=True)
    chargable_weight = fields.Integer(string='chargable_weight', required=False, compute='_compute_chargable_weight', store=True)
    item_count = fields.Integer(string='item_count', required=True)
    fare = fields.Integer(string='fare', required=False, compute='_compute_fare', store=True)
    consingee = fields.Selection([('flipkart', 'Flipkart'), ('amazon', 'Amazon'), ('ford', 'Ford'), ('tvs', 'TVS')], string='consingee', required=False)
    shipper = fields.Selection([('shipglobal', 'Ship Global'), ('form2global', 'Form 2 Global')], string='shipper', required=False)
    perm_read = fields.Boolean(string='Apply for Read', default=True)
    perm_write = fields.Boolean(string='Apply for Write', default=True)
    perm_create = fields.Boolean(string='Apply for Create', default=True)
    perm_unlink = fields.Boolean(string='Apply for Delete', default=True)

    @api.constrains('origin', 'destination')
    def _check_unique_location(self):
        for rec in self:
            if rec.origin == rec.destination:
                raise ValidationError("Orgin and Destination should not be same!")

    @api.depends('chargable_weight','item_count')
    def _compute_fare(self):
        for rec in self:
            if rec.chargable_weight != 0 and rec.item_count != 0:
                rec.fare = rec.chargable_weight * rec.item_count
                logging.info("test ==> ssdnskndksndsjdnsndmnsadnksndsndjsn")
                logging.info(rec.fare)
            else:
                rec.fare = 0

    @api.depends('gross_weight','volume_weight')
    def _compute_chargable_weight(self):
        for rec in self:
            if rec.gross_weight != 0 and rec.volume_weight != 0:
                if rec.gross_weight > rec.volume_weight:
                    rec.chargable_weight = rec.gross_weight
                else:
                    rec.chargable_weight = rec.volume_weight
            else:
                rec.chargable_weight = 0
