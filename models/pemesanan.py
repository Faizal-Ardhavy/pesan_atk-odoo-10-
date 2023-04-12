from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime, pytz

class Pemesanan(models.Model):
    _name = "training.pemesanan"

    name = fields.Char(string = "Nama Divisi", required=True,readonly = True,  states={'draft': [('readonly', False)]})
    atk_ids = fields.Many2one('training.atk', string="Nama ATK", states={'draft': [('readonly', False)]})
    total = fields.Integer(string= "Harga Total", compute = "set_harga_total", readonly = True, states={'draft': [('readonly', True)]})
    campuran = fields.One2many('campuran','pemesanan_ids', string="Alat Tulis Kantor",readonly = True, states={'draft': [('readonly', False)]})
    harga = fields.Integer(related = "atk_ids.harga", string="Harga Produk" ,required=True, states={'draft': [('readonly', False)]})
    jumlah  = fields.Integer(string="Jumlah Pemesanan Produk", required=True, compute = "get_jumlah", states={'draft': [('readonly', False)]})
    jenis =  fields.Integer(string="Total Jenis Produk", required=True, compute = "get_jenis", states={'draft': [('readonly', False)]})
    date_action = fields.Datetime(
            'Date current action',
            required=False,
            readonly=False,
            select=True,
            default=lambda self: fields.datetime.now(pytz.timezone('Asia/Jakarta'))
        )
    justification = fields.Text(string="Justifikasi Penolakan")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'RFA'),
        ('done', 'Approved'),
        ('reject', 'Rejected'),
    ], string='Status', readonly=True, copy=False, default='draft', track_visibility='onchange')

     
    @api.multi
    def action_confirm(self):
        self.write({'state': 'open'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'draft'})
        self.write({"justification" : ""})

    @api.multi
    def action_close(self):
        self.write({'state': 'done'})
        self.write({"justification" : ""})


    @api.multi
    def action_reject(self):
        self.write({'state': 'reject'})


    @api.depends("harga")
    def set_harga_total(self):
        for r in self:
            tmp = 0
            for a in r.campuran:
                tmp += a.jumlah * a.atk_ids.harga
            r.total = tmp

    @api.depends("jumlah")
    def get_jumlah(self):
        for r in self:
            tmp = 0
            for a in r.campuran:
                tmp = tmp + a.jumlah
            r.jumlah = tmp

    @api.depends("jenis")
    def get_jenis(self):
        for r in self:
            tmp = 0
            jenis = 0
            for a in r.campuran:
                tmp = tmp + a.jumlah
                jenis = jenis+1
            r.jenis = jenis

    @api.multi
    def cetak_sesi(self):
        return self.env['report'].get_action(self, 'pesan_atk.laporan_pemesanan')
    
    @api.constrains("name")
    def _check_atk(self):
        for r in self:
            if not r.name or r.name.strip()=="":
                raise ValidationError("Nama divisi tidak valid")
            
    @api.constrains('campuran')
    def _check_pemesanan(self):
        for r in self:
            if not r.campuran:
                raise ValidationError('Belum ada barang yang dipesan')
 
    @api.multi
    def submit_reject(self):
        reference = self.env.ref('pesan_atk.reject_wizard_form_view').id
        return {
            'name': 'Reject Pemesanan',
            'type': 'ir.actions.act_window',
            'res_model': 'training.pemesanan',
            'view_type': 'form',
            'view_mode': 'form',
            'views'    : [(reference,'form')],
            'target': 'new',
            'res_id': self.id
        }
        
