import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pathlib import Path
import base64
import uuid

# =========================================================
# CẤU HÌNH
# =========================================================

st.set_page_config(
    page_title="Charm Pearl Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE = Path(__file__).parent

LOGO = BASE / "IMG_LOGO11.jpg"
BANNER = BASE / "IMG_BANNER2.jpg"
BG = BASE / "IMG_NENCHIM3.jpg"

HOTEL_NAME = "CHARM PEARL HOTEL"
LOCATION = "VŨNG TÀU"

# =========================================================
# DỮ LIỆU HẠNG PHÒNG
# =========================================================

ROOM_TYPES = {
    "Standard": {
        "price": 550000,
        "capacity": 2,
        "description": "Phòng tiêu chuẩn, phù hợp cho 1–2 khách."
    },
    "Deluxe": {
        "price": 750000,
        "capacity": 2,
        "description": "Phòng rộng rãi, tiện nghi hiện đại."
    },
    "Suite": {
        "price": 1200000,
        "capacity": 3,
        "description": "Không gian cao cấp, phù hợp nghỉ dưỡng."
    },
    "Family": {
        "price": 1500000,
        "capacity": 4,
        "description": "Phòng dành cho gia đình hoặc nhóm nhỏ."
    }
}

STATUSES = [
    "Trống",
    "Đã đặt",
    "Đang ở",
    "Đang dọn",
    "Bảo trì"
]

# =========================================================
# HÀM TIỆN ÍCH
# =========================================================

def money(value):
    return f"{int(value):,}".replace(",", ".") + " VNĐ"


def img_to_base64(path):
    if not path.exists():
        return None

    try:
        return base64.b64encode(path.read_bytes()).decode()
    except Exception:
        return None


def status_icon(status):
    icons = {
        "Trống": "🟢",
        "Đã đặt": "🟣",
        "Đang ở": "🔵",
        "Đang dọn": "🟡",
        "Bảo trì": "🔴"
    }
    return icons.get(status, "⚪")


# =========================================================
# TẠO 50 PHÒNG
# =========================================================

def create_rooms():

    rooms = []

    room_counter = 1

    for floor in range(1, 6):

        for position in range(1, 11):

            room_number = f"{floor}{position:02d}"

            if position <= 4:
                room_type = "Standard"

            elif position <= 8:
                room_type = "Deluxe"

            elif position == 9:
                room_type = "Suite"

            else:
                room_type = "Family"

            rooms.append({
                "Phòng": room_number,
                "Tầng": floor,
                "Loại phòng": room_type,
                "Giá": ROOM_TYPES[room_type]["price"],
                "Sức chứa": ROOM_TYPES[room_type]["capacity"],
                "Trạng thái": "Trống"
            })

            room_counter += 1

    return pd.DataFrame(rooms)


# =========================================================
# SESSION STATE
# =========================================================

if "rooms" not in st.session_state:
    st.session_state.rooms = create_rooms()

if "bookings" not in st.session_state:
    st.session_state.bookings = []

if "services" not in st.session_state:
    st.session_state.services = [
        {
            "Mã": "DV001",
            "Tên dịch vụ": "Ăn sáng",
            "Đơn giá": 100000
        },
        {
            "Mã": "DV002",
            "Tên dịch vụ": "Cà phê",
            "Đơn giá": 45000
        },
        {
            "Mã": "DV003",
            "Tên dịch vụ": "Giặt ủi",
            "Đơn giá": 80000
        },
        {
            "Mã": "DV004",
            "Tên dịch vụ": "Minibar",
            "Đơn giá": 60000
        },
        {
            "Mã": "DV005",
            "Tên dịch vụ": "Extra Bed",
            "Đơn giá": 200000
        },
        {
            "Mã": "DV006",
            "Tên dịch vụ": "Spa",
            "Đơn giá": 300000
        },
        {
            "Mã": "DV007",
            "Tên dịch vụ": "Đưa đón sân bay",
            "Đơn giá": 350000
        }
    ]

if "guest_chat" not in st.session_state:
    st.session_state.guest_chat = []

if "guest_name" not in st.session_state:
    st.session_state.guest_name = "Khách"


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f4f7f8;
    font-family: Arial, sans-serif;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #082f3d 0%,
        #0d4658 50%,
        #092d3a 100%
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* HEADER */

.main-title {
    text-align: center;
    color: #123e4d;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-top: 10px;
}

.main-subtitle {
    text-align: center;
    color: #71838b;
    font-size: 16px;
    margin-bottom: 25px;
}

/* CARD */

.info-card {
    background: rgba(255,255,255,0.96);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #e3eaed;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    min-height: 125px;
}

.info-label {
    color: #71818a;
    font-size: 14px;
}

.info-value {
    color: #123e4d;
    font-size: 27px;
    font-weight: 800;
    margin-top: 8px;
}

/* ROOM CARD */

.room-card {
    background: rgba(255,255,255,0.97);
    border-radius: 15px;
    padding: 15px;
    border: 1px solid #dfe7ea;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    min-height: 145px;
    margin-bottom: 8px;
}

.room-number {
    color: #123e4d;
    font-size: 23px;
    font-weight: 800;
}

.room-type {
    color: #71818a;
    font-size: 13px;
    margin-top: 4px;
}

.room-price {
    color: #345762;
    font-size: 13px;
    margin-top: 7px;
}

.room-status {
    margin-top: 10px;
    font-weight: 700;
}

/* SECTION */

.section-title {
    color: #123e4d;
    font-size: 25px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* CHAT */

.chat-wrapper {
    background: white;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #dfe7ea;
}

.chat-user {
    background: #e6f3f7;
    border-radius: 15px;
    padding: 12px 15px;
    margin: 8px 0 8px 15%;
}

.chat-bot {
    background: #f1f4f5;
    border-radius: 15px;
    padding: 12px 15px;
    margin: 8px 15% 8px 0;
}

.chat-name {
    font-weight: 700;
    font-size: 13px;
    color: #315866;
}

/* BUTTON */

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# NỀN CHÌM
# =========================================================

bg64 = img_to_base64(BG)

if bg64:

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
            linear-gradient(
                rgba(244,247,248,0.94),
                rgba(244,247,248,0.94)
            ),
            url("data:image/jpeg;base64,{bg64}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    if LOGO.exists():
        st.image(str(LOGO), width=85)

    st.markdown("## CHARM PEARL")
    st.caption("HOTEL MANAGEMENT SYSTEM")

    st.divider()

    menu = st.radio(
        "MENU QUẢN LÝ",
        [
            "🏠 Dashboard",
            "🛏️ Quản lý phòng",
            "📅 Đặt phòng",
            "🛎️ Check-in",
            "🚪 Check-out",
            "👥 Khách hàng",
            "🍽️ Dịch vụ",
            "🧾 Hóa đơn",
            "💰 Doanh thu",
            "📊 Báo cáo",
            "💬 Chat với khách"
        ]
    )

    st.divider()

    st.caption("CHARM PEARL HOTEL")
    st.caption("Vũng Tàu")
    st.caption("50 phòng · 5 tầng")


# =========================================================
# DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">CHARM PEARL HOTEL</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">Hotel Management System · Vũng Tàu</div>',
        unsafe_allow_html=True
    )

    # BANNER
    if BANNER.exists():

        c1, c2, c3 = st.columns([1, 3, 1])

        with c2:
            st.image(
                str(BANNER),
                use_container_width=True
            )

    st.markdown(
        '<div class="section-title">Tổng quan khách sạn</div>',
        unsafe_allow_html=True
    )

    rooms = st.session_state.rooms

    total_rooms = len(rooms)

    empty_rooms = len(
        rooms[rooms["Trạng thái"] == "Trống"]
    )

    reserved_rooms = len(
        rooms[rooms["Trạng thái"] == "Đã đặt"]
    )

    occupied_rooms = len(
        rooms[rooms["Trạng thái"] == "Đang ở"]
    )

    bookings = st.session_state.bookings

    revenue = sum(
        b["Tổng tiền"] for b in bookings
    )

    cards = st.columns(5)

    values = [
        ("🏨", "Tổng phòng", total_rooms),
        ("🟢", "Phòng trống", empty_rooms),
        ("🟣", "Đã đặt", reserved_rooms),
        ("🔵", "Đang ở", occupied_rooms),
        ("💰", "Doanh thu", money(revenue))
    ]

    for col, item in zip(cards, values):

        with col:

            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-label">
                        {item[0]} {item[1]}
                    </div>

                    <div class="info-value">
                        {item[2]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # =====================================================
    # SƠ ĐỒ PHÒNG
    # =====================================================

    st.markdown(
        '<div class="section-title">Sơ đồ phòng</div>',
        unsafe_allow_html=True
    )

    floor = st.selectbox(
        "Chọn tầng",
        ["Tất cả", 1, 2, 3, 4, 5],
        key="dashboard_floor"
    )

    if floor == "Tất cả":
        display_rooms = rooms.copy()
    else:
        display_rooms = rooms[
            rooms["Tầng"] == floor
        ].copy()

    # 5 cột cố định
    cols = st.columns(5)

    for i in range(len(display_rooms)):

        room = display_rooms.iloc[i]

        with cols[i % 5]:

            st.markdown(
                f"""
                <div class="room-card">

                    <div class="room-number">
                        🛏️ {room["Phòng"]}
                    </div>

                    <div class="room-type">
                        {room["Loại phòng"]} ·
                        Tầng {room["Tầng"]}
                    </div>

                    <div class="room-price">
                        {money(room["Giá"])} / đêm
                    </div>

                    <div class="room-status">
                        {status_icon(room["Trạng thái"])}
                        {room["Trạng thái"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Quản lý phòng":

    st.title("🛏️ Quản lý phòng")

    rooms = st.session_state.rooms.copy()

    c1, c2, c3 = st.columns(3)

    with c1:

        floor_filter = st.selectbox(
            "Tầng",
            ["Tất cả", 1, 2, 3, 4, 5],
            key="room_floor"
        )

    with c2:

        type_filter = st.selectbox(
            "Loại phòng",
            ["Tất cả"] + list(ROOM_TYPES.keys()),
            key="room_type"
        )

    with c3:

        status_filter = st.selectbox(
            "Trạng thái",
            ["Tất cả"] + STATUSES,
            key="room_status"
        )

    result = rooms.copy()

    if floor_filter != "Tất cả":

        result = result[
            result["Tầng"] == floor_filter
        ]

    if type_filter != "Tất cả":

        result = result[
            result["Loại phòng"] == type_filter
        ]

    if status_filter != "Tất cả":

        result = result[
            result["Trạng thái"] == status_filter
        ]

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Cập nhật trạng thái phòng")

    with st.form("update_room_form"):

        room_number = st.selectbox(
            "Chọn phòng",
            rooms["Phòng"].tolist()
        )

        new_status = st.selectbox(
            "Trạng thái mới",
            STATUSES
        )

        save_room = st.form_submit_button(
            "CẬP NHẬT PHÒNG",
            use_container_width=True
        )

    if save_room:

        st.session_state.rooms.loc[
            st.session_state.rooms["Phòng"] == room_number,
            "Trạng thái"
        ] = new_status

        st.success(
            f"Phòng {room_number} đã chuyển sang "
            f"trạng thái: {new_status}"
        )

        st.rerun()


# =========================================================
# ĐẶT PHÒNG
# =========================================================

elif menu == "📅 Đặt phòng":

    st.title("📅 Đặt phòng")

    st.info(
        "Chọn ngày lưu trú, hạng phòng và phòng còn trống."
    )

    c1, c2 = st.columns(2)

    with c1:

        check_in = st.date_input(
            "Ngày check-in",
            date.today(),
            key="booking_checkin"
        )

    with c2:

        check_out = st.date_input(
            "Ngày check-out",
            date.today() + timedelta(days=1),
            key="booking_checkout"
        )

    if check_out <= check_in:

        st.error(
            "Ngày check-out phải sau ngày check-in."
        )

    else:

        nights = (
            check_out - check_in
        ).days

        room_type = st.selectbox(
            "Hạng phòng",
            list(ROOM_TYPES.keys()),
            key="booking_type"
        )

        suitable = st.session_state.rooms[
            st.session_state.rooms["Loại phòng"] == room_type
        ]

        available = suitable[
            suitable["Trạng thái"] == "Trống"
        ]

        st.write(
            f"**Còn {len(available)} phòng {room_type}**"
        )

        if available.empty:

            st.warning(
                "Hiện không còn phòng trống thuộc hạng này."
            )

        else:

            room = st.selectbox(
                "Chọn phòng",
                available["Phòng"].tolist(),
                key="booking_room"
            )

            c1, c2 = st.columns(2)

            with c1:

                guest_name = st.text_input(
                    "Họ tên khách *",
                    key="guest_name_booking"
                )

                phone = st.text_input(
                    "Số điện thoại *",
                    key="guest_phone"
                )

            with c2:

                capacity = ROOM_TYPES[
                    room_type
                ]["capacity"]

                guest_count = st.number_input(
                    "Số khách",
                    min_value=1,
                    max_value=capacity,
                    value=1,
                    key="guest_count"
                )

                note = st.text_area(
                    "Ghi chú",
                    key="booking_note"
                )

            room_price = ROOM_TYPES[
                room_type
            ]["price"]

            total_room = room_price * nights

            st.success(
                f"Phòng {room} · {nights} đêm · "
                f"{money(total_room)}"
            )

            if st.button(
                "📅 XÁC NHẬN ĐẶT PHÒNG",
                type="primary",
                use_container_width=True
            ):

                if not guest_name.strip():

                    st.error(
                        "Vui lòng nhập tên khách."
                    )

                elif not phone.strip():

                    st.error(
                        "Vui lòng nhập số điện thoại."
                    )

                else:

                    booking_id = (
                        "CP"
                        + date.today().strftime("%y%m%d")
                        + str(uuid.uuid4())[:4].upper()
                    )

                    booking = {
                        "Mã booking": booking_id,
                        "Phòng": room,
                        "Khách hàng": guest_name,
                        "Số điện thoại": phone,
                        "Số khách": guest_count,
                        "Check-in": check_in,
                        "Check-out": check_out,
                        "Số đêm": nights,
                        "Tiền phòng": total_room,
                        "Dịch vụ": 0,
                        "Tổng tiền": total_room,
                        "Trạng thái": "Đã đặt",
                        "Ghi chú": note
                    }

                    st.session_state.bookings.append(
                        booking
                    )

                    st.session_state.rooms.loc[
                        st.session_state.rooms["Phòng"] == room,
                        "Trạng thái"
                    ] = "Đã đặt"

                    st.success(
                        f"Đặt phòng thành công! "
                        f"Mã booking: {booking_id}"
                    )

                    st.balloons()


# =========================================================
# CHECK-IN
# =========================================================

elif menu == "🛎️ Check-in":

    st.title("🛎️ Check-in")

    bookings = st.session_state.bookings

    waiting = [
        b for b in bookings
        if b["Trạng thái"] == "Đã đặt"
    ]

    if not waiting:

        st.info(
            "Hiện không có booking chờ check-in."
        )

    else:

        booking_ids = [
            b["Mã booking"]
            for b in waiting
        ]

        selected_id = st.selectbox(
            "Chọn booking",
            booking_ids
        )

        selected = next(
            b for b in waiting
            if b["Mã booking"] == selected_id
        )

        st.markdown(
            f"""
            **Khách hàng:** {selected["Khách hàng"]}

            **Phòng:** {selected["Phòng"]}

            **Check-in:** {selected["Check-in"]}

            **Check-out:** {selected["Check-out"]}

            **Số khách:** {selected["Số khách"]}
            """
        )

        if st.button(
            "🛎️ XÁC NHẬN CHECK-IN",
            type="primary",
            use_container_width=True
        ):

            for b in st.session_state.bookings:

                if b["Mã booking"] == selected_id:
                    b["Trạng thái"] = "Đang ở"

            st.session_state.rooms.loc[
                st.session_state.rooms["Phòng"]
                == selected["Phòng"],
                "Trạng thái"
            ] = "Đang ở"

            st.success(
                "Check-in thành công."
            )

            st.rerun()


# =========================================================
# CHECK-OUT
# =========================================================

elif menu == "🚪 Check-out":

    st.title("🚪 Check-out")

    staying = [
        b for b in st.session_state.bookings
        if b["Trạng thái"] == "Đang ở"
    ]

    if not staying:

        st.info(
            "Hiện không có khách đang ở."
        )

    else:

        booking_ids = [
            b["Mã booking"]
            for b in staying
        ]

        selected_id = st.selectbox(
            "Booking",
            booking_ids
        )

        selected = next(
            b for b in staying
            if b["Mã booking"] == selected_id
        )

        st.write(
            f"**Khách:** {selected['Khách hàng']}"
        )

        st.write(
            f"**Phòng:** {selected['Phòng']}"
        )

        extra = st.number_input(
            "Dịch vụ phát sinh",
            min_value=0,
            step=50000
        )

        total = selected["Tiền phòng"] + extra

        st.metric(
            "Tổng thanh toán",
            money(total)
        )

        if st.button(
            "💳 THANH TOÁN & CHECK-OUT",
            type="primary",
            use_container_width=True
        ):

            for b in st.session_state.bookings:

                if b["Mã booking"] == selected_id:

                    b["Dịch vụ"] = extra
                    b["Tổng tiền"] = total
                    b["Trạng thái"] = "Đã trả phòng"

            st.session_state.rooms.loc[
                st.session_state.rooms["Phòng"]
                == selected["Phòng"],
                "Trạng thái"
            ] = "Đang dọn"

            st.success(
                "Check-out thành công. "
                "Phòng đã chuyển sang trạng thái đang dọn."
            )

            st.rerun()


# =========================================================
# KHÁCH HÀNG
# =========================================================

elif menu == "👥 Khách hàng":

    st.title("👥 Khách hàng")

    bookings = st.session_state.bookings

    if not bookings:

        st.info(
            "Chưa có dữ liệu khách hàng."
        )

    else:

        df = pd.DataFrame(bookings)

        keyword = st.text_input(
            "🔎 Tìm khách hàng"
        )

        if keyword:

            mask = df.astype(str).apply(
                lambda column:
                column.str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            ).any(axis=1)

            df = df[mask]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# DỊCH VỤ
# =========================================================

elif menu == "🍽️ Dịch vụ":

    st.title("🍽️ Dịch vụ khách sạn")

    service_df = pd.DataFrame(
        st.session_state.services
    )

    st.dataframe(
        service_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Thêm dịch vụ")

    with st.form("new_service"):

        c1, c2, c3 = st.columns(3)

        with c1:

            code = st.text_input(
                "Mã dịch vụ"
            )

        with c2:

            name = st.text_input(
                "Tên dịch vụ"
            )

        with c3:

            price = st.number_input(
                "Đơn giá",
                min_value=0,
                step=10000
            )

        submit = st.form_submit_button(
            "THÊM DỊCH VỤ",
            use_container_width=True
        )

    if submit:

        if not code or not name:

            st.error(
                "Vui lòng nhập đầy đủ thông tin."
            )

        else:

            st.session_state.services.append(
                {
                    "Mã": code,
                    "Tên dịch vụ": name,
                    "Đơn giá": price
                }
            )

            st.success(
                "Đã thêm dịch vụ."
            )

            st.rerun()


# =========================================================
# HÓA ĐƠN
# =========================================================

elif menu == "🧾 Hóa đơn":

    st.title("🧾 Hóa đơn")

    bookings = st.session_state.bookings

    if not bookings:

        st.info(
            "Chưa có booking để lập hóa đơn."
        )

    else:

        booking_ids = [
            b["Mã booking"]
            for b in bookings
        ]

        selected_id = st.selectbox(
            "Chọn booking",
            booking_ids
        )

        invoice = next(
            b for b in bookings
            if b["Mã booking"] == selected_id
        )

        st.markdown("---")

        st.markdown(
            f"""
            ## {HOTEL_NAME}

            **Địa điểm:** {LOCATION}

            **Mã booking:** {invoice["Mã booking"]}

            **Khách hàng:** {invoice["Khách hàng"]}

            **Số điện thoại:** {invoice["Số điện thoại"]}

            **Phòng:** {invoice["Phòng"]}

            **Check-in:** {invoice["Check-in"]}

            **Check-out:** {invoice["Check-out"]}

            **Số đêm:** {invoice["Số đêm"]}

            ---

            **Tiền phòng:** {money(invoice["Tiền phòng"])}

            **Dịch vụ:** {money(invoice["Dịch vụ"])}

            ### TỔNG THANH TOÁN: {money(invoice["Tổng tiền"])}
            """
        )


# =========================================================
# DOANH THU
# =========================================================

elif menu == "💰 Doanh thu":

    st.title("💰 Doanh thu")

    bookings = st.session_state.bookings

    room_revenue = sum(
        b["Tiền phòng"]
        for b in bookings
    )

    service_revenue = sum(
        b["Dịch vụ"]
        for b in bookings
    )

    total_revenue = (
        room_revenue
        + service_revenue
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Doanh thu phòng",
            money(room_revenue)
        )

    with c2:
        st.metric(
            "Doanh thu dịch vụ",
            money(service_revenue)
        )

    with c3:
        st.metric(
            "Tổng doanh thu",
            money(total_revenue)
        )

    chart = pd.DataFrame(
        {
            "Khoản thu": [
                "Phòng",
                "Dịch vụ"
            ],
            "Doanh thu": [
                room_revenue,
                service_revenue
            ]
        }
    )

    st.bar_chart(
        chart.set_index("Khoản thu")
    )


# =========================================================
# BÁO CÁO
# =========================================================

elif menu == "📊 Báo cáo":

    st.title("📊 Báo cáo khách sạn")

    rooms = st.session_state.rooms

    counts = (
        rooms["Trạng thái"]
        .value_counts()
        .reindex(
            STATUSES,
            fill_value=0
        )
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Tổng phòng",
            len(rooms)
        )

    with c2:
        st.metric(
            "Phòng trống",
            int(counts["Trống"])
        )

    with c3:
        st.metric(
            "Đang ở",
            int(counts["Đang ở"])
        )

    with c4:
        st.metric(
            "Bảo trì",
            int(counts["Bảo trì"])
        )

    st.subheader("Thống kê trạng thái phòng")

    chart = pd.DataFrame(
        {
            "Trạng thái": counts.index,
            "Số phòng": counts.values
        }
    )

    st.bar_chart(
        chart.set_index("Trạng thái")
    )

    st.subheader("Danh sách 50 phòng")

    st.dataframe(
        rooms,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# CHATBOX KHÁCH HÀNG
# =========================================================

elif menu == "💬 Chat với khách":

    st.title("💬 Chat với Charm Pearl Hotel")

    st.caption(
        "Kênh tư vấn trực tuyến dành cho khách hàng"
    )

    # Tên khách
    name = st.text_input(
        "Tên khách hàng",
        value=st.session_state.guest_name
    )

    if name.strip():

        st.session_state.guest_name = name

    st.divider()

    # =====================================================
    # HÀM CHATBOT
    # =====================================================

    def chatbot_reply(message):

        text = message.lower().strip()

        rooms = st.session_state.rooms

        # Chào hỏi
        if any(
            word in text
            for word in [
                "xin chào",
                "hello",
                "hi",
                "chào"
            ]
        ):

            return (
                f"Xin chào {st.session_state.guest_name}! "
                "Chào mừng bạn đến với Charm Pearl Hotel Vũng Tàu. "
                "Tôi có thể hỗ trợ bạn về phòng, giá phòng, "
                "đặt phòng, check-in, check-out và dịch vụ."
            )

        # Giá phòng
        if (
            "giá" in text
            or "bao nhiêu" in text
            or "phòng bao nhiêu" in text
        ):

            return (
                "Giá phòng hiện tại của Charm Pearl Hotel:\n\n"
                f"• Standard: {money(ROOM_TYPES['Standard']['price'])}/đêm\n"
                f"• Deluxe: {money(ROOM_TYPES['Deluxe']['price'])}/đêm\n"
                f"• Suite: {money(ROOM_TYPES['Suite']['price'])}/đêm\n"
                f"• Family: {money(ROOM_TYPES['Family']['price'])}/đêm"
            )

        # Loại phòng
        if (
            "loại phòng" in text
            or "hạng phòng" in text
            or "có phòng gì" in text
        ):

            return (
                "Charm Pearl Hotel hiện có 4 hạng phòng:\n\n"
                "• Standard – tối đa 2 khách\n"
                "• Deluxe – tối đa 2 khách\n"
                "• Suite – tối đa 3 khách\n"
                "• Family – tối đa 4 khách\n\n"
                "Bạn muốn xem thông tin hạng phòng nào?"
            )

        # Standard
        if "standard" in text:

            info = ROOM_TYPES["Standard"]

            return (
                f"Phòng Standard có giá "
                f"{money(info['price'])}/đêm, "
                f"sức chứa tối đa {info['capacity']} khách. "
                f"{info['description']}"
            )

        # Deluxe
        if "deluxe" in text:

            info = ROOM_TYPES["Deluxe"]

            return (
                f"Phòng Deluxe có giá "
                f"{money(info['price'])}/đêm, "
                f"sức chứa tối đa {info['capacity']} khách. "
                f"{info['description']}"
            )

        # Suite
        if "suite" in text:

            info = ROOM_TYPES["Suite"]

            return (
                f"Phòng Suite có giá "
                f"{money(info['price'])}/đêm, "
                f"sức chứa tối đa {info['capacity']} khách. "
                f"{info['description']}"
            )

        # Family
        if "family" in text:

            info = ROOM_TYPES["Family"]

            return (
                f"Phòng Family có giá "
                f"{money(info['price'])}/đêm, "
                f"sức chứa tối đa {info['capacity']} khách. "
                f"{info['description']}"
            )

        # Phòng trống
        if (
            "còn phòng" in text
            or "phòng trống" in text
            or "phòng nào còn" in text
        ):

            available = rooms[
                rooms["Trạng thái"] == "Trống"
            ]

            if available.empty:

                return (
                    "Hiện tại hệ thống không còn phòng "
                    "trống. Bạn vui lòng chọn ngày khác."
                )

            counts = (
                available["Loại phòng"]
                .value_counts()
            )

            reply = "Hiện tại khách sạn còn:\n\n"

            for room_type in ROOM_TYPES:

                number = int(
                    counts.get(room_type, 0)
                )

                reply += (
                    f"• {room_type}: {number} phòng\n"
                )

            return reply

        # Check-in
        if "check-in" in text or "nhận phòng" in text:

            return (
                "Giờ check-in dự kiến: 14:00. "
                "Nếu bạn đến sớm, khách sạn có thể hỗ trợ "
                "tùy tình trạng phòng thực tế."
            )

        # Check-out
        if "check-out" in text or "trả phòng" in text:

            return (
                "Giờ check-out dự kiến: 12:00. "
                "Bạn có thể liên hệ lễ tân nếu cần hỗ trợ "
                "trả phòng muộn."
            )

        # Địa điểm
        if (
            "ở đâu" in text
            or "địa chỉ" in text
            or "vũng tàu" in text
            or "địa điểm" in text
        ):

            return (
                "Charm Pearl Hotel tọa lạc tại Vũng Tàu, "
                "phù hợp cho kỳ nghỉ biển và du lịch cuối tuần."
            )

        # Dịch vụ
        if (
            "dịch vụ" in text
            or "spa" in text
            or "ăn sáng" in text
            or "giặt" in text
        ):

            return (
                "Khách sạn hiện cung cấp các dịch vụ như "
                "ăn sáng, cà phê, giặt ủi, minibar, "
                "Extra Bed, Spa và đưa đón sân bay."
            )

        # Đặt phòng
        if (
            "đặt phòng" in text
            or "booking" in text
            or "book phòng" in text
        ):

            return (
                "Bạn có thể vào mục '📅 Đặt phòng' "
                "trên menu để kiểm tra phòng trống và "
                "tạo booking. Hệ thống sẽ tự động cấp mã booking."
            )

        # Cảm ơn
        if "cảm ơn" in text:

            return (
                "Rất hân hạnh được hỗ trợ bạn. "
                "Charm Pearl Hotel chúc bạn có một kỳ nghỉ "
                "thật thoải mái tại Vũng Tàu."
            )

        # Mặc định
        return (
            "Tôi có thể hỗ trợ bạn về:\n\n"
            "• Giá phòng\n"
            "• Các hạng phòng\n"
            "• Phòng còn trống\n"
            "• Đặt phòng\n"
            "• Check-in / Check-out\n"
            "• Dịch vụ khách sạn\n"
            "• Thông tin khách sạn\n\n"
            "Bạn muốn hỏi nội dung nào?"
        )

    # =====================================================
    # HIỂN THỊ CHAT
    # =====================================================

    st.markdown(
        '<div class="chat-wrapper">',
        unsafe_allow_html=True
    )

    if not st.session_state.guest_chat:

        st.markdown(
            """
            <div class="chat-bot">
                <div class="chat-name">
                    🏨 Charm Pearl Hotel
                </div>
                Xin chào! Tôi là trợ lý trực tuyến của
                Charm Pearl Hotel. Tôi có thể hỗ trợ bạn
                tìm hiểu phòng và dịch vụ khách sạn.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        for chat in st.session_state.guest_chat:

            if chat["role"] == "user":

                st.markdown(
                    f"""
                    <div class="chat-user">
                        <div class="chat-name">
                            👤 {st.session_state.guest_name}
                        </div>
                        {chat["message"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="chat-bot">
                        <div class="chat-name">
                            🏨 Charm Pearl Hotel
                        </div>
                        {chat["message"].replace(chr(10), "<br>")}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.divider()

    # =====================================================
    # Ô NHẬP CHAT
    # =====================================================

    with st.form("guest_chat_form", clear_on_submit=True):

        message = st.text_input(
            "Tin nhắn",
            placeholder="Nhập câu hỏi của khách..."
        )

        send = st.form_submit_button(
            "GỬI TIN NHẮN",
            use_container_width=True
        )

    if send and message.strip():

        st.session_state.guest_chat.append(
            {
                "role": "user",
                "message": message.strip()
            }
        )

        reply = chatbot_reply(
            message.strip()
        )

        st.session_state.guest_chat.append(
            {
                "role": "bot",
                "message": reply
            }
        )

        st.rerun()

    if st.button(
        "🗑️ Xóa cuộc trò chuyện",
        use_container_width=True
    ):

        st.session_state.guest_chat = []

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "© Charm Pearl Hotel · Vũng Tàu · "
    "Hotel Management System · 50 Rooms"
)
