from odoo import models, fields, api


class QuanLyPhongHop(models.Model):
    _name = 'quan_ly_phong_hop'
    _description = 'Bảng chứa thông tin phòng họp'
    

    ten_phong = fields.Char(string="Tên Phòng", required=True)
    suc_chua = fields.Integer(string="Sức Chứa")
    trang_thiet_bi = fields.Text(string="Trang Thiết Bị")
    dia_chi = fields.Char(string="Địa Chỉ")
    
