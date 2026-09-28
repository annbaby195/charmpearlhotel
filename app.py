import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pathlib import Path
import base64


# =========================================================
# CẤU HÌNH APP
# =========================================================

st.set_page_config(
    page_title="Charm Pearl Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent

LOGO_PATH = BASE_DIR / "IMG_LOGO1.jpg"
BANNER_PATH = BASE_DIR / "IMG_BANNER2.jpg"
BACKGROUND_PATH = BASE_DIR / "IMG_NENCHIM3.jpg"


# =========================================================
# THÔNG TIN KHÁCH SẠN
# =========================================================

HOTEL_NAME = "Charm Pearl Hotel"
HOTEL_LOCATION = "Vũng Tàu"
TOTAL_ROOMS = 50


# =========================================================
# LOẠI PHÒNG
# =========================================================

ROOM_TYPES = {
    "Standard": {
        "price": 550000,
        "capacity": 2
    },
    "Deluxe": {
        "price": 750000,
        "capacity": 2
    },
    "Suite": {
        "price": 1200000,
        "capacity": 3
    },
    "Family": {
        "price": 1500000,
        "capacity": 4
    }
}


ROOM_STATUS = [
    "Trống",
    "Đã đặt",
    "Đang ở",
    "Đang dọn",
    "Bảo trì"
]


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================

def format_money(number):
    return f"{int(number):,}".replace(",", ".") + " VNĐ"


def room_status_icon(status):
    icons = {
        "Trống": "🟢",
        "Đã đặt": "🟣",
        "Đang ở": "🔵",
        "Đang dọn": "🟡",
        "Bảo trì": "🔴"
    }

    return icons.get(status, "⚪")


def image_exists(path):
    return path.exists() and path.is_file()


# =========================================================
# TẠO 50 PHÒNG
# =========================================================

def create_rooms():

    rooms = []

    for floor in range(1, 6):

        for number in range(1, 11):

            room_number = f"{floor}{number:02d}"

            if number <= 4:
                room_type = "Standard"

            elif number <= 8:
                room_type = "Deluxe"

            elif number == 9:
                room_type = "Suite"

            else:
                room_type = "Family"

            rooms.append({
                "Phòng": room_number,
                "Tầng": floor,
                "Loại phòng": room_type,
                "Giá/đêm": ROOM_TYPES[room_type]["price"],
                "Sức chứa": ROOM_TYPES[room_type]["capacity"],
                "Trạng thái": "Trống"
            })

    return pd.DataFrame(rooms)


# =========================================================
# SESSION STATE
# =========================================================

if "rooms" not in st.session_state:
    st.session_state.rooms = create_rooms()


if "bookings" not in st.session_state:

    st.session_state.bookings = pd.DataFrame(
        columns=[
            "Mã đặt phòng",
            "Phòng",
            "Tên khách",
            "Số điện thoại",
            "Số khách",
            "Ngày nhận",
            "Ngày trả",
            "Số đêm",
            "Tiền phòng",
            "Dịch vụ",
            "Tổng tiền",
            "Trạng thái"
        ]
    )


if "services" not in st.session_state:

    st.session_state.services = pd.DataFrame(
        [
            ["DV001", "Ăn sáng", 100000],
            ["DV002", "Cà phê", 45000],
            ["DV003", "Giặt ủi", 80000],
            ["DV004", "Minibar", 60000],
            ["DV005", "Extra Bed", 200000],
            ["DV006", "Spa & Wellness", 300000],
            ["DV007", "Đưa đón sân bay", 350000]
        ],
        columns=[
            "Mã dịch vụ",
            "Tên dịch vụ",
            "Đơn giá"
        ]
    )


# =========================================================
# CSS GIAO DIỆN
# =========================================================

css = """
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    color: #173b52;
    margin-bottom: 5px;
}

.sub-title {
    font-size: 17px;
    color: #687b88;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #173b52;
}

.room-box {
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #dfe6ea;
    background-color: rgba(255,255,255,0.94);
    text-align: center;
    margin-bottom: 15px;
}

.room-number {
    font-size: 22px;
    font-weight: 700;
    color: #173b52;
}

.room-type {
    color: #657783;
    font-size: 14px;
}

.room-price {
    font-weight: 600;
    margin-top: 5px;
}

.sidebar-title {
    font-size: 20px;
    font-weight: 700;
}

</style>
"""

st.markdown(css, unsafe_allow_html=True)


# =========================================================
# ẢNH NỀN CHÌM
# =========================================================

if image_exists(BACKGROUND_PATH):

    encoded_background = base64.b64encode(
        BACKGROUND_PATH.read_bytes()
    ).decode()

    background_css = f"""
    <style>

    .stApp {{
        background-image:
            linear-gradient(
                rgba(248, 250, 251, 0.94),
                rgba(248, 250, 251, 0.94)
            ),
            url("data:image/jpeg;base64,{encoded_background}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    </style>
    """

    st.markdown(background_css, unsafe_allow_html=True)


# =========================================================
# HÀM TẠO MÃ BOOKING
# =========================================================

def generate_booking_id():

    bookings = st.session_state.bookings

    if bookings.empty:
        return "BK0001"

    numbers = []

    for booking_id in bookings["Mã đặt phòng"]:

        try:
            number = int(str(booking_id).replace("BK", ""))
            numbers.append(number)

        except:
            pass

    if not numbers:
        return "BK0001"

    return f"BK{max(numbers) + 1:04d}"


# =========================================================
# KIỂM TRA TRÙNG LỊCH PHÒNG
# =========================================================

def is_room_booked(room_number, check_in, check_out):

    bookings = st.session_state.bookings

    if bookings.empty:
        return False

    active_bookings = bookings[
        (bookings["Phòng"] == room_number)
        &
        (
            bookings["Trạng thái"].isin(
                ["Đã đặt", "Đang ở"]
            )
        )
    ]

    for _, booking in active_bookings.iterrows():

        old_check_in = pd.to_datetime(
            booking["Ngày nhận"]
        ).date()

        old_check_out = pd.to_datetime(
            booking["Ngày trả"]
        ).date()

        if check_in < old_check_out and check_out > old_check_in:
            return True

    return False


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # LOGO IMG_LOGO1
    if image_exists(LOGO_PATH):

        st.image(
            str(LOGO_PATH),
            width=115
        )

    else:

        st.markdown("## 🏨")

    st.markdown(
        '<div class="sidebar-title">CHARM PEARL HOTEL</div>',
        unsafe_allow_html=True
    )

    st.caption("HOTEL MANAGEMENT SYSTEM")

    st.divider()

    menu = st.radio(
        "MENU QUẢN LÝ",
        [
            "🏠 Tổng quan",
            "🛏️ Quản lý phòng",
            "📅 Đặt phòng",
            "🛎️ Check-in",
            "🚪 Check-out",
            "👥 Khách hàng",
            "🍽️ Dịch vụ",
            "🧾 Hóa đơn",
            "💰 Doanh thu",
            "📊 Báo cáo"
        ]
    )

    st.divider()

    st.caption("Charm Pearl Hotel")
    st.caption("Vũng Tàu")
    st.caption("50 phòng · 5 tầng")


# =========================================================
# TRANG TỔNG QUAN
# =========================================================

if menu == "🏠 Tổng quan":

    st.markdown(
        '<div class="main-title">Charm Pearl Hotel</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Hệ thống quản lý khách sạn · Vũng Tàu</div>',
        unsafe_allow_html=True
    )

    # =====================================================
    # BANNER IMG_BANNER2
    # Đặt chính giữa
    # =====================================================

    if image_exists(BANNER_PATH):

        left, center, right = st.columns(
            [1, 2, 1]
        )

        with center:

            st.image(
                str(BANNER_PATH),
                width=600
            )

    else:

        st.warning(
            "Không tìm thấy file IMG_BANNER2.jpg"
        )

    st.divider()

    rooms = st.session_state.rooms
    bookings = st.session_state.bookings

    total_rooms = len(rooms)

    empty_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Trống"
        ]
    )

    booked_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Đã đặt"
        ]
    )

    occupied_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Đang ở"
        ]
    )

    if bookings.empty:
        revenue = 0
    else:
        revenue = bookings["Tổng tiền"].sum()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "🏨 Tổng phòng",
        total_rooms
    )

    col2.metric(
        "🟢 Phòng trống",
        empty_rooms
    )

    col3.metric(
        "🟣 Đã đặt",
        booked_rooms
    )

    col4.metric(
        "🔵 Đang ở",
        occupied_rooms
    )

    col5.metric(
        "💰 Doanh thu",
        format_money(revenue)
    )

    st.divider()

    st.markdown(
        '<div class="section-title">🛏️ Sơ đồ phòng</div>',
        unsafe_allow_html=True
    )

    floor = st.selectbox(
        "Chọn tầng",
        ["Tất cả", 1, 2, 3, 4, 5]
    )

    if floor == "Tất cả":

        display_rooms = rooms

    else:

        display_rooms = rooms[
            rooms["Tầng"] == floor
        ]

    columns = st.columns(5)

    for index, (_, room) in enumerate(
        display_rooms.iterrows()
    ):

        with columns[index % 5]:

            st.info(
                f"""
                🛏️ **Phòng {room['Phòng']}**

                {room['Loại phòng']} · Tầng {room['Tầng']}

                **{format_money(room['Giá/đêm'])} / đêm**

                {room_status_icon(room['Trạng thái'])}
                **{room['Trạng thái']}**
                """
            )


