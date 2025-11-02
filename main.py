from PyQt6 import QtWidgets
from sinhhoatthang_ui import *
from xuly import *
import sys
# Định nghĩa các khu vực và phí rác tương ứng
cac_khu_vuc = ["Chọn khu vực", "Thành phố Thủ Đức và các quận", "Hóc Môn - Nhà Bè - Cần Giờ", "Bình Chánh - Củ Chi"]
phi_rac = {
    "Chọn khu vực": 0,
    "Thành phố Thủ Đức và các quận": 61000,
    "Hóc Môn - Nhà Bè - Cần Giờ": 57000,
    "Bình Chánh - Củ Chi": 57000
}

# Hộp thoại thông báo
def hien_canh_bao(title, message):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec()

# Chuyển văn bản thành số
def chuyen_doi(text):
    """
    Chuyển văn bản (text) sang số (float).
    Nếu văn bản bị trống hoặc không phải là số, nó sẽ trả về 0.0.
    """
    try:
        # Thay thế dấu phẩy (nếu người dùng nhập) và chuyển sang float
        return float(text.replace(',', ''))
    except (ValueError, TypeError):
        # Nếu lỗi (ví dụ: chuỗi rỗng ""), trả về 0
        return 0.0
def kiem_tra():
        dien_cu = chuyen_doi(form.lneDienCu.text()) 
        dien_moi = chuyen_doi(form.lneDienMoi.text())
        nuoc_cu = chuyen_doi(form.lneNuocCu.text())
        nuoc_moi = chuyen_doi(form.lneNuocMoi.text())

        # Kiểm tra dữ liệu nhập liệu
        if dien_moi > 0 and dien_moi < dien_cu:
            hien_canh_bao("Cảnh báo dữ liệu", 
                         "Chỉ số điện mới nhỏ hơn chỉ số cũ. Vui lòng kiểm tra lại.")
        
        if nuoc_moi > 0 and nuoc_moi < nuoc_cu:
            hien_canh_bao("Cảnh báo dữ liệu", 
                         "Chỉ số nước mới nhỏ hơn chỉ số cũ. Vui lòng kiểm tra lại.")

# Tính chi phí sinh hoạt
def tinh_chiphi():
    try:
        # Lấy dữ liệu từ giao diện
        dien_cu = chuyen_doi(form.lneDienCu.text()) 
        dien_moi = chuyen_doi(form.lneDienMoi.text())
        nuoc_cu = chuyen_doi(form.lneNuocCu.text())
        nuoc_moi = chuyen_doi(form.lneNuocMoi.text())

        # Tính tiền điện và nước
        kdien = dien_moi - dien_cu
        if kdien < 0: kdien = 0
        knuoc = nuoc_moi - nuoc_cu
        if knuoc < 0: knuoc = 0

        gia_dien = tien_dien(kdien)
        gia_nuoc = tien_nuoc(knuoc)

        # Tính tiền rác
        khu_vuc_text = form.cmbKhuVuc.currentText()
        phi = phi_rac.get(khu_vuc_text, 0)
        form.lblRacPhi.setText(f"Phí rác: {phi:,} ₫")

        # Cộng tổng chi phí
        tong_phi = gia_dien + gia_nuoc + phi
        form.lblTongPhi.setText(f"Tổng phí sinh hoạt: {tong_phi:,.0f} ₫")

        # Hiển thị kết quả
        form.lneGiaDien.setText(f"{gia_dien:,.0f} ₫")
        form.lneGiaNuoc.setText(f"{gia_nuoc:,.0f} ₫")

    except ValueError:
        form.lneGiaDien.setText("Vui lòng nhập đúng số liệu")
        form.lneGiaNuoc.setText("Vui lòng nhập đúng số liệu")

# Dọn giao diện
def clear_ui():
        form.lneDienCu.clear()
        form.lneDienMoi.clear()
        form.lneNuocCu.clear()
        form.lneNuocMoi.clear()
        form.cmbKhuVuc.setCurrentIndex(0)
        form.lneGiaDien.clear()
        form.lneGiaNuoc.clear()
        form.lblRacPhi.setText("Phí rác: 0 ₫")
        form.lblTongPhi.setText("Tổng phí sinh hoạt: 0 ₫")

# Kết nối các nút 
def setup_connections():
        # 1. Thêm các khu vực vào combobox
        form.cmbKhuVuc.addItems(cac_khu_vuc)

        # 2. Kết nối nút "Clear"
        form.btnClear.clicked.connect(clear_ui)

        # 3. Kết nối các ô nhập liệu để tự động tính chi phí khi có thay đổi
        form.lneDienCu.textChanged.connect(tinh_chiphi)
        form.lneDienMoi.textChanged.connect(tinh_chiphi)
        form.lneNuocCu.textChanged.connect(tinh_chiphi)
        form.lneNuocMoi.textChanged.connect(tinh_chiphi)
        form.lneDienMoi.editingFinished.connect(kiem_tra)
        form.lneNuocMoi.editingFinished.connect(kiem_tra)
        form.cmbKhuVuc.currentIndexChanged.connect(tinh_chiphi)

        # 4. Kết nối nút "Tính"
        form.btnTinh.clicked.connect(tinh_chiphi)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    form = Ui_SinhHoatThang()
    form.setupUi(window)
    setup_connections()
    window.show()
    app.exec()