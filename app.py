import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date, timedelta
import base64


# =========================================================
# 1. CẤU HÌNH APP
# =========================================================

st.set_page_config(
    page_title="Charm Pearl Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. ĐƯỜNG DẪN HÌNH ẢNH
# =========================================================

BASE_DIR = Path(__file__).parent

LOGO_PATH = BASE_DIR / "IMG_LOGO1.jpg"
BANNER_PATH = BASE_DIR / "IMG_BANNER2.jpg"
BACKGROUND_PATH = BASE_DIR / "IMG_NENCHIM3.jpg"


# =========================================================
# 3. HÀM TIỀN
# =========================================================

def money(value):
    try:
        return f"{int(value):,} VNĐ"
    except:
        return "0 VNĐ"


# =========================================================
# 4. NỀN APP
# =========================================================

def get_background():

    if not BACKGROUND_PATH.exists():
        return ""

    try:

        image_data = base64.b64encode(
            BACKGROUND_PATH.read_bytes()
        ).decode()

        return f"""
        <style>

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(248, 250, 252, 0.94),
                    rgba(248, 250, 252, 0.94)
                ),
                url("data:image/jpeg;base64,{image_data}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        </style>
        """

    except:
        return ""


st.markdown(
    get_background(),
    unsafe_allow_html=True
)


# =========================================================
# 5. CSS GIAO DIỆN
# =========================================================

st.markdown(
    """
    <style>

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #063650 0%,
                #0a5971 100%
            );
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }


    /* TIÊU ĐỀ */

    .hotel-title {
        font-size: 34px;
        font-weight: 800;
        color: #07324f;
        margin-bottom: 0px;
    }

    .hotel-subtitle {
        font-size: 14px;
        color: #71808c;
        margin-bottom: 20px;
    }


    /* HERO */

    .hero-box {
        background:
            linear-gradient(
                135deg,
                rgba(4, 43, 66, 0.97),
                rgba(8, 99, 122, 0.90)
            );

        border-radius: 20px;

        padding: 28px 35px;

        margin-top: 20px;
        margin-bottom: 25px;

        color: white;

        box-shadow:
            0 10px 30px
            rgba(0, 0, 0, 0.12);
    }


    /* ROOM CARD */

    .room-card {
        background: rgba(255,255,255,0.97);

        border:
            1px solid
            #dce6eb;

        border-radius: 15px;

        padding: 15px 8px;

        text-align: center;

        min-height: 135px;

        margin-bottom: 15px;

        box-shadow:
            0 4px 12px
            rgba(0,0,0,0.05);
    }


    .room-number {
        font-size: 23px;
        font-weight: 800;
        color: #07324f;
    }


    .room-type {
        font-size: 12px;
        color: #71808c;
        margin-top: 4px;
    }


    .room-price {
        font-size: 13px;
        font-weight: 700;
        color: #08728f;
        margin-top: 6px;
    }


    .room-status {
        font-size: 12px;
        font-weight: 700;
        margin-top: 8px;
    }


    /* INFO BOX */

    .info-box {
        background: rgba(255,255,255,0.97);

        border:
            1px solid
            #e0e8ed;

        border-radius: 15px;

        padding: 20px;

        margin: 10px 0 20px 0;

        box-shadow:
            0 4px 15px
            rgba(0,0,0,0.04);
    }


    /* FOOTER */

    .footer {
        text-align: center;

        color: #71808c;

        font-size: 12px;

        padding:
            30px 0 15px 0;
    }


    /* BUTTON */

    .stButton > button {
        border-radius: 9px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 6. LOẠI PHÒNG
# =========================================================

ROOM_TYPES = {

    "Standard": {
        "price": 550000,
        "capacity": 2,
        "description":
            "Phòng tiêu chuẩn, phù hợp 1–2 khách."
    },

    "Deluxe": {
        "price": 750000,
        "capacity": 2,
        "description":
            "Phòng cao cấp, không gian rộng."
    },

    "Suite": {
        "price": 1200000,
        "capacity": 3,
        "description":
            "Phòng Suite rộng, phù hợp nghỉ dưỡng."
    },

    "Family": {
        "price": 1500000,
        "capacity": 4,
        "description":
            "Phòng gia đình, tối đa 4 khách."
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
# 7. TẠO 50 PHÒNG
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

            rooms.append([
                room_number,
                floor,
                room_type,
                ROOM_TYPES[room_type]["price"],
                ROOM_TYPES[room_type]["capacity"],
                "Trống"
            ])

    return pd.DataFrame(
        rooms,
        columns=[
            "Phòng",
            "Tầng",
            "Loại phòng",
            "Giá/đêm",
            "Sức chứa",
            "Trạng thái"
        ]
    )


# =========================================================
# 8. TẠO BOOKING
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
# 9. DỊCH VỤ
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
            ["DV007", "Đưa đón sân bay", 350000],
        ],
        columns=[
            "Mã DV",
            "Tên dịch vụ",
            "Đơn giá"
        ]
    )


# =========================================================
# 10. SESSION STATE
# =========================================================

if "rooms" not in st.session_state:

    st.session_state.rooms = create_rooms()


if "bookings" not in st.session_state:

    st.session_state.bookings = create_bookings()


if "services" not in st.session_state:

    st.session_state.services = create_services()


# =========================================================
# 11. HÀM BOOKING
# =========================================================

def next_booking_id():

    bookings = st.session_state.bookings

    if bookings.empty:

        return "BK0001"

    numbers = []

    for code in bookings["Mã đặt phòng"]:

        try:

            numbers.append(
                int(str(code).replace("BK", ""))
            )

        except:

            pass

    next_number = max(
        numbers,
        default=0
    ) + 1

    return f"BK{next_number:04d}"


# =========================================================
# 12. KIỂM TRA TRÙNG PHÒNG
# =========================================================

def room_has_conflict(
    room_number,
    checkin,
    checkout
):

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

        old_checkin = booking["Ngày nhận"]
        old_checkout = booking["Ngày trả"]

        if isinstance(
            old_checkin,
            str
        ):

            old_checkin = pd.to_datetime(
                old_checkin
            ).date()

        if isinstance(
            old_checkout,
            str
        ):

            old_checkout = pd.to_datetime(
                old_checkout
            ).date()

        if (
            checkin < old_checkout
            and
            checkout > old_checkin
        ):

            return True

    return False


# =========================================================
# 13. ĐỔI TRẠNG THÁI PHÒNG
# =========================================================

def set_room_status(
    room_number,
    status
):

    indexes = st.session_state.rooms.index[
        st.session_state.rooms["Phòng"]
        == room_number
    ]

    if len(indexes) > 0:

        st.session_state.rooms.loc[
            indexes[0],
            "Trạng thái"
        ] = status


# =========================================================
# 14. ICON TRẠNG THÁI
# =========================================================

def status_icon(status):

    icons = {

        "Trống": "🟢",

        "Đã đặt": "🟣",

        "Đang ở": "🔵",

        "Đang dọn": "🟡",

        "Bảo trì": "🔴"

    }

    return icons.get(
        status,
        "⚪"
    )


# =========================================================
# 15. HIỂN THỊ PHÒNG
# =========================================================

def show_room_grid(data):

    columns = st.columns(5)

    for i, (_, room) in enumerate(
        data.iterrows()
    ):

        with columns[i % 5]:

            st.markdown(
                f"""
                <div class="room-card">

                    <div class="room-number">
                        {room["Phòng"]}
                    </div>

                    <div class="room-type">
                        {room["Loại phòng"]}
                        · Tầng {room["Tầng"]}
                    </div>

                    <div class="room-price">
                        {money(room["Giá/đêm"])}
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
# 16. SIDEBAR
# =========================================================

with st.sidebar:

    # LOGO Ở BÊN TRÁI

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=150
        )

    st.markdown(
        "## CHARM PEARL"
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
        "Charm Pearl Hotel · Vũng Tàu"
    )

    st.caption(
        "50 phòng · 5 tầng"
    )


# =========================================================
# 17. TRANG TỔNG QUAN
# =========================================================

if menu == "🏠 Tổng quan":

    st.markdown(
        '<div class="hotel-title">Charm Pearl Hotel</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hotel-subtitle">Hệ thống quản lý khách sạn · Vũng Tàu</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # BANNER CHÍNH GIỮA
    # =====================================================

    if BANNER_PATH.exists():

        left_space, banner_col, right_space = st.columns(
            [1, 4, 1]
        )

        with banner_col:

            st.image(
                str(BANNER_PATH),
                use_container_width=True
            )


    # =====================================================
    # HERO
    # =====================================================

    st.markdown(
        """
        <div class="hero-box">

            <h1 style="
                color:white;
                margin:0;
                font-size:36px;
            ">
                Charm Pearl Hotel
            </h1>

            <p style="
                color:#eaf8fb;
                font-size:16px;
                font-weight:700;
            ">
                HỆ THỐNG QUẢN LÝ KHÁCH SẠN
            </p>

            <p style="
                color:white;
                font-size:14px;
            ">
                Quản lý phòng · Đặt phòng ·
                Check-in · Check-out ·
                Dịch vụ · Hóa đơn · Doanh thu
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # THỐNG KÊ
    # =====================================================

    rooms = st.session_state.rooms

    bookings = st.session_state.bookings

    total_rooms = len(rooms)

    empty_rooms = len(
        rooms[
            rooms["Trạng thái"]
            == "Trống"
        ]
    )

    reserved_rooms = len(
        rooms[
            rooms["Trạng thái"]
            == "Đã đặt"
        ]
    )

    occupied_rooms = len(
        rooms[
            rooms["Trạng thái"]
            == "Đang ở"
        ]
    )

    total_revenue = (
        bookings["Tổng tiền"].sum()
        if not bookings.empty
        else 0
    )


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
        money(total_revenue)
    )


    # =====================================================
    # SƠ ĐỒ PHÒNG
    # =====================================================

    st.subheader(
        "🛏️ Sơ đồ phòng"
    )

    floor = st.selectbox(
        "Chọn tầng",
        [
            "Tất cả",
            1,
            2,
            3,
            4,
            5
        ]
    )

    if floor == "Tất cả":

        display_rooms = rooms

    else:

        display_rooms = rooms[
            rooms["Tầng"]
            == floor
        ]

    show_room_grid(
        display_rooms
    )

    st.caption(
        "🟢 Trống   "
        "🟣 Đã đặt   "
        "🔵 Đang ở   "
        "🟡 Đang dọn   "
        "🔴 Bảo trì"
    )


# =========================================================
# 18. QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Quản lý phòng":

    st.markdown(
        '<div class="hotel-title">🛏️ Quản lý phòng</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hotel-subtitle">Theo dõi và cập nhật trạng thái 50 phòng</div>',
        unsafe_allow_html=True
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
            ]
        )

    with c2:

        type_filter = st.selectbox(
            "Loại phòng",
            [
                "Tất cả"
            ]
            +
            list(ROOM_TYPES.keys())
        )

    with c3:

        status_filter = st.selectbox(
            "Trạng thái",
            [
                "Tất cả"
            ]
            +
            ROOM_STATUSES
        )


    filtered = rooms.copy()


    if floor_filter != "Tất cả":

        filtered = filtered[
            filtered["Tầng"]
            == floor_filter
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

    st.subheader(
        "🔧 Cập nhật trạng thái phòng"
    )


    with st.form(
        "update_room"
    ):

        c1, c2 = st.columns(2)

        with c1:

            room_number = st.selectbox(
                "Phòng",
                rooms["Phòng"].tolist()
            )

        with c2:

            new_status = st.selectbox(
                "Trạng thái mới",
                ROOM_STATUSES
            )

        submit = st.form_submit_button(
            "CẬP NHẬT",
            use_container_width=True
        )


    if submit:

        set_room_status(
            room_number,
            new_status
        )

        st.success(
            f"Phòng {room_number} đã chuyển sang {new_status}."
        )

        st.rerun()


# =========================================================
# 19. ĐẶT PHÒNG
# =========================================================

elif menu == "📅 Đặt phòng":

    st.markdown(
        '<div class="hotel-title">📅 Đặt phòng</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hotel-subtitle">Tạo booking và kiểm tra phòng trống theo ngày</div>',
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)


    with c1:

        checkin = st.date_input(
            "Ngày nhận phòng",
            value=date.today(),
            min_value=date.today()
        )


    with c2:

        checkout = st.date_input(
            "Ngày trả phòng",
            value=date.today()
            +
            timedelta(days=1),
            min_value=date.today()
            +
            timedelta(days=1)
        )


    if checkout <= checkin:

        st.error(
            "Ngày trả phòng phải sau ngày nhận phòng."
        )

    else:

        nights = (
            checkout - checkin
        ).days


        room_type = st.selectbox(
            "Loại phòng",
            list(
                ROOM_TYPES.keys()
            )
        )


        info = ROOM_TYPES[
            room_type
        ]


        st.info(
            f"{info['description']} "
            f"· Sức chứa: {info['capacity']} khách "
            f"· Giá: {money(info['price'])}/đêm"
        )


        candidate_rooms = (
            st.session_state.rooms[
                st.session_state.rooms[
                    "Loại phòng"
                ]
                == room_type
            ]
        )


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

            st.warning(
                "Không có phòng phù hợp "
                "trong khoảng thời gian này."
            )

        else:

            selected_room = st.selectbox(
                "Phòng có thể đặt",
                available_rooms
            )


            st.success(
                f"Phòng {selected_room} có thể đặt."
            )


            st.subheader(
                "👤 Thông tin khách"
            )


            c1, c2 = st.columns(2)


            with c1:

                guest_name = st.text_input(
                    "Họ và tên *"
                )

                phone = st.text_input(
                    "Số điện thoại *"
                )


            with c2:

                guest_count = st.number_input(
                    "Số khách",
                    min_value=1,
                    max_value=info["capacity"],
                    value=1
                )

                note = st.text_area(
                    "Ghi chú"
                )


            room_total = (
                info["price"]
                *
                nights
            )


            st.markdown(
                f"""
                <div class="info-box">

                    <b>Phòng:</b>
                    {selected_room}

                    <br><br>

                    <b>Loại phòng:</b>
                    {room_type}

                    <br><br>

                    <b>Số đêm:</b>
                    {nights}

                    <br><br>

                    <b>Giá:</b>
                    {money(info["price"])}
                    /đêm

                    <hr>

                    <h3>
                        Tổng tiền:
                        {money(room_total)}
                    </h3>

                </div>
                """,
                unsafe_allow_html=True
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

                elif not phone.strip():

                    st.error(
                        "Vui lòng nhập số điện thoại."
                    )

                elif room_has_conflict(
                    selected_room,
                    checkin,
                    checkout
                ):

                    st.error(
                        "Phòng đã phát sinh booking "
                        "trùng lịch."
                    )

                else:

                    booking_id = next_booking_id()


                    new_booking = pd.DataFrame(
                        [[
                            booking_id,
                            selected_room,
                            guest_name.strip(),
                            phone.strip(),
                            guest_count,
                            checkin,
                            checkout,
                            nights,
                            room_total,
                            0,
                            room_total,
                            "Đã đặt"
                        ]],
                        columns=
                        st.session_state.bookings.columns
                    )


                    st.session_state.bookings = pd.concat(
                        [
                            st.session_state.bookings,
                            new_booking
                        ],
                        ignore_index=True
                    )


                    set_room_status(
                        selected_room,
                        "Đã đặt"
                    )


                    st.success(
                        f"Đặt phòng thành công! "
                        f"Mã booking: {booking_id}"
                    )


# =========================================================
# 20. CHECK-IN
# =========================================================

elif menu == "🛎️ Check-in":

    st.markdown(
        '<div class="hotel-title">🛎️ Check-in</div>',
        unsafe_allow_html=True
    )

    bookings = st.session_state.bookings


    pending = bookings[
        bookings["Trạng thái"]
        == "Đã đặt"
    ]


    if pending.empty:

        st.info(
            "Không có booking chờ check-in."
        )

    else:

        booking_id = st.selectbox(
            "Mã đặt phòng",
            pending[
                "Mã đặt phòng"
            ].tolist()
        )


        index = pending.index[
            pending[
                "Mã đặt phòng"
            ]
            == booking_id
        ][0]


        booking = bookings.loc[
            index
        ]


        st.markdown(
            f"""
            <div class="info-box">

                <b>Khách:</b>
                {booking["Tên khách"]}

                <br><br>

                <b>Số điện thoại:</b>
                {booking["Số điện thoại"]}

                <br><br>

                <b>Phòng:</b>
                {booking["Phòng"]}

                <br><br>

                <b>Ngày nhận:</b>
                {booking["Ngày nhận"]}

                <br><br>

                <b>Ngày trả:</b>
                {booking["Ngày trả"]}

            </div>
            """,
            unsafe_allow_html=True
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


            set_room_status(
                booking["Phòng"],
                "Đang ở"
            )


            st.success(
                f"Khách {booking['Tên khách']} "
                f"đã check-in phòng {booking['Phòng']}."
            )


            st.rerun()


# =========================================================
# 21. CHECK-OUT
# =========================================================

elif menu == "🚪 Check-out":

    st.markdown(
        '<div class="hotel-title">🚪 Check-out</div>',
        unsafe_allow_html=True
    )


    bookings = st.session_state.bookings


    staying = bookings[
        bookings["Trạng thái"]
        == "Đang ở"
    ]


    if staying.empty:

        st.info(
            "Không có khách đang lưu trú."
        )

    else:

        booking_id = st.selectbox(
            "Booking",
            staying[
                "Mã đặt phòng"
            ].tolist()
        )


        index = staying.index[
            staying[
                "Mã đặt phòng"
            ]
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
            money(
                booking["Tiền phòng"]
            )
        )


        service_fee = st.number_input(
            "Dịch vụ phát sinh",
            min_value=0,
            value=int(
                booking["Dịch vụ"]
            ),
            step=50000
        )


        total = (
            int(
                booking["Tiền phòng"]
            )
            +
            service_fee
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


            set_room_status(
                booking["Phòng"],
                "Đang dọn"
            )


            st.success(
                f"Đã check-out phòng "
                f"{booking['Phòng']}."
            )


            st.rerun()


# =========================================================
# 22. KHÁCH HÀNG
# =========================================================

elif menu == "👥 Khách hàng":

    st.markdown(
        '<div class="hotel-title">👥 Khách hàng & Booking</div>',
        unsafe_allow_html=True
    )


    bookings = (
        st.session_state.bookings.copy()
    )


    if bookings.empty:

        st.info(
            "Chưa có khách hàng."
        )

    else:

        search = st.text_input(
            "🔎 Tìm tên khách, SĐT, phòng hoặc mã booking"
        )


        if search:

            mask = (
                bookings
                .astype(str)
                .apply(
                    lambda column:
                    column.str.contains(
                        search,
                        case=False,
                        na=False
                    )
                )
                .any(axis=1)
            )


            bookings = bookings[
                mask
            ]


        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )


        st.divider()

        st.subheader(
            "❌ Hủy booking"
        )


        active = bookings[
            bookings["Trạng thái"]
            == "Đã đặt"
        ]


        if not active.empty:

            cancel_id = st.selectbox(
                "Chọn booking",
                active[
                    "Mã đặt phòng"
                ].tolist()
            )


            if st.button(
                "HỦY BOOKING",
                use_container_width=True
            ):

                original_index = (
                    st.session_state
                    .bookings
                    .index[
                        st.session_state
                        .bookings[
                            "Mã đặt phòng"
                        ]
                        == cancel_id
                    ][0]
                )


                room_number = (
                    st.session_state
                    .bookings.loc[
                        original_index,
                        "Phòng"
                    ]
                )


                st.session_state.bookings.loc[
                    original_index,
                    "Trạng thái"
                ] = "Đã hủy"


                set_room_status(
                    room_number,
                    "Trống"
                )


                st.success(
                    f"Đã hủy booking {cancel_id}."
                )


                st.rerun()


# =========================================================
# 23. DỊCH VỤ
# =========================================================

elif menu == "🍽️ Dịch vụ":

    st.markdown(
        '<div class="hotel-title">🍽️ Dịch vụ khách sạn</div>',
        unsafe_allow_html=True
    )


    services = (
        st.session_state.services
    )


    display_services = (
        services.copy()
    )


    display_services[
        "Đơn giá"
    ] = (
        display_services[
            "Đơn giá"
        ]
        .apply(money)
    )


    st.dataframe(
        display_services,
        use_container_width=True,
        hide_index=True
    )


    st.divider()

    st.subheader(
        "➕ Thêm dịch vụ"
    )


    with st.form(
        "add_service"
    ):

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

        if not code.strip() or not name.strip():

            st.error(
                "Vui lòng nhập đầy đủ thông tin."
            )

        else:

            new_service = pd.DataFrame(
                [[
                    code.upper(),
                    name.strip(),
                    price
                ]],
                columns=services.columns
            )


            st.session_state.services = pd.concat(
                [
                    services,
                    new_service
                ],
                ignore_index=True
            )


            st.success(
                "Đã thêm dịch vụ."
            )


            st.rerun()


# =========================================================
# 24. HÓA ĐƠN
# =========================================================

elif menu == "🧾 Hóa đơn":

    st.markdown(
        '<div class="hotel-title">🧾 Hóa đơn</div>',
        unsafe_allow_html=True
    )


    bookings = (
        st.session_state.bookings
    )


    if bookings.empty:

        st.info(
            "Chưa có booking để lập hóa đơn."
        )

    else:

        booking_id = st.selectbox(
            "Chọn booking",
            bookings[
                "Mã đặt phòng"
            ].tolist()
        )


        booking = bookings[
            bookings[
                "Mã đặt phòng"
            ]
            == booking_id
        ].iloc[0]


        st.markdown(
            f"""
            <div class="info-box">

                <div style="text-align:center;">

                    <h2>
                        CHARM PEARL HOTEL
                    </h2>

                    <p>
                        VŨNG TÀU
                    </p>

                    <h3>
                        PHIẾU THANH TOÁN
                    </h3>

                </div>

                <hr>

                <b>Mã booking:</b>
                {booking["Mã đặt phòng"]}

                <br><br>

                <b>Khách hàng:</b>
                {booking["Tên khách"]}

                <br><br>

                <b>Số điện thoại:</b>
                {booking["Số điện thoại"]}

                <br><br>

                <b>Phòng:</b>
                {booking["Phòng"]}

                <br><br>

                <b>Ngày nhận:</b>
                {booking["Ngày nhận"]}

                <br><br>

                <b>Ngày trả:</b>
                {booking["Ngày trả"]}

                <br><br>

                <b>Số đêm:</b>
                {booking["Số đêm"]}

                <hr>

                <b>Tiền phòng:</b>
                {money(booking["Tiền phòng"])}

                <br><br>

                <b>Dịch vụ:</b>
                {money(booking["Dịch vụ"])}

                <hr>

                <h2>
                    TỔNG:
                    {money(booking["Tổng tiền"])}
                </h2>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 25. DOANH THU
# =========================================================

elif menu == "💰 Doanh thu":

    st.markdown(
        '<div class="hotel-title">💰 Doanh thu</div>',
        unsafe_allow_html=True
    )


    bookings = (
        st.session_state.bookings
    )


    if bookings.empty:

        room_revenue = 0
        service_revenue = 0
        total_revenue = 0

    else:

        room_revenue = (
            bookings[
                "Tiền phòng"
            ].sum()
        )

        service_revenue = (
            bookings[
                "Dịch vụ"
            ].sum()
        )

        total_revenue = (
            bookings[
                "Tổng tiền"
            ].sum()
        )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "🏨 Tiền phòng",
        money(room_revenue)
    )


    c2.metric(
        "🍽️ Dịch vụ",
        money(service_revenue)
    )


    c3.metric(
        "💰 Tổng doanh thu",
        money(total_revenue)
    )


    chart = pd.DataFrame(
        {
            "Khoản thu":
                [
                    "Tiền phòng",
                    "Dịch vụ"
                ],

            "Doanh thu":
                [
                    room_revenue,
                    service_revenue
                ]
        }
    )


    st.subheader(
        "📊 Biểu đồ doanh thu"
    )


    st.bar_chart(
        chart.set_index(
            "Khoản thu"
        )
    )


    if not bookings.empty:

        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 26. BÁO CÁO
# =========================================================

elif menu == "📊 Báo cáo":

    st.markdown(
        '<div class="hotel-title">📊 Báo cáo vận hành</div>',
        unsafe_allow_html=True
    )


    rooms = st.session_state.rooms

    bookings = (
        st.session_state.bookings
    )


    total = len(
        rooms
    )


    empty = len(
        rooms[
            rooms["Trạng thái"]
            == "Trống"
        ]
    )


    reserved = len(
        rooms[
            rooms["Trạng thái"]
            == "Đã đặt"
        ]
    )


    occupied = len(
        rooms[
            rooms["Trạng thái"]
            == "Đang ở"
        ]
    )


    occupancy = (
        occupied / total
        if total > 0
        else 0
    )


    revenue = (
        bookings[
            "Tổng tiền"
        ].sum()
        if not bookings.empty
        else 0
    )


    c1, c2, c3, c4, c5 = st.columns(5)


    c1.metric(
        "Tổng phòng",
        total
    )


    c2.metric(
        "Phòng trống",
        empty
    )


    c3.metric(
        "Đã đặt",
        reserved
    )


    c4.metric(
        "Đang ở",
        occupied
    )


    c5.metric(
        "Doanh thu",
        money(revenue)
    )


    st.write(
        f"**Công suất phòng: {occupancy:.0%}**"
    )


    st.progress(
        occupancy
    )


    st.subheader(
        "📊 Trạng thái phòng"
    )


    st.bar_chart(
        rooms[
            "Trạng thái"
        ].value_counts()
    )


    st.subheader(
        "🛏️ Danh sách phòng"
    )


    st.dataframe(
        rooms,
        use_container_width=True,
        hide_index=True
    )


    st.subheader(
        "📅 Danh sách booking"
    )


    if bookings.empty:

        st.info(
            "Chưa có booking."
        )

    else:

        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 27. FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        CHARM PEARL HOTEL · VŨNG TÀU

        <br>

        Hotel Management System · 50 rooms

    </div>
    """,
    unsafe_allow_html=True
)
