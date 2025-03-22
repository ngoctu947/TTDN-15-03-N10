from odoo import models, fields, api


class ThongKePhongHop(models.Model):
    _name = 'thong_ke_phong_hop'
    _description = 'Thống Kê Phòng Họp'

    phong_hop_id = fields.Many2one('phong_hop', string='Phòng Họp', required=True)
    so_nguoi_tham_du = fields.Integer(string='Số Người Tham Dự', default=0)
    so_su_co_thiet_bi = fields.Integer(string='Số Sự Cố Thiết Bị', default=0)
    so_cuoc_hop_bi_huy = fields.Integer(string='Số Cuộc Họp Bị Hủy', default=0)
    nguoi_dat_nhieu_nhat = fields.Many2one('res.users', string='Người Đặt Nhiều Nhất')
    ngay_thong_ke = fields.Date(string='Ngày Thống Kê', default=fields.Date.today)
    thoi_luong_trung_binh = fields.Float(string='Thời Lượng Trung Bình (phút)', default=0.0)
    tong_so_cuoc_hop = fields.Integer(string='Tổng Số Cuộc Họp', compute='_compute_tong_so_cuoc_hop', store=True)
    ty_le_su_dung = fields.Float(string='Tỷ Lệ Sử Dụng (%)', compute='_compute_ty_le_su_dung', store=True)

    @api.depends('phong_hop_id')
    def _compute_tong_so_cuoc_hop(self):
        for record in self:
            # Tính tổng số cuộc họp dựa trên lịch sử cuộc họp
            record.tong_so_cuoc_hop = self.env['lich_su_su_dung_phong'].search_count([
                ('cuoc_hop_id.phong_hop_id', '=', record.phong_hop_id.id)
            ])

    @api.depends('tong_so_cuoc_hop', 'thoi_luong_trung_binh')
    def _compute_ty_le_su_dung(self):
        for record in self:
            if record.tong_so_cuoc_hop > 0:
                record.ty_le_su_dung = (record.thoi_luong_trung_binh / (record.tong_so_cuoc_hop * 60)) * 100
            else:
                record.ty_le_su_dung = 0.0

    def action_update_statistics(self):
        # Cập nhật thông tin thống kê
        for record in self:
            # Logic để cập nhật số liệu thống kê
            record.so_nguoi_tham_du = self._calculate_attendees(record.phong_hop_id)
            record.so_su_co_thiet_bi = self._calculate_device_issues(record.phong_hop_id)
            record.so_cuoc_hop_bi_huy = self._calculate_cancelled_meetings(record.phong_hop_id)
            record.nguoi_dat_nhieu_nhat = self._find_top_booker(record.phong_hop_id)

    def _calculate_attendees(self, phong_hop):
        # Logic để tính số người tham dự
        return self.env['lich_su_su_dung_phong'].search_count([
            ('cuoc_hop_id.phong_hop_id', '=', phong_hop.id)
        ])

    def _calculate_device_issues(self, phong_hop):
        # Logic để tính số sự cố thiết bị
        return self.env['thiet_bi'].search_count([
            ('phong_hop_id', '=', phong_hop.id),
            ('trang_thai', '=', 'hong')
        ])

    def _calculate_cancelled_meetings(self, phong_hop):
        # Logic để tính số cuộc họp bị hủy
        return self.env['don_muon_phong'].search_count([
            ('phong_id', '=', phong_hop.id),
            ('trang_thai', '=', 'huy')
        ])

    def _find_top_booker(self, phong_hop):
        # Logic để tìm người đặt phòng nhiều nhất
        users = self.env['don_muon_phong'].read_group([
            ('phong_id', '=', phong_hop.id)
        ], ['nguoi_dat_phong'], ['nguoi_dat_phong'])
        if users:
            return max(users, key=lambda x: x['__count'])['nguoi_dat_phong']
        return False