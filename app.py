import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date, timedelta
import base64


# =========================================================
# CẤU HÌNH
# =========================================================

st.set_page_config(
    page_title="Charm Pearl Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# ĐƯỜNG DẪN ẢNH
# =========================================================

BASE_DIR = Path(__file__).parent

LOGO_FILE = BASE_DIR / "IMG_LOGO1.jpg"
BANNER_FILE = BASE_DIR / "IMG_BANNER2.jpg"
BACKGROUND_FILE = BASE_DIR / "IMG_NENCHIM3.jpg"


# =========================================================
# CSS - CHỈ DÙNG CHO GIAO DIỆN
# Không dùng HTML DIV cho các phòng
# =========================================================

st.markdown(
    """
    <style>

    /* Nền tổng thể */

    .stApp {
        background-color: #f5f8fa;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: #073b4c;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Nút */

    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Metric */

    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    /* Container */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================

def money(value):
    """Định dạng tiền Việt Nam."""

    try:
        return f"{int(value):,} VNĐ"
    except Exception:
        return "0 VNĐ"


def image_exists(path):
    return path.exists() and path.is_file()


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
# NỀN CHÌM
# =========================================================

def apply_background():

    if not image_exists(BACKGROUND_FILE):
        return

    try:

        image_bytes = BACKGROUND_FILE.read_bytes()

        encoded = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        css = f"""
        <style>

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(245, 248, 250, 0.93),
                    rgba(245, 248, 250, 0.93)
                ),
                url("data:image/jpeg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        </style>
        """

        st.markdown(
            css,
            unsafe_allow_html=True
        )

    except Exception:
        pass


apply_background()


# =========================================================
# THÔNG TIN LOẠI PHÒNG
# =========================================================

ROOM_TYPES = {

    "Standard": {
        "price": 550000,
        "capacity": 2,
        "description": "Phòng tiêu chuẩn dành cho 1–2 khách."
    },

    "Deluxe": {
        "price": 750000,
        "capacity": 2,
        "description": "Phòng Deluxe rộng rãi, tiện nghi."
    },

    "Suite": {
        "price": 1200000,
        "capacity": 3,
        "description": "Phòng Suite cao cấp, phù hợp nghỉ dưỡng."
    },

    "Family": {
        "price": 1500000,
        "capacity": 4,
        "description": "Phòng gia đình, sức chứa tối đa 4 khách."
    }
}


ROOM_STATUSES = [
    "Trống",
    "Đã đặt",
    "Đang ở",
    "Đang dọn",
    "Bảo trì"
]


# =========================================================
# TẠO 50 PHÒNG
# =========================================================

def create_rooms():

    data = []

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

            data.append(
                {
                    "Phòng": room_number,
                    "Tầng": floor,
                    "Loại phòng": room_type,
                    "Giá/đêm": ROOM_TYPES[room_type]["price"],
                    "Sức chứa": ROOM_TYPES[room_type]["capacity"],
                    "Trạng thái": "Trống"
                }
            )

    return pd.DataFrame(data)


# =========================================================
# TẠO BẢNG BOOKING
# =========================================================

def create_bookings():

    return pd.DataFrame(
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


# =========================================================
# TẠO DỊCH VỤ
# =========================================================

def create_services():

    return pd.DataFrame(
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
# SESSION STATE
# =========================================================

if "rooms" not in st.session_state:
    st.session_state.rooms = create_rooms()

if "bookings" not in st.session_state:
    st.session_state.bookings = create_bookings()

if "services" not in st.session_state:
    st.session_state.services = create_services()


# =========================================================
# BOOKING ID
# =========================================================

def next_booking_id():

    bookings = st.session_state.bookings

    if bookings.empty:
        return "BK0001"

    numbers = []

    for value in bookings["Mã đặt phòng"]:

        try:

            number = int(
                str(value).replace("BK", "")
            )

            numbers.append(number)

        except Exception:
            continue

    next_number = max(numbers, default=0) + 1

    return f"BK{next_number:04d}"


# =========================================================
# KIỂM TRA TRÙNG LỊCH
# =========================================================

def room_has_conflict(
    room_number,
    checkin,
    checkout
):

    bookings = st.session_state.bookings

    if bookings.empty:
        return False

    active = bookings[
        (bookings["Phòng"] == room_number)
        &
        (
            bookings["Trạng thái"].isin(
                ["Đã đặt", "Đang ở"]
            )
        )
    ]

    for _, booking in active.iterrows():

        old_checkin = booking["Ngày nhận"]
        old_checkout = booking["Ngày trả"]

        if isinstance(old_checkin, str):

            old_checkin = pd.to_datetime(
                old_checkin
            ).date()

        if isinstance(old_checkout, str):

            old_checkout = pd.to_datetime(
                old_checkout
            ).date()

        if (
            checkin < old_checkout
            and checkout > old_checkin
        ):
            return True

    return False


# =========================================================
# ĐỔI TRẠNG THÁI PHÒNG
# =========================================================

def update_room_status(
    room_number,
    new_status
):

    rooms = st.session_state.rooms

    mask = rooms["Phòng"] == room_number

    if mask.any():

        st.session_state.rooms.loc[
            mask,
            "Trạng thái"
        ] = new_status


# =========================================================
# HIỂN THỊ SƠ ĐỒ PHÒNG
# =========================================================

def show_room_grid(data):

    if data.empty:

        st.info(
            "Không có phòng phù hợp với điều kiện lọc."
        )

        return

    columns = st.columns(5)

    for index, (_, room) in enumerate(
        data.iterrows()
    ):

        with columns[index % 5]:

            status = room["Trạng thái"]

            icon = status_icon(status)

            with st.container(border=True):

                st.subheader(
                    f"🛏️ {room['Phòng']}"
                )

                st.caption(
                    f"{room['Loại phòng']} · "
                    f"Tầng {room['Tầng']}"
                )

                st.write(
                    f"**{money(room['Giá/đêm'])} / đêm**"
                )

                st.write(
                    f"{icon} **{status}**"
                )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # LOGO BÊN TRÁI

    if image_exists(LOGO_FILE):

        st.image(
            str(LOGO_FILE),
            width=150
        )

    else:

        st.markdown(
            "# 🏨"
        )

    st.markdown(
        "## CHARM PEARL HOTEL"
    )

    st.caption(
        "HOTEL MANAGEMENT SYSTEM"
    )

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

    st.caption(
        "Charm Pearl Hotel"
    )

    st.caption(
        "Vũng Tàu · 50 phòng · 5 tầng"
    )


# =========================================================
# TRANG 1 - TỔNG QUAN
# =========================================================

if menu == "🏠 Tổng quan":

    st.title(
        "Charm Pearl Hotel"
    )

    st.caption(
        "Hệ thống quản lý khách sạn · Vũng Tàu"
    )


    # BANNER CHÍNH GIỮA

    if image_exists(BANNER_FILE):

        left, center, right = st.columns(
            [1, 4, 1]
        )

        with center:

            st.image(
                str(BANNER_FILE),
                use_container_width=True
            )

    else:

        st.warning(
            "Không tìm thấy IMG_BANNER2.jpg"
        )


    st.divider()


    # THỐNG KÊ

    rooms = st.session_state.rooms

    bookings = st.session_state.bookings


    total_rooms = len(rooms)

    empty_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Trống"
        ]
    )

    reserved_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Đã đặt"
        ]
    )

    occupied_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Đang ở"
        ]
    )

    cleaning_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Đang dọn"
        ]
    )


    if bookings.empty:
        revenue = 0
    else:
        revenue = bookings["Tổng tiền"].sum()


    c1, c2, c3, c4, c5 = st.columns(5)


    c1.metric(
        "🏨 Tổng phòng",
        total_rooms
    )

    c2.metric(
        "🟢 Phòng trống",
        empty_rooms
    )

    c3.metric(
        "🟣 Đã đặt",
        reserved_rooms
    )

    c4.metric(
        "🔵 Đang ở",
        occupied_rooms
    )

    c5.metric(
        "💰 Doanh thu",
        money(revenue)
    )


    st.divider()


    # SƠ ĐỒ PHÒNG

    st.header(
        "🛏️ Sơ đồ phòng"
    )

    floor_choice = st.selectbox(
        "Chọn tầng",
        [
            "Tất cả",
            1,
            2,
            3,
            4,
            5
        ],
        key="overview_floor"
    )


    if floor_choice == "Tất cả":

        room_display = rooms

    else:

        room_display = rooms[
            rooms["Tầng"] == floor_choice
        ]


    show_room_grid(
        room_display
    )


    st.caption(
        "🟢 Trống · "
        "🟣 Đã đặt · "
        "🔵 Đang ở · "
        "🟡 Đang dọn · "
        "🔴 Bảo trì"
    )


# =========================================================
# TRANG 2 - QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Quản lý phòng":

    st.title(
        "🛏️ Quản lý phòng"
    )

    st.caption(
        "Theo dõi và cập nhật trạng thái 50 phòng"
    )


    rooms = st.session_state.rooms


    c1, c2, c3 = st.columns(3)


    with c1:

        floor_filter = st.selectbox(
            "Tầng",
            [
                "Tất cả",
                1,
                2,
                3,
                4,
                5
            ],
            key="room_floor_filter"
        )


    with c2:

        type_filter = st.selectbox(
            "Loại phòng",
            [
                "Tất cả"
            ] + list(ROOM_TYPES.keys()),
            key="room_type_filter"
        )


    with c3:

        status_filter = st.selectbox(
            "Trạng thái",
            [
                "Tất cả"
            ] + ROOM_STATUSES,
            key="room_status_filter"
        )


    filtered = rooms.copy()


    if floor_filter != "Tất cả":

        filtered = filtered[
            filtered["Tầng"] == floor_filter
        ]


    if type_filter != "Tất cả":

        filtered = filtered[
            filtered["Loại phòng"]
            == type_filter
        ]


    if status_filter != "Tất cả":

        filtered = filtered[
            filtered["Trạng thái"]
            == status_filter
        ]


    show_room_grid(
        filtered
    )


    st.divider()


    st.header(
        "🔧 Cập nhật trạng thái phòng"
    )


    with st.form(
        "room_status_form"
    ):

        room_number = st.selectbox(
            "Chọn phòng",
            rooms["Phòng"].tolist()
        )

        new_status = st.selectbox(
            "Trạng thái mới",
            ROOM_STATUSES
        )

        submit_status = st.form_submit_button(
            "CẬP NHẬT PHÒNG",
            use_container_width=True
        )


    if submit_status:

        update_room_status(
            room_number,
            new_status
        )

        st.success(
            f"Phòng {room_number} đã được cập nhật thành {new_status}."
        )

        st.rerun()


# =========================================================
# TRANG 3 - ĐẶT PHÒNG
# =========================================================

elif menu == "📅 Đặt phòng":

    st.title(
        "📅 Đặt phòng"
    )

    st.caption(
        "Tìm phòng trống và tạo booking cho khách"
    )


    st.header(
        "1. Chọn thời gian lưu trú"
    )


    c1, c2 = st.columns(2)


    with c1:

        checkin = st.date_input(
            "Ngày nhận phòng",
            value=date.today(),
            min_value=date.today(),
            key="booking_checkin"
        )


    with c2:

        checkout = st.date_input(
            "Ngày trả phòng",
            value=date.today() + timedelta(days=1),
            min_value=date.today() + timedelta(days=1),
            key="booking_checkout"
        )


    if checkout <= checkin:

        st.error(
            "Ngày trả phòng phải sau ngày nhận phòng."
        )

    else:

        nights = (
            checkout - checkin
        ).days


        st.success(
            f"Thời gian lưu trú: {nights} đêm"
        )


        st.header(
            "2. Chọn loại phòng"
        )


        room_type = st.selectbox(
            "Loại phòng",
            list(ROOM_TYPES.keys()),
            key="booking_room_type"
        )


        room_info = ROOM_TYPES[
            room_type
        ]


        st.info(
            f"{room_info['description']} "
            f"Sức chứa: {room_info['capacity']} khách. "
            f"Giá: {money(room_info['price'])}/đêm."
        )


        candidate_rooms = st.session_state.rooms[
            st.session_state.rooms[
                "Loại phòng"
            ] == room_type
        ]


        available_rooms = []


        for _, room in candidate_rooms.iterrows():

            if room["Trạng thái"] in [
                "Bảo trì",
                "Đang dọn"
            ]:

                continue


            if not room_has_conflict(
                room["Phòng"],
                checkin,
                checkout
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


            selected_room = st.selectbox(
                "Chọn phòng",
                available_rooms,
                key="booking_room"
            )


            st.header(
                "3. Thông tin khách"
            )


            c1, c2 = st.columns(2)


            with c1:

                guest_name = st.text_input(
                    "Họ và tên khách *",
                    key="guest_name"
                )

                guest_phone = st.text_input(
                    "Số điện thoại *",
                    key="guest_phone"
                )


            with c2:

                guest_count = st.number_input(
                    "Số khách",
                    min_value=1,
                    max_value=room_info["capacity"],
                    value=1,
                    key="guest_count"
                )

                guest_note = st.text_area(
                    "Ghi chú",
                    key="guest_note"
                )


            room_total = (
                room_info["price"] * nights
            )


            st.header(
                "4. Xác nhận"
            )


            summary = pd.DataFrame(
                [
                    [
                        selected_room,
                        room_type,
                        nights,
                        room_info["price"],
                        room_total
                    ]
                ],
                columns=[
                    "Phòng",
                    "Loại phòng",
                    "Số đêm",
                    "Giá/đêm",
                    "Tổng tiền phòng"
                ]
            )


            summary_display = summary.copy()

            summary_display["Giá/đêm"] = (
                summary_display["Giá/đêm"]
                .apply(money)
            )

            summary_display["Tổng tiền phòng"] = (
                summary_display["Tổng tiền phòng"]
                .apply(money)
            )


            st.dataframe(
                summary_display,
                use_container_width=True,
                hide_index=True
            )


            if st.button(
                "📅 XÁC NHẬN ĐẶT PHÒNG",
                type="primary",
                use_container_width=True
            ):

                if not guest_name.strip():

                    st.error(
                        "Vui lòng nhập họ tên khách."
                    )

                elif not guest_phone.strip():

                    st.error(
                        "Vui lòng nhập số điện thoại."
                    )

                elif room_has_conflict(
                    selected_room,
                    checkin,
                    checkout
                ):

                    st.error(
                        "Phòng vừa được đặt bởi booking khác. "
                        "Vui lòng chọn phòng khác."
                    )

                else:

                    booking_id = next_booking_id()


                    new_booking = {
                        "Mã đặt phòng": booking_id,
                        "Phòng": selected_room,
                        "Tên khách": guest_name.strip(),
                        "Số điện thoại": guest_phone.strip(),
                        "Số khách": guest_count,
                        "Ngày nhận": checkin,
                        "Ngày trả": checkout,
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


                    update_room_status(
                        selected_room,
                        "Đã đặt"
                    )


                    st.success(
                        f"ĐẶT PHÒNG THÀNH CÔNG — "
                        f"Mã booking: {booking_id}"
                    )


                    st.info(
                        f"Phòng {selected_room} · "
                        f"{guest_name} · "
                        f"{nights} đêm · "
                        f"{money(room_total)}"
                    )


# =========================================================
# TRANG 4 - CHECK-IN
# =========================================================

elif menu == "🛎️ Check-in":

    st.title(
        "🛎️ Check-in"
    )

    st.caption(
        "Tiếp nhận khách đã có booking"
    )


    bookings = st.session_state.bookings


    pending = bookings[
        bookings["Trạng thái"] == "Đã đặt"
    ]


    if pending.empty:

        st.info(
            "Hiện không có booking chờ check-in."
        )

    else:

        booking_id = st.selectbox(
            "Chọn mã booking",
            pending["Mã đặt phòng"].tolist()
        )


        index = bookings.index[
            bookings["Mã đặt phòng"]
            == booking_id
        ][0]


        booking = bookings.loc[
            index
        ]


        st.subheader(
            "Thông tin khách"
        )


        c1, c2, c3 = st.columns(3)


        c1.metric(
            "Khách",
            booking["Tên khách"]
        )

        c2.metric(
            "Phòng",
            booking["Phòng"]
        )

        c3.metric(
            "Số khách",
            booking["Số khách"]
        )


        st.write(
            f"**Ngày nhận:** {booking['Ngày nhận']}"
        )

        st.write(
            f"**Ngày trả:** {booking['Ngày trả']}"
        )

        st.write(
            f"**Số điện thoại:** {booking['Số điện thoại']}"
        )


        if st.button(
            "🛎️ XÁC NHẬN CHECK-IN",
            type="primary",
            use_container_width=True
        ):

            st.session_state.bookings.loc[
                index,
                "Trạng thái"
            ] = "Đang ở"


            update_room_status(
                booking["Phòng"],
                "Đang ở"
            )


            st.success(
                f"Check-in thành công. "
                f"Phòng {booking['Phòng']} đang có khách."
            )


            st.rerun()


# =========================================================
# TRANG 5 - CHECK-OUT
# =========================================================

elif menu == "🚪 Check-out":

    st.title(
        "🚪 Check-out"
    )

    st.caption(
        "Thanh toán và kết thúc lưu trú"
    )


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


        index = bookings.index[
            bookings["Mã đặt phòng"]
            == booking_id
        ][0]


        booking = bookings.loc[
            index
        ]


        c1, c2, c3 = st.columns(3)


        c1.metric(
            "Khách",
            booking["Tên khách"]
        )

        c2.metric(
            "Phòng",
            booking["Phòng"]
        )

        c3.metric(
            "Tiền phòng",
            money(booking["Tiền phòng"])
        )


        service_fee = st.number_input(
            "Dịch vụ phát sinh",
            min_value=0,
            value=int(booking["Dịch vụ"]),
            step=50000
        )


        total = (
            int(booking["Tiền phòng"])
            + int(service_fee)
        )


        st.metric(
            "TỔNG THANH TOÁN",
            money(total)
        )


        if st.button(
            "💳 THANH TOÁN & CHECK-OUT",
            type="primary",
            use_container_width=True
        ):

            st.session_state.bookings.loc[
                index,
                "Dịch vụ"
            ] = service_fee


            st.session_state.bookings.loc[
                index,
                "Tổng tiền"
            ] = total


            st.session_state.bookings.loc[
                index,
                "Trạng thái"
            ] = "Đã trả phòng"


            update_room_status(
                booking["Phòng"],
                "Đang dọn"
            )


            st.success(
                f"Đã check-out phòng {booking['Phòng']}."
            )


            st.info(
                "Phòng đã chuyển sang trạng thái "
                "Đang dọn. Sau khi vệ sinh xong, "
                "vào Quản lý phòng và chuyển về Trống."
            )


            st.rerun()


# =========================================================
# TRANG 6 - KHÁCH HÀNG
# =========================================================

elif menu == "👥 Khách hàng":

    st.title(
        "👥 Khách hàng & Booking"
    )

    st.caption(
        "Tra cứu thông tin khách và lịch sử đặt phòng"
    )


    bookings = st.session_state.bookings


    if bookings.empty:

        st.info(
            "Chưa có booking nào."
        )

    else:

        search = st.text_input(
            "🔎 Tìm theo tên khách, số điện thoại, phòng hoặc mã booking"
        )


        display = bookings.copy()


        if search.strip():

            text = search.strip().lower()

            mask = (
                display.astype(str)
                .apply(
                    lambda col:
                    col.str.lower().str.contains(
                        text,
                        na=False
                    )
                )
                .any(axis=1)
            )

            display = display[mask]


        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        st.subheader(
            "❌ Hủy booking"
        )


        active = bookings[
            bookings["Trạng thái"] == "Đã đặt"
        ]


        if active.empty:

            st.info(
                "Không có booking có thể hủy."
            )

        else:

            cancel_id = st.selectbox(
                "Chọn booking cần hủy",
                active["Mã đặt phòng"].tolist()
            )


            if st.button(
                "HỦY BOOKING",
                use_container_width=True
            ):

                booking_index = bookings.index[
                    bookings["Mã đặt phòng"]
                    == cancel_id
                ][0]


                room_number = bookings.loc[
                    booking_index,
                    "Phòng"
                ]


                st.session_state.bookings.loc[
                    booking_index,
                    "Trạng thái"
                ] = "Đã hủy"


                update_room_status(
                    room_number,
                    "Trống"
                )


                st.success(
                    f"Đã hủy booking {cancel_id}."
                )


                st.rerun()


# =========================================================
# TRANG 7 - DỊCH VỤ
# =========================================================

elif menu == "🍽️ Dịch vụ":

    st.title(
        "🍽️ Dịch vụ khách sạn"
    )

    st.caption(
        "Danh mục dịch vụ cung cấp cho khách"
    )


    services = st.session_state.services.copy()


    service_display = services.copy()


    service_display["Đơn giá"] = (
        service_display["Đơn giá"]
        .apply(money)
    )


    st.dataframe(
        service_display,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    st.subheader(
        "➕ Thêm dịch vụ"
    )


    with st.form(
        "new_service"
    ):

        c1, c2, c3 = st.columns(3)


        with c1:

            service_code = st.text_input(
                "Mã dịch vụ"
            )


        with c2:

            service_name = st.text_input(
                "Tên dịch vụ"
            )


        with c3:

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

        if (
            not service_code.strip()
            or not service_name.strip()
        ):

            st.error(
                "Vui lòng nhập đầy đủ thông tin."
            )

        else:

            duplicate = (
                st.session_state.services[
                    "Mã dịch vụ"
                ]
                .astype(str)
                .str.upper()
                .eq(service_code.strip().upper())
                .any()
            )


            if duplicate:

                st.error(
                    "Mã dịch vụ đã tồn tại."
                )

            else:

                new_service = pd.DataFrame(
                    [
                        {
                            "Mã dịch vụ":
                                service_code.strip().upper(),

                            "Tên dịch vụ":
                                service_name.strip(),

                            "Đơn giá":
                                service_price
                        }
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
# TRANG 8 - HÓA ĐƠN
# =========================================================

elif menu == "🧾 Hóa đơn":

    st.title(
        "🧾 Hóa đơn"
    )

    st.caption(
        "Tra cứu và xem chi tiết thanh toán"
    )


    bookings = st.session_state.bookings


    if bookings.empty:

        st.info(
            "Chưa có booking."
        )

    else:

        booking_id = st.selectbox(
            "Chọn mã booking",
            bookings["Mã đặt phòng"].tolist()
        )


        booking = bookings[
            bookings["Mã đặt phòng"]
            == booking_id
        ].iloc[0]


        st.subheader(
            "CHARM PEARL HOTEL"
        )

        st.caption(
            "Vũng Tàu"
        )


        st.divider()


        c1, c2 = st.columns(2)


        with c1:

            st.write(
                f"**Mã booking:** {booking['Mã đặt phòng']}"
            )

            st.write(
                f"**Khách hàng:** {booking['Tên khách']}"
            )

            st.write(
                f"**Số điện thoại:** {booking['Số điện thoại']}"
            )

            st.write(
                f"**Phòng:** {booking['Phòng']}"
            )


        with c2:

            st.write(
                f"**Ngày nhận:** {booking['Ngày nhận']}"
            )

            st.write(
                f"**Ngày trả:** {booking['Ngày trả']}"
            )

            st.write(
                f"**Số đêm:** {booking['Số đêm']}"
            )

            st.write(
                f"**Trạng thái:** {booking['Trạng thái']}"
            )


        st.divider()


        invoice = pd.DataFrame(
            [
                [
                    "Tiền phòng",
                    booking["Tiền phòng"]
                ],
                [
                    "Dịch vụ",
                    booking["Dịch vụ"]
                ],
                [
                    "Tổng cộng",
                    booking["Tổng tiền"]
                ]
            ],
            columns=[
                "Khoản thu",
                "Số tiền"
            ]
        )


        invoice_display = invoice.copy()


        invoice_display["Số tiền"] = (
            invoice_display["Số tiền"]
            .apply(money)
        )


        st.table(
            invoice_display
        )


        st.success(
            f"TỔNG THANH TOÁN: {money(booking['Tổng tiền'])}"
        )


# =========================================================
# TRANG 9 - DOANH THU
# =========================================================

elif menu == "💰 Doanh thu":

    st.title(
        "💰 Doanh thu"
    )

    st.caption(
        "Tổng hợp doanh thu từ phòng và dịch vụ"
    )


    bookings = st.session_state.bookings


    if bookings.empty:

        room_revenue = 0
        service_revenue = 0
        total_revenue = 0

    else:

        room_revenue = bookings[
            "Tiền phòng"
        ].sum()

        service_revenue = bookings[
            "Dịch vụ"
        ].sum()

        total_revenue = bookings[
            "Tổng tiền"
        ].sum()


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "🏨 Doanh thu phòng",
        money(room_revenue)
    )

    c2.metric(
        "🍽️ Doanh thu dịch vụ",
        money(service_revenue)
    )

    c3.metric(
        "💰 Tổng doanh thu",
        money(total_revenue)
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


    st.subheader(
        "📊 Biểu đồ doanh thu"
    )


    st.bar_chart(
        chart_data.set_index(
            "Khoản thu"
        )
    )


    st.subheader(
        "Danh sách giao dịch"
    )


    if bookings.empty:

        st.info(
            "Chưa có dữ liệu."
        )

    else:

        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# TRANG 10 - BÁO CÁO
# =========================================================

elif menu == "📊 Báo cáo":

    st.title(
        "📊 Báo cáo vận hành"
    )

    st.caption(
        "Tình hình hoạt động của Charm Pearl Hotel"
    )


    rooms = st.session_state.rooms

    bookings = st.session_state.bookings


    total_rooms = len(rooms)


    empty_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Trống"
        ]
    )


    reserved_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Đã đặt"
        ]
    )


    occupied_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Đang ở"
        ]
    )


    cleaning_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Đang dọn"
        ]
    )


    maintenance_rooms = len(
        rooms[
            rooms["Trạng thái"] == "Bảo trì"
        ]
    )


    if total_rooms > 0:

        occupancy = (
            occupied_rooms / total_rooms
        )

    else:

        occupancy = 0


    if bookings.empty:

        total_revenue = 0

    else:

        total_revenue = bookings[
            "Tổng tiền"
        ].sum()


    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Tổng phòng",
        total_rooms
    )

    c2.metric(
        "Phòng trống",
        empty_rooms
    )

    c3.metric(
        "Đang ở",
        occupied_rooms
    )

    c4.metric(
        "Doanh thu",
        money(total_revenue)
    )


    st.subheader(
        "Công suất phòng"
    )


    st.progress(
        occupancy
    )


    st.write(
        f"Công suất hiện tại: **{occupancy:.0%}**"
    )


    st.divider()


    st.subheader(
        "📊 Phân bố trạng thái phòng"
    )


    status_data = pd.DataFrame(
        {
            "Trạng thái": [
                "Trống",
                "Đã đặt",
                "Đang ở",
                "Đang dọn",
                "Bảo trì"
            ],

            "Số phòng": [
                empty_rooms,
                reserved_rooms,
                occupied_rooms,
                cleaning_rooms,
                maintenance_rooms
            ]
        }
    )


    st.bar_chart(
        status_data.set_index(
            "Trạng thái"
        )
    )


    st.subheader(
        "🛏️ Danh sách 50 phòng"
    )


    st.dataframe(
        rooms,
        use_container_width=True,
        hide_index=True
    )


    st.subheader(
        "📅 Toàn bộ booking"
    )


    if bookings.empty:

        st.info(
            "Chưa có booking nào."
        )

    else:

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
    "Hotel Management System · 50 rooms"
)
