# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


# class pesan_atk(models.Model):
#     _name = 'pesan_atk.pesan_atk'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Atk(models.Model):
    _name = 'training.atk'
    _rec_name = "name"
 
    name = fields.Char(string="Alat Tulis Kantor", required=True)
    limit  = fields.Integer(string="Batas Pemesanan Produk", required = True)
    harga = fields.Integer(string="Harga Produk", required = True)

    @api.constrains("name" ,"limit", "harga")
    def _check(self):
        for r in self:
            if  not r.name or r.name.strip()=="":
                raise ValidationError("Nama barang tidak valid")
            elif r.limit<=0:
                raise ValidationError("Batas pemesanan barang tidak valid")
            elif r.harga<=0:
                raise ValidationError("Harga barang tidak valid")
            
    @api.constrains("name")
    def _check_atk(self):
        for r in self:
            count = self.env['training.atk'].search_count([
                ('id', '!=', r.id),
                ('name', 'ilike', r.name),
            ])
            if count > 0:
                raise ValidationError("Terdapat barang yang dibuat lebih dari 1 kali")