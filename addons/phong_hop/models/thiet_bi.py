from odoo import models, fields, api


class ThietBi(models.Model):
    _name = 'thiet_bi'
    _description = 'Thiết Bị'

    ma_thiet_bi = fields.Char(string='Mã Thiết Bị', required=True)
    ten_thiet_bi = fields.Char(string='Tên Thiết Bị', required=True)
    trang_thai = fields.Selection([
        ('hoat_dong', 'Hoạt Động'),
        ('khong_hoat_dong', 'Không Hoạt Động'),
        ('bao_tri', 'Bảo Trì')
    ], string='Trạng Thái', default='hoat_dong')
    phong_id = fields.Many2one('phong_hop', string='Phòng Họp')

    @api.constrains('ma_thiet_bi')
    def _check_unique_code(self):
        for record in self:
            if self.search_count([('ma_thiet_bi', '=', record.ma_thiet_bi)]) > 1:
                raise ValidationError("Mã thiết bị phải là duy nhất.")

    def action_activate_device(self):
        # Kích hoạt thiết bị
        for record in self:
            record.trang_thai = 'hoat_dong'
            return f"Thiết bị {record.ten_thiet_bi} đã được kích hoạt."

    def action_deactivate_device(self):
        # Ngừng hoạt động thiết bị
        for record in self:
            record.trang_thai = 'khong_hoat_dong'
            return f"Thiết bị {record.ten_thiet_bi} đã ngừng hoạt động."

    def action_send_for_maintenance(self):
        # Gửi thiết bị đi bảo trì
        for record in self:
            record.trang_thai = 'bao_tri'
            return f"Thiết bị {record.ten_thiet_bi} đã được gửi đi bảo trì."

    def action_update_device(self, ma_thiet_bi, ten_thiet_bi):
        # Cập nhật thông tin thiết bị
        for record in self:
            record.update({
                'ma_thiet_bi': ma_thiet_bi,
                'ten_thiet_bi': ten_thiet_bi
            })
            return f"Thông tin thiết bị {record.ten_thiet_bi} đã được cập nhật."
