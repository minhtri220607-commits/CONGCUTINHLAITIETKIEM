import streamlit as st
st.image("logo.jpg")
# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Tính Lãi Tiết Kiệm",
    page_icon="💰",
    layout="centered"
)

# Tiêu đề ứng dụng
st.title("💰 Công Cụ Tính Lãi Gửi Tiết Kiệm_Trần Đình Minh Trí")
st.write("Nhập các thông tin dưới đây để tính toán số tiền lãi dự kiến.")

# --- KHU VỰC NHẬP DỮ LIỆU ---
st.header("1. Thông tin khoản gửi")

# Số tiền gửi
so_tien_goc = st.number_input(
    "Số tiền gửi gốc (VNĐ):", 
    min_value=0, 
    value=10000000, 
    step=1000000, 
    format="%d"
)

# Kỳ hạn gửi
ky_han_thang = st.number_input(
    "Kỳ hạn gửi (tháng):", 
    min_value=1, 
    value=12, 
    step=1
)

# Lãi suất
lai_suat_nam = st.number_input(
    "Lãi suất (% / năm):", 
    min_value=0.0, 
    value=5.5, 
    step=0.1,
    format="%.2f"
)

# Hình thức nhận lãi
hinh_thuc_nhan = st.selectbox(
    "Hình thức nhận lãi:",
    options=["Cuối kỳ", "Hàng tháng", "Hàng quý"]
)

# Loại lãi
loai_lai = st.radio(
    "Chọn phương thức tính lãi:",
    options=["Lãi đơn", "Lãi kép"]
)

# --- XỬ LÝ LOGIC TÍNH TOÁN ---
# Đổi lãi suất năm thành lãi suất tháng
lai_suat_thang = (lai_suat_nam / 100) / 12

tong_tien_goc_va_lai = 0
tong_tien_lai = 0
tien_lai_dinh_ky = 0

if loai_lai == "Lãi đơn":
    # Công thức lãi đơn: Tiền lãi = Gốc * Lãi suất tháng * Số tháng
    tong_tien_lai = so_tien_goc * lai_suat_thang * ky_han_thang
    tong_tien_goc_va_lai = so_tien_goc + tong_tien_lai
    
    # Tính lãi định kỳ cho lãi đơn
    if hinh_thuc_nhan == "Hàng tháng":
        tien_lai_dinh_ky = so_tien_goc * lai_suat_thang
    elif hinh_thuc_nhan == "Hàng quý":
        tien_lai_dinh_ky = so_tien_goc * lai_suat_thang * 3
    else: # Cuối kỳ
        tien_lai_dinh_ky = tong_tien_lai

else: # Lãi kép
    if hinh_thuc_nhan == "Hàng tháng":
        # Lãi kép theo tháng
        tong_tien_goc_va_lai = so_tien_goc * ((1 + lai_suat_thang) ** ky_han_thang)
        tong_tien_lai = tong_tien_goc_va_lai - so_tien_goc
        # Lãi định kỳ trung bình mỗi tháng
        tien_lai_dinh_ky = tong_tien_lai / ky_han_thang 
        
    elif hinh_thuc_nhan == "Hàng quý":
        # Lãi kép theo quý (3 tháng 1 lần nhập gốc)
        so_quy = ky_han_thang / 3
        lai_suat_quy = lai_suat_thang * 3
        tong_tien_goc_va_lai = so_tien_goc * ((1 + lai_suat_quy) ** so_quy)
        tong_tien_lai = tong_tien_goc_va_lai - so_tien_goc
        # Lãi định kỳ trung bình mỗi quý
        tien_lai_dinh_ky = tong_tien_lai / so_quy if so_quy > 0 else 0
        
    else: # Cuối kỳ
        # Lãi kép nhập gốc vào cuối kỳ (bản chất giống lãi đơn nếu không tái tục nhiều kỳ)
        tong_tien_lai = so_tien_goc * lai_suat_thang * ky_han_thang
        tong_tien_goc_va_lai = so_tien_goc + tong_tien_lai
        tien_lai_dinh_ky = tong_tien_lai

# --- HIỂN THỊ KẾT QUẢ ---
st.header("2. Kết quả tính toán")

# Định dạng hiển thị tiền tệ VNĐ
def format_vnd(amount):
    return f"{amount:,.0f} VNĐ"

col1, col2 = st.columns(2)

with col1:
    st.metric("Tiền gốc ban đầu", format_vnd(so_tien_goc))
    st.metric("Tổng tiền lãi nhận được", format_vnd(tong_tien_lai))

with col2:
    st.metric("Lãi định kỳ phát sinh (" + hinh_thuc_nhan.lower() + ")", format_vnd(tien_lai_dinh_ky))
    st.metric("Tổng gốc + lãi thu về", format_vnd(tong_tien_goc_va_lai))

# Lưu ý nhỏ cho người dùng
st.info("⚠️ Lưu ý: Kết quả trên mang tính chất tham khảo dựa trên công thức toán học tiêu chuẩn. Thực tế tại ngân hàng có thể chênh lệch nhỏ tùy thuộc vào số ngày thực tế trong tháng/năm.")