# =========================================================
# QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Quản lý phòng":

    st.title("🛏️ Quản lý phòng")

    rooms = st.session_state.rooms

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_floor = st.selectbox(
            "Tầng",
            ["Tất cả", 1, 2, 3, 4, 5]
        )

    with col2:

        selected_type = st.selectbox(
            "Loại phòng",
            ["Tất cả"] + list(ROOM_TYPES.keys())
        )

    with col3:

        selected_status = st.selectbox(
            "Trạng thái",
            ["Tất cả"] + ROOM_STATUS
        )

    filtered_rooms = rooms.copy()

    if selected_floor != "Tất cả":

        filtered_rooms = filtered_rooms[
            filtered_rooms["Tầng"] == selected_floor
        ]

    if selected_type != "Tất cả":

        filtered_rooms = filtered_rooms[
            filtered_rooms["Loại phòng"] == selected_type
        ]

    if selected_status != "Tất cả":

        filtered_rooms = filtered_rooms[
            filtered_rooms["Trạng thái"] == selected_status
        ]

    st.dataframe(
        filtered_rooms,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🔧 Cập nhật trạng thái phòng")

    with st.form("update_room"):

        room_number = st.selectbox(
            "Chọn phòng",
            rooms["Phòng"].tolist()
        )

        new_status = st.selectbox(
            "Trạng thái mới",
            ROOM_STATUS
        )

        update_button = st.form_submit_button(
            "CẬP NHẬT PHÒNG",
            use_container_width=True
        )

    if update_button:

        st.session_state.rooms.loc[
            st.session_state.rooms["Phòng"] == room_number,
            "Trạng thái"
        ] = new_status

        st.success(
            f"Phòng {room_number} đã chuyển sang: {new_status}"
        )

        st.rerun()


# =========================================================
# ĐẶT PHÒNG
# =========================================================

elif menu == "📅 Đặt phòng":

    st.title("📅 Đặt phòng")

    st.write(
        "Nhập thông tin khách và thời gian lưu trú để tạo booking."
    )

    col1, col2 = st.columns(2)

    with col1:

        check_in = st.date_input(
            "Ngày nhận phòng",
            value=date.today()
        )

    with col2:

        check_out = st.date_input(
            "Ngày trả phòng",
            value=date.today() + timedelta(days=1)
        )

    if check_out <= check_in:

        st.error(
            "Ngày trả phòng phải sau ngày nhận phòng."
        )

    else:

        nights = (
            check_out - check_in
        ).days

        room_type = st.selectbox(
            "Loại phòng",
            list(ROOM_TYPES.keys())
        )

        room_information = ROOM_TYPES[room_type]

        suitable_rooms = st.session_state.rooms[
            st.session_state.rooms["Loại phòng"] == room_type
        ]

        available_rooms = []

        for _, room in suitable_rooms.iterrows():

            if room["Trạng thái"] in [
                "Bảo trì",
                "Đang dọn"
            ]:
                continue

            if not is_room_booked(
                room["Phòng"],
                check_in,
                check_out
            ):

                available_rooms.append(
                    room["Phòng"]
                )

        if not available_rooms:

            st.error(
                "Không có phòng phù hợp trong khoảng thời gian này."
            )

        else:

            st.success(
                f"Có {len(available_rooms)} phòng có thể đặt."
            )

            room_number = st.selectbox(
                "Chọn phòng",
                available_rooms
            )

            col1, col2 = st.columns(2)

            with col1:

                guest_name = st.text_input(
                    "Họ và tên khách *"
                )

                phone = st.text_input(
                    "Số điện thoại *"
                )

            with col2:

                guest_count = st.number_input(
                    "Số khách",
                    min_value=1,
                    max_value=room_information["capacity"],
                    value=1
                )

                note = st.text_area(
                    "Ghi chú"
                )

            room_total = (
                room_information["price"]
                * nights
            )

            st.info(
                f"""
                **Phòng:** {room_number}

                **Loại:** {room_type}

                **Số đêm:** {nights}

                **Giá:** {format_money(room_information['price'])}/đêm

                **Tạm tính:** {format_money(room_total)}
                """
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

                elif is_room_booked(
                    room_number,
                    check_in,
                    check_out
                ):

                    st.error(
                        "Phòng này vừa được đặt. Vui lòng chọn phòng khác."
                    )

                else:

                    booking_id = generate_booking_id()

                    new_booking = {
                        "Mã đặt phòng": booking_id,
                        "Phòng": room_number,
                        "Tên khách": guest_name,
                        "Số điện thoại": phone,
                        "Số khách": guest_count,
                        "Ngày nhận": check_in,
                        "Ngày trả": check_out,
                        "Số đêm": nights,
                        "Tiền phòng": room_total,
                        "Dịch vụ": 0,
                        "Tổng tiền": room_total,
                        "Trạng thái": "Đã đặt"
                    }

                    st.session_state.bookings = pd.concat(
                        [
                            st.session_state.bookings,
                            pd.DataFrame([new_booking])
                        ],
                        ignore_index=True
                    )

                    st.session_state.rooms.loc[
                        st.session_state.rooms["Phòng"] == room_number,
                        "Trạng thái"
                    ] = "Đã đặt"

                    st.success(
                        f"ĐẶT PHÒNG THÀNH CÔNG — Mã booking: {booking_id}"
                    )

                    st.balloons()


# =========================================================
# CHECK-IN
# =========================================================

elif menu == "🛎️ Check-in":

    st.title("🛎️ Check-in")

    bookings = st.session_state.bookings

    waiting = bookings[
        bookings["Trạng thái"] == "Đã đặt"
    ]

    if waiting.empty:

        st.info(
            "Hiện không có booking chờ check-in."
        )

    else:

        booking_id = st.selectbox(
            "Chọn mã booking",
            waiting["Mã đặt phòng"].tolist()
        )

        selected = waiting[
            waiting["Mã đặt phòng"] == booking_id
        ].iloc[0]

        st.info(
            f"""
            **Khách:** {selected['Tên khách']}

            **Phòng:** {selected['Phòng']}

            **Ngày nhận:** {selected['Ngày nhận']}

            **Ngày trả:** {selected['Ngày trả']}

            **Số khách:** {selected['Số khách']}
            """
        )

        if st.button(
            "🛎️ XÁC NHẬN CHECK-IN",
            type="primary",
            use_container_width=True
        ):

            index = st.session_state.bookings.index[
                st.session_state.bookings["Mã đặt phòng"]
                == booking_id
            ][0]

            st.session_state.bookings.loc[
                index,
                "Trạng thái"
            ] = "Đang ở"

            st.session_state.rooms.loc[
                st.session_state.rooms["Phòng"]
                == selected["Phòng"],
                "Trạng thái"
            ] = "Đang ở"

            st.success(
                f"Check-in thành công cho phòng {selected['Phòng']}."
            )

            st.rerun()


# =========================================================
# CHECK-OUT
# =========================================================

elif menu == "🚪 Check-out":

    st.title("🚪 Check-out")

    bookings = st.session_state.bookings

    staying = bookings[
        bookings["Trạng thái"] == "Đang ở"
    ]

    if staying.empty:

        st.info(
            "Hiện không có khách đang lưu trú."
        )

    else:

        booking_id = st.selectbox(
            "Chọn booking",
            staying["Mã đặt phòng"].tolist()
        )

        selected = staying[
            staying["Mã đặt phòng"] == booking_id
        ].iloc[0]

        st.write(
            f"**Khách:** {selected['Tên khách']}"
        )

        st.write(
            f"**Phòng:** {selected['Phòng']}"
        )

        st.write(
            f"**Tiền phòng:** {format_money(selected['Tiền phòng'])}"
        )

        extra_service = st.number_input(
            "Chi phí dịch vụ phát sinh",
            min_value=0,
            value=0,
            step=50000
        )

        total = (
            int(selected["Tiền phòng"])
            + extra_service
        )

        st.metric(
            "TỔNG THANH TOÁN",
            format_money(total)
        )

        if st.button(
            "💳 THANH TOÁN & CHECK-OUT",
            type="primary",
            use_container_width=True
        ):

            index = st.session_state.bookings.index[
                st.session_state.bookings["Mã đặt phòng"]
                == booking_id
            ][0]

            st.session_state.bookings.loc[
                index,
                "Dịch vụ"
            ] = extra_service

            st.session_state.bookings.loc[
                index,
                "Tổng tiền"
            ] = total

            st.session_state.bookings.loc[
                index,
                "Trạng thái"
            ] = "Đã trả phòng"

            st.session_state.rooms.loc[
                st.session_state.rooms["Phòng"]
                == selected["Phòng"],
                "Trạng thái"
            ] = "Đang dọn"

            st.success(
                f"Đã check-out phòng {selected['Phòng']}."
            )

            st.rerun()


# =========================================================
# KHÁCH HÀNG
# =========================================================

elif menu == "👥 Khách hàng":

    st.title("👥 Khách hàng")

    bookings = st.session_state.bookings

    if bookings.empty:

        st.info(
            "Chưa có thông tin khách hàng."
        )

    else:

        search = st.text_input(
            "🔎 Tìm kiếm khách hàng"
        )

        display = bookings.copy()

        if search:

            mask = display.astype(str).apply(
                lambda column:
                column.str.lower().str.contains(
                    search.lower(),
                    na=False
                )
            ).any(axis=1)

            display = display[mask]

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        active_bookings = bookings[
            bookings["Trạng thái"] == "Đã đặt"
        ]

        if not active_bookings.empty:

            st.subheader(
                "❌ Hủy đặt phòng"
            )

            booking_id = st.selectbox(
                "Chọn booking cần hủy",
                active_bookings["Mã đặt phòng"].tolist()
            )

            if st.button(
                "HỦY BOOKING",
                use_container_width=True
            ):

                index = st.session_state.bookings.index[
                    st.session_state.bookings["Mã đặt phòng"]
                    == booking_id
                ][0]

                room_number = st.session_state.bookings.loc[
                    index,
                    "Phòng"
                ]

                st.session_state.bookings.loc[
                    index,
                    "Trạng thái"
                ] = "Đã hủy"

                st.session_state.rooms.loc[
                    st.session_state.rooms["Phòng"]
                    == room_number,
                    "Trạng thái"
                ] = "Trống"

                st.success(
                    "Booking đã được hủy."
                )

                st.rerun()


# =========================================================
# DỊCH VỤ
# =========================================================

elif menu == "🍽️ Dịch vụ":

    st.title("🍽️ Quản lý dịch vụ")

    st.dataframe(
        st.session_state.services,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "➕ Thêm dịch vụ"
    )

    with st.form("add_service"):

        col1, col2, col3 = st.columns(3)

        with col1:

            service_code = st.text_input(
                "Mã dịch vụ"
            )

        with col2:

            service_name = st.text_input(
                "Tên dịch vụ"
            )

        with col3:

            service_price = st.number_input(
                "Đơn giá",
                min_value=0,
                step=10000
            )

        submit = st.form_submit_button(
            "THÊM DỊCH VỤ",
            use_container_width=True
        )

    if submit:

        if not service_code or not service_name:

            st.error(
                "Vui lòng nhập đầy đủ thông tin."
            )

        else:

            new_service = pd.DataFrame(
                [[
                    service_code.upper(),
                    service_name,
                    service_price
                ]],
                columns=[
                    "Mã dịch vụ",
                    "Tên dịch vụ",
                    "Đơn giá"
                ]
            )

            st.session_state.services = pd.concat(
                [
                    st.session_state.services,
                    new_service
                ],
                ignore_index=True
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

    if bookings.empty:

        st.info(
            "Chưa có hóa đơn."
        )

    else:

        booking_id = st.selectbox(
            "Chọn mã booking",
            bookings["Mã đặt phòng"].tolist()
        )

        invoice = bookings[
            bookings["Mã đặt phòng"]
            == booking_id
        ].iloc[0]

        st.divider()

        st.subheader(
            "CHARM PEARL HOTEL"
        )

        st.write(
            f"**Mã hóa đơn:** {invoice['Mã đặt phòng']}"
        )

        st.write(
            f"**Khách hàng:** {invoice['Tên khách']}"
        )

        st.write(
            f"**Phòng:** {invoice['Phòng']}"
        )

        st.write(
            f"**Ngày nhận:** {invoice['Ngày nhận']}"
        )

        st.write(
            f"**Ngày trả:** {invoice['Ngày trả']}"
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "Tiền phòng"
            )

            st.write(
                "Dịch vụ"
            )

        with col2:

            st.write(
                format_money(invoice["Tiền phòng"])
            )

            st.write(
                format_money(invoice["Dịch vụ"])
            )

        st.divider()

        st.success(
            f"TỔNG THANH TOÁN: "
            f"{format_money(invoice['Tổng tiền'])}"
        )


# =========================================================
# DOANH THU
# =========================================================

elif menu == "💰 Doanh thu":

    st.title("💰 Doanh thu")

    bookings = st.session_state.bookings

    if bookings.empty:

        room_revenue = 0
        service_revenue = 0

    else:

        room_revenue = bookings[
            "Tiền phòng"
        ].sum()

        service_revenue = bookings[
            "Dịch vụ"
        ].sum()

    total_revenue = (
        room_revenue
        + service_revenue
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🏨 Doanh thu phòng",
        format_money(room_revenue)
    )

    col2.metric(
        "🍽️ Doanh thu dịch vụ",
        format_money(service_revenue)
    )

    col3.metric(
        "💰 Tổng doanh thu",
        format_money(total_revenue)
    )

    st.divider()

    chart_data = pd.DataFrame(
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
        chart_data.set_index("Khoản thu")
    )

    if not bookings.empty:

        st.subheader(
            "Danh sách giao dịch"
        )

        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# BÁO CÁO
# =========================================================

elif menu == "📊 Báo cáo":

    st.title("📊 Báo cáo khách sạn")

    rooms = st.session_state.rooms
    bookings = st.session_state.bookings

    status_count = (
        rooms["Trạng thái"]
        .value_counts()
        .reindex(
            ROOM_STATUS,
            fill_value=0
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏨 Tổng phòng",
        len(rooms)
    )

    col2.metric(
        "🟢 Phòng trống",
        int(status_count["Trống"])
    )

    col3.metric(
        "🔵 Đang ở",
        int(status_count["Đang ở"])
    )

    if bookings.empty:

        total_revenue = 0

    else:

        total_revenue = bookings[
            "Tổng tiền"
        ].sum()

    col4.metric(
        "💰 Doanh thu",
        format_money(total_revenue)
    )

    st.divider()

    st.subheader(
        "Tình trạng phòng"
    )

    st.bar_chart(
        status_count
    )

    st.divider()

    st.subheader(
        "Danh sách 50 phòng"
    )

    st.dataframe(
        rooms,
        use_container_width=True,
        hide_index=True
    )

    if not bookings.empty:

        st.divider()

        st.subheader(
            "Danh sách đặt phòng"
        )

        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Charm Pearl Hotel · Vũng Tàu · "
    "50 phòng · Hotel Management System"
)
