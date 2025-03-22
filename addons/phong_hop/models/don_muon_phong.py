from odoo import models, fields, api


class DonMuonPhong(models.Model):
    _name = 'don_muon_phong'
    _description = 'Đơn mượn phòng'

    phong_id = fields.Many2one('phong_hop', string='Phòng Họp', required=True)
    tieu_de = fields.Char(string='Tiêu Đề', required=True)
    nguoi_dat_phong = fields.Char(string='Người Đặt Phòng', required=True)
    thoi_gian_bat_dau = fields.Datetime(string='Thời Gian Bắt Đầu', required=True)
    thoi_gian_ket_thuc = fields.Datetime(string='Thời Gian Kết Thúc', required=True)
    muc_dich = fields.Text(string='Mục Đích')
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ Duyệt'),
        ('duyet', 'Đã Duyệt'),
        ('huy', 'Đã Hủy')
    ], string='Trạng Thái', default='cho_duyet')
    
    loai_phong = fields.Selection([
        ('phong_hop', 'Phòng Họp'),
        ('phong_hoi_nghi', 'Phòng Hội Nghị')
    ], string='Loại Phòng', required=True)  
     
    ghi_chu = fields.Text(string='Ghi Chú')
    
    @api.constrains('thoi_gian_ket_thuc', 'thoi_gian_bat_dau')
    def _check_time(self):
        for record in self:
            if record.thoi_gian_ket_thuc <= record.thoi_gian_bat_dau:
                raise ValidationError("Thời gian kết thúc phải lớn hơn thời gian bắt đầu.")

    def action_confirm_booking(self):
        # Xác nhận đơn mượn phòng
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.trang_thai = 'duyet'
                return f"Đơn mượn phòng {record.phong_id.name} đã được xác nhận."
            return "Đơn mượn này đã được xác nhận hoặc hủy."

    def action_cancel_booking(self):
        # Hủy đơn mượn phòng
        for record in self:
            if record.trang_thai == 'cho_duyet':
                record.trang_thai = 'huy'
                return f"Đơn mượn phòng {record.phong_id.name} đã bị hủy."
            return "Không thể hủy đơn mượn này."

    def action_get_booking_summary(self):
        # Tạo báo cáo tóm tắt đơn mượn
        summary = []
        for record in self:
            summary.append({
                'phong_hop': record.phong_id.name,
                'tieu_de': record.tieu_de,
                'thoi_gian_bat_dau': record.thoi_gian_bat_dau,
                'thoi_gian_ket_thuc': record.thoi_gian_ket_thuc,
                'trang_thai': record.trang_thai,
                'muc_dich': record.muc_dich,
            })
        return summary