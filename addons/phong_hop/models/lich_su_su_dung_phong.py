from odoo import models, fields, api


class LichSuSuDungPhong(models.Model):
    _name = 'lich_su_su_dung_phong'
    _description = 'Lịch Sử Sử Dụng Phòng'

    cuoc_hop_id = fields.Many2one('don_muon_phong', string='Cuộc Họp', required=True)
    chu_de = fields.Char(string='Chủ Đề', required=True)
    gio_bat_dau = fields.Datetime(string='Giờ Bắt Đầu', required=True)
    gio_ket_thuc = fields.Datetime(string='Giờ Kết Thúc', required=True)
    ghi_chu = fields.Text(string='Ghi Chú')

    @api.constrains('gio_ket_thuc', 'gio_bat_dau')
    def _check_time(self):
        for record in self:
            if record.gio_ket_thuc <= record.gio_bat_dau:
                raise ValidationError("Giờ kết thúc phải lớn hơn giờ bắt đầu.")

    def action_add_meeting_history(self):
        # Thêm lịch sử sử dụng phòng
        for record in self:
            self.create({
                'cuoc_hop_id': record.cuoc_hop_id.id,
                'chu_de': record.chu_de,
                'gio_bat_dau': record.gio_bat_dau,
                'gio_ket_thuc': record.gio_ket_thuc,
                'ghi_chu': record.ghi_chu,
            })
            return "Lịch sử sử dụng phòng đã được thêm."

    def action_update_meeting_history(self, meeting_id):
        # Cập nhật lịch sử sử dụng phòng
        meeting = self.browse(meeting_id)
        if meeting:
            meeting.write({
                'chu_de': self.chu_de,
                'gio_bat_dau': self.gio_bat_dau,
                'gio_ket_thuc': self.gio_ket_thuc,
                'ghi_chu': self.ghi_chu,
            })
            return "Lịch sử sử dụng phòng đã được cập nhật."
        return "Cuộc họp không tồn tại."

    def action_delete_meeting_history(self, meeting_id):
        # Xóa lịch sử sử dụng phòng
        meeting = self.browse(meeting_id)
        if meeting:
            meeting.unlink()
            return "Lịch sử sử dụng phòng đã được xóa."
        return "Cuộc họp không tồn tại."