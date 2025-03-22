from odoo import models, fields, api


class PhongHop(models.Model):
    _name = 'phong_hop'
    _description = 'Bảng chứa thông tin phòng họp'


    name = fields.Char(string='Tên Phòng', required=True)
    suc_chua = fields.Integer(string='Sức Chứa', required=True)
    mo_ta = fields.Text(string='Mô Tả')
    thiet_bi_ids = fields.Many2many('thiet_bi', string='Thiết Bị')
    trang_thai = fields.Selection([
        ('hoat_dong', 'Hoạt Động'),
        ('khong_hoat_dong', 'Không Hoạt Động')
    ], string='Trạng Thái', default='hoat_dong')
    hinh_anh = fields.Binary(string='Hình Ảnh')
    
    @api.constrains('suc_chua')
    def _check_capacity(self):
        for record in self:
            if record.suc_chua <= 0:
                raise ValidationError("Sức chứa phải lớn hơn 0.")

    def action_activate_room(self):
        # Kích hoạt phòng họp
        for record in self:
            record.trang_thai = 'hoat_dong'
            return f"Phòng {record.name} đã được kích hoạt."

    def action_deactivate_room(self):
        # Ngừng hoạt động phòng họp
        for record in self:
            record.trang_thai = 'khong_hoat_dong'
            return f"Phòng {record.name} đã ngừng hoạt động."

    def action_add_device(self, device_ids):
        # Thêm thiết bị vào phòng họp
        for record in self:
            record.thiet_bi_ids |= self.env['thiet_bi'].browse(device_ids)
            return f"Thiết bị đã được thêm vào phòng {record.name}."

    def action_remove_device(self, device_ids):
        # Xóa thiết bị khỏi phòng họp
        for record in self:
            record.thiet_bi_ids -= self.env['thiet_bi'].browse(device_ids)
            return f"Thiết bị đã được xóa khỏi phòng {record.name}."
