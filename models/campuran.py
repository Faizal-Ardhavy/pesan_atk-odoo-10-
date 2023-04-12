from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Campuran(models.Model):
    _name = "campuran"

    atk_ids = fields.Many2one('training.atk', string="Nama ATK")
    jumlah  = fields.Integer(string="Jumlah Pemesanan Produk", required=True, readonly = False)
    limit = fields.Integer(related = "atk_ids.limit", string="Batas Pemesanan Produk", readonly = True)
    total = fields.Integer(related = "pemesanan_ids.total", string= "Harga Total",  readonly = True)

    pemesanan_ids = fields.Many2one('training.pemesanan', string="test")


    @api.constrains("atk_ids", "pemesanan_ids")
    def _check_atk(self):
        for r in self:
            count = self.env['campuran'].search_count([
                ('id', '!=', r.id),
                ('atk_ids', '=', r.atk_ids.id),
                ('pemesanan_ids', '=', r.pemesanan_ids.id)
            ])
            if count > 0:
                raise ValidationError("Terdapat barang yang dipesan lebih dari 1 kali")

    
    @api.constrains("jumlah")
    def _cek_jumlah(self):
        for r in self:
            if r.jumlah > r.limit:
                raise ValidationError("Terdapat barang yang melebihi batas")

            elif r.jumlah <= 0:
                raise ValidationError("Terdapat jumlah barang yang tidak valid")
            
    @api.constrains("atk_ids")
    def _cek_atk(self):
        for r in self:
            if not r.atk_ids:
                raise ValidationError("Terdapat pesanan yang tidak valid")

