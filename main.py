from PyQt6 import QtWidgets
from sinhhoatthang_ui import *
from xuly import *
import sys
# Định nghĩa các khu vực và phí rác tương ứng

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
        return float(text.replace(',', '.'))
    except (ValueError, TypeError):
        if text != "":
            hien_canh_bao("Cảnh báo", "Chỉ được nhập số.")
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
def tinh_dien():
    dien_cu = chuyen_doi(form.lneDienCu.text()) 
    dien_moi = chuyen_doi(form.lneDienMoi.text())
    kdien = dien_moi - dien_cu
    if kdien < 0: kdien = 0
    gia_dien = tien_dien(kdien)
    form.lneGiaDien.setText(f"{gia_dien * 1.1:,.0f} ₫")

def tinh_nuoc():
    nuoc_cu = chuyen_doi(form.lneNuocCu.text()) 
    nuoc_moi = chuyen_doi(form.lneNuocMoi.text())
    knuoc = nuoc_moi - nuoc_cu 
    if knuoc < 0: knuoc = 0
    gia_nuoc = tien_nuoc(knuoc)
    form.lneGiaNuoc.setText(f"{gia_nuoc * 1.1:,.0f} ₫")

def tinh_rac():
    khu_vuc_text = form.cmbKhuVuc.currentText()
    phi = phi_rac.get(khu_vuc_text, 0)
    form.lblRacPhi.setText(f"Phí rác: {phi:,} ₫")

def tinh_tong_phi():
    # Lấy giá điện
    gia_dien = chuyen_doi(form.lneGiaDien.text().replace('₫', '').replace(',', ''))
    # Lấy giá nước
    gia_nuoc = chuyen_doi(form.lneGiaNuoc.text().replace('₫', '').replace(',', ''))
    # Lấy phí rác
    phi = 0
    text_rac = form.lblRacPhi.text().replace('Phí rác:', '').replace('₫', '').replace(',', '').strip()
    if text_rac:
        phi = chuyen_doi(text_rac)
    tong = gia_dien + gia_nuoc + phi
    form.lblTongPhi.setText(f"Tổng phí sinh hoạt: {tong:,.0f} ₫ (Đã tính thuế 10%)")

# Kết nối các nút 
def setup_connections():
    form.cmbKhuVuc.addItems(phi_rac.keys())

    # Điện
    form.lneDienCu.textChanged.connect(tinh_dien)
    form.lneDienMoi.textChanged.connect(tinh_dien)
    form.lneDienMoi.editingFinished.connect(kiem_tra)

    # Nước
    form.lneNuocCu.textChanged.connect(tinh_nuoc)
    form.lneNuocMoi.textChanged.connect(tinh_nuoc)
    form.lneNuocMoi.editingFinished.connect(kiem_tra)

    # Rác
    form.cmbKhuVuc.currentIndexChanged.connect(tinh_rac)

    # Chỉ khi bấm "Tính" mới cộng tổng
    form.btnTinh.clicked.connect(tinh_tong_phi)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    form = Ui_SinhHoatThang()
    form.setupUi(window)
    setup_connections()
    window.show()
    app.exec()
