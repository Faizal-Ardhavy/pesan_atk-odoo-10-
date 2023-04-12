from odoo.exceptions import ValidationError
from odoo import models, fields, api
import time
import xlsxwriter
import base64
import tempfile
import os
from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta
from xlsxwriter.utility import xl_rowcol_to_cell
import logging
import re
import pytz
from lxml import etree
import calendar
import StringIO
from StringIO import StringIO



class Wizard(models.TransientModel):
    _name = 'report.wizard'

    name = fields.Char("File Name")
    file = fields.Binary("File", readonly=True)

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    wbf={}
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'RFA'),
        ('done', 'Approved'),
        ('reject', 'Rejected'),
    ], string='Status', copy=False, track_visibility='onchange')


    @api.multi
    def add_workbook_format(self, workbook):
        self.wbf['company'] = workbook.add_format({'bold':1,'align': 'left','font_color':'#000000','num_format': 'dd-mm-yyyy'})
        self.wbf['company'].set_font_size(12)

        self.wbf['footer'] = workbook.add_format({'align':'left'})

        self.wbf['header'] = workbook.add_format({'bg_color':'#FFFF00','bold': 1,'align': 'center','font_color': '#000000'})
        self.wbf['header'].set_top(2)
        self.wbf['header'].set_bottom()
        self.wbf['header'].set_left()
        self.wbf['header'].set_right()
        self.wbf['header'].set_font_size(11)
        self.wbf['header'].set_align('vcenter')

        self.wbf['header_left'] = workbook.add_format({'bg_color':'#FFFF00','bold': 1,'align': 'center','font_color': '#000000'})
        self.wbf['header_left'].set_top(2)
        self.wbf['header_left'].set_bottom()
        self.wbf['header_left'].set_left(2)
        self.wbf['header_left'].set_right()
        self.wbf['header_left'].set_font_size(11)
        self.wbf['header_left'].set_align('vcenter')
        
        self.wbf['header_right'] = workbook.add_format({'bg_color':'#FFFF00','bold': 1,'align': 'center','font_color': '#000000'})
        self.wbf['header_right'].set_top(2)
        self.wbf['header_right'].set_bottom()
        self.wbf['header_right'].set_left()
        self.wbf['header_right'].set_right(2)
        self.wbf['header_right'].set_font_size(11)
        self.wbf['header_right'].set_align('vcenter')


        self.wbf['content'] = workbook.add_format({'align': 'left','font_color': '#000000'})
        self.wbf['content'].set_left()
        self.wbf['content'].set_right()
        self.wbf['content'].set_top()
        self.wbf['content'].set_bottom()
        self.wbf['content'].set_font_size(10)                

        self.wbf['content_bg'] = workbook.add_format({'bg_color': '#81DAF5','align': 'center','font_color': '#000000'})
        self.wbf['content_bg'].set_left()
        self.wbf['content_bg'].set_right()
        self.wbf['content_bg'].set_top()
        self.wbf['content_bg'].set_bottom()
        self.wbf['content_bg'].set_font_size(10)                
      
        self.wbf['content_center'] = workbook.add_format({'align': 'center','font_color': '#000000'})
        self.wbf['content_center'].set_left()
        self.wbf['content_center'].set_right()
        self.wbf['content_center'].set_top()
        self.wbf['content_center'].set_bottom()
        self.wbf['content_center'].set_font_size(10)
        
        self.wbf['content_left'] = workbook.add_format({'align': 'center','font_color': '#000000'})
        self.wbf['content_left'].set_left(2)
        self.wbf['content_left'].set_right()
        self.wbf['content_left'].set_top()
        self.wbf['content_left'].set_bottom()
        self.wbf['content_left'].set_font_size(10)
        
        self.wbf['content_right'] = workbook.add_format({'align': 'center','font_color': '#000000'})
        self.wbf['content_right'].set_left()
        self.wbf['content_right'].set_right(2)
        self.wbf['content_right'].set_top()
        self.wbf['content_right'].set_bottom()
        self.wbf['content_right'].set_font_size(10)

        self.wbf['content_bottom'] = workbook.add_format({'align': 'center','font_color': '#000000'})
        self.wbf['content_bottom'].set_left()
        self.wbf['content_bottom'].set_right()
        self.wbf['content_bottom'].set_top()
        self.wbf['content_bottom'].set_bottom(2)
        self.wbf['content_bottom'].set_font_size(10)

        self.wbf['content_left_bottom'] = workbook.add_format({'align': 'center','font_color': '#000000'})
        self.wbf['content_left_bottom'].set_left(2)
        self.wbf['content_left_bottom'].set_right()
        self.wbf['content_left_bottom'].set_top()
        self.wbf['content_left_bottom'].set_bottom(2)
        self.wbf['content_left_bottom'].set_font_size(10)
        
        self.wbf['content_right_bottom'] = workbook.add_format({'align': 'center','font_color': '#000000'})
        self.wbf['content_right_bottom'].set_left()
        self.wbf['content_right_bottom'].set_right(2)
        self.wbf['content_right_bottom'].set_top()
        self.wbf['content_right_bottom'].set_bottom(2)
        self.wbf['content_right_bottom'].set_font_size(10)

        self.wbf['content_center_bg'] = workbook.add_format({'bg_color':'#85C1E9', 'align': 'center','font_color': '#000000'})
        self.wbf['content_center_bg'].set_left()
        self.wbf['content_center_bg'].set_right()
        self.wbf['content_center_bg'].set_top()
        self.wbf['content_center_bg'].set_bottom()
        self.wbf['content_center_bg'].set_font_size(10)                
        
        self.wbf['content_center_bg_bottom'] = workbook.add_format({'bg_color':'#85C1E9', 'align': 'center','font_color': '#000000'})
        self.wbf['content_center_bg_bottom'].set_left()
        self.wbf['content_center_bg_bottom'].set_right()
        self.wbf['content_center_bg_bottom'].set_top()
        self.wbf['content_center_bg_bottom'].set_bottom(2)
        self.wbf['content_center_bg_bottom'].set_font_size(10)                
        
        return workbook   

    def generate_report(self):
        Sales = self.env['training.pemesanan']
        sales = Sales.search([
            ('date_action', '>=', self.start_date),
            ('date_action', '<=', self.end_date),
            ('state', '=', self.state),
        ])
        fp = StringIO()
        workbook = xlsxwriter.Workbook(fp)
        workbook = self.add_workbook_format(workbook)
        wbf = self.wbf
        worksheet = workbook.add_worksheet('Rekapan Laporan')
        worksheet.set_column('B1:B1', 4)
        worksheet.set_column('C1:C1', 20)
        worksheet.set_column('D1:D1', 20)
        worksheet.set_column('E1:E1', 20)
        worksheet.set_column('F1:F1', 20)
        query = """
            SELECT t.name, t.harga, SUM(j.jumlah), t.harga*SUM(j.jumlah) AS total 
            FROM campuran j, training_atk t 
            WHERE j.atk_ids= t.id 
            AND pemesanan_ids IN (
                SELECT id 
                FROM training_pemesanan 
                WHERE state = '%s' and date_action >= '%s' and date_action <= '%s'
            ) 
            GROUP BY t.name, t.harga;
        """%(str(self.state), str(self.start_date), str(self.end_date))

        self.env.cr.execute(query)
        ress = self.env.cr.fetchall()
        if ress==[] or not ress:
            raise ValidationError('Tidak ada laporan yang sesuai')
        else:
            worksheet.merge_range('B1:F1', 'Rekapitulasi Pemesanan ATK' , wbf['company'])
            worksheet.merge_range('B2:F2', 'Tanggal : %s s/d %s' % (str(self.start_date), str(self.end_date)) , wbf['company'])
            worksheet.merge_range('B3:F3', 'Status : %s' % (str(self.state)) , wbf['company'])

            row= 3
            worksheet.write('B%s' % (row+1), 'No', wbf['header_left'])
            worksheet.write('C%s' % (row+1), 'Nama Produk', wbf['header'])
            worksheet.write('D%s' % (row+1), 'Harga Satuan', wbf['header'])
            worksheet.write('E%s' % (row+1), 'Jumlah Barang', wbf['header'])
            worksheet.write('F%s' % (row+1), 'Harga Total', wbf['header_right'])
            row+=2

            if ress == []:
                worksheet.merge_range('A%s:X%s' % (row,row), 'Data tidak ada !' , wbf['content'])
            no=1
            for res in ress:
                worksheet.write('B%s' % (row), no, wbf['content_left'])
                worksheet.write('C%s' % (row), res[0], wbf['content'])
                worksheet.write('D%s' % (row), res[1], wbf['content'])
                worksheet.write('E%s' % (row), res[2], wbf['content'])
                worksheet.write('F%s' % (row), res[3], wbf['content_right'])
                row+=1
                no+=1
            worksheet.merge_range('B%s:E%s' % (row,row), 'Total' , wbf['content_center_bg_bottom'])
            worksheet.write('F%s' % (row), '=SUM(F5:F%s)' % (row-1), wbf['content_center_bg_bottom'])
            workbook.close()
            out = base64.encodestring(fp.getvalue())
            self.write({'file':out, 'name':'Rekapan Laporan.xlsx'})
            fp.close()
            action = {
                    'type': 'ir.actions.act_url',
                    'url': '/web/content/report.wizard/%s/file/%s?download=true' % (self.id, self.name),
                    'target': 'self',
                    'res_id': self.id,
                    }
            return action        