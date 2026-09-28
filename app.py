import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date, timedelta
import base64


# =========================================================
# 1. CẤU HÌNH ỨNG DỤNG
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
# 3. HÀM XỬ LÝ ẢNH NỀN
# =========================================================

def image_to_base64(path):

    if not path.exists():
        return None

    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(
                image_file.read()
            ).decode()

    except Exception:
        return None


background_image = image_to_base64(
    BACKGROUND_PATH
)


# =========================================================
# 4. CSS GIAO DIỆN
# =========================================================

if background_image:

    background_css = f"""
    .stApp {{
        background-image:
            linear-gradient(
                rgba(248, 250, 252, 0.94),
                rgba(248, 250, 252, 0.94)
            ),
            url("data:image/jpeg;base64,{background_image}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    """

else:

    background_css = """
    .stApp {
        background: #f4f7f9;
    }
    """


st.markdown(
    f"""
    <style>

    {background_css}

    /* ================= SIDEBAR ================= */

    [data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                #07324f 0%,
                #0b4968 100%
            );
    }}

    [data-testid="stSidebar"] * {{
        color: white !important;
    }}

    /* ================= TITLE ================= */

    .page-title {{
        color: #07324f;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 2px;
    }}

    .page-subtitle {{
        color: #71808c;
        font-size: 14px;
        margin-bottom: 20px;
    }}

    /* ================= HERO ================= */

    .hero-box {{
        background:
            linear-gradient(
                90deg,
                rgba(4, 39, 62, 0.94),
                rgba(4, 39, 62, 0.55)
            );

        border-radius: 20px;
        padding: 35px;
        margin-bottom: 25px;
        color: white;

        box-shadow:
            0 10px 30px
            rgba(0,0,0,0.12);
    }}

    .hero-box h1 {{
        color: white;
        font-size: 38px;
        font-weight: 800;
        margin: 0;
    }}

    .hero-box p {{
        color: #eef8fb;
        margin-top: 8px;
    }}

    /* ================= CARD ================= */

    .info-card {{
        background: rgba(255,255,255,0.97);
        border: 1px solid #e0e8ed;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;

        box-shadow:
            0 5px 18px
            rgba(0,0,0,0.05);
    }}

    /* ================= ROOM ================= */

    .room-card {{
        background: rgba(255,255,255,0.98);
        border-radius: 15px;
        padding: 15px 10px;
        text-align: center;

        border: 1px solid #dce5ea;

        min-height: 145px;

        box-shadow:
            0 3px 10px
            rgba(0,0,0,0.05);
    }}

    .room-number {{
        color: #07324f;
        font-size: 23px;
        font-weight: 800;
    }}

    .room-type {{
        color: #74828d;
        font-size: 12px;
        margin-top: 3px;
    }}

    .room-price {{
        color: #08728f;
        font-size: 13px;
        font-weight: 700;
        margin-top: 6px;
    }}

    .room-status {{
        font-size: 12px;
        font-weight: 700;
        margin-top: 10px;
    }}

    /* ================= SECTION ================= */

    .section-title {{
        color: #07324f;
        font-size: 23px;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 15px;
    }}

    /* ================= FOOTER ================= */

    .footer {{
        text-align: center;
        color: #71808c;
        font-size: 12px;
        padding: 30px 0;
    }}

    /* ================= BUTTON ================= */

    .stButton > button {{
        border-radius: 9px;
        font-weight: 700;
    }}

    /* ================= DATAFRAME ================= */

    [data-testid="stDataFrame"] {{
        border-radius: 12px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 5. HÀM TIỀN TỆ
# =========================================================

def money(value):

    try:
        return f"{int(value):,} VNĐ"

    except Exception:
        return "0 VNĐ"


# =========================================================
# 6. THÔNG TIN LOẠI PHÒNG
# =========================================================

ROOM_TYPES = {

    "Standard": {
        "price": 550000,
        "capacity": 2,
        "description": "Phòng tiêu chuẩn, phù hợp 1–2 khách."
    },

    "Deluxe": {
        "price": 750000,
        "capacity": 2,
        "description": "Phòng cao cấp, không gian rộng hơn."
    },

    "Suite": {
        "price": 1200000,
        "capacity": 3,
        "description": "Phòng Suite có không gian nghỉ dưỡng."
    },

    "Family": {
        "price": 1500000,
        "capacity": 4,
        "description": "Phòng gia đình, tối đa 4 khách."
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

            rooms.append(
                [
                    room_number,
                    floor,
                    room_type,
                    ROOM_TYPES[room_type]["price"],
                    ROOM_TYPES[room_type]["capacity"],
                    "Trống"
                ]
            )

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
# 8. DỮ LIỆU BAN ĐẦU
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


if "rooms" not in st.session_state:

    st.session_state.rooms = create_rooms()


if "bookings" not in st.session_state:

    st.session_state.bookings = create_bookings()


if "services" not in st.session_state:

    st.session_state.services = create_services()


# =========================================================
# 9. HÀM TẠO MÃ BOOKING
# =========================================================

def create_booking_id():

    number = len(
        st.session_state.bookings
    ) + 1

    return f"BK{number:04d}"


# =========================================================
# 10. CẬP NHẬT TRẠNG THÁI PHÒNG
# =========================================================

def set_room_status(
    room_number,
    new_status
):

    index = st.session_state.rooms.index[
        st.session_state.rooms["Phòng"]
        == room_number
    ]

    if len(index) > 0:

        st.session_state.rooms.loc[
            index[0],
            "Trạng thái"
        ] = new_status


# =========================================================
# 11. KIỂM TRA BOOKING TRÙNG
# =========================================================

def room_has_conflict(
    room_number,
    checkin,
    checkout
):

    bookings = st.session_state.bookings

    if bookings.empty:
        return False

    active_status = [
        "Đã đặt",
        "Đang ở"
    ]

    existing = bookings[
        (bookings["Phòng"] == room_number)
        &
        (bookings["Trạng thái"].isin(active_status))
    ]

    for _, booking in existing.iterrows():

        old_checkin = booking["Ngày nhận"]
        old_checkout = booking["Ngày trả"]

        if (
            checkin < old_checkout
            and
            checkout > old_checkin
        ):

            return True

    return False


# =========================================================
# 12. SIDEBAR
# =========================================================

with st.sidebar:

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            use_container_width=True
        )

    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:21px;
            font-weight:800;
            margin-top:5px;
        ">
            CHARM PEARL HOTEL
        </div>

        <div style="
            text-align:center;
            font-size:10px;
            letter-spacing:2px;
            margin-top:4px;
        ">
            VŨNG TÀU
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    menu = st.radio(
        "QUẢN LÝ KHÁCH SẠN",
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
        "Hệ thống quản lý đang hoạt động"
    )

    st.caption(
        "50 phòng · Charm Pearl Hotel"
    )


# =========================================================
# 13. TRANG TỔNG QUAN
# =========================================================

if menu == "🏠 Tổng quan":

    if BANNER_PATH.exists():

        st.image(
            str(BANNER_PATH),
            use_container_width=True
        )

    st.markdown(
        """
        <div class="hero-box">

            <h1>
                Charm Pearl Hotel
            </h1>

            <p>
                HỆ THỐNG QUẢN LÝ KHÁCH SẠN
            </p>

            <p>
                Quản lý phòng · Đặt phòng ·
                Check-in · Check-out · Dịch vụ ·
                Hóa đơn · Doanh thu
            </p>

        </div>
        """,
        unsafe_allow_html=True
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

    st.markdown(
        '<div class="section-title">🛏️ Sơ đồ phòng</div>',
        unsafe_allow_html=True
    )

    selected_floor = st.selectbox(
        "Chọn tầng",
        ["Tất cả", 1, 2, 3, 4, 5]
    )

    if selected_floor == "Tất cả":

        display_rooms = rooms

    else:

        display_rooms = rooms[
            rooms["Tầng"] == selected_floor
        ]

    columns = st.columns(5)

    for i, (_, room) in enumerate(
        display_rooms.iterrows()
    ):

        with columns[i % 5]:

            status = room["Trạng thái"]

            status_icon = {
                "Trống": "🟢",
                "Đã đặt": "🟣",
                "Đang ở": "🔵",
                "Đang dọn": "🟡",
                "Bảo trì": "🔴"
            }.get(status, "⚪")

            st.markdown(
                f"""
                <div class="room-card">

                    <div class="room-number">
                        {room["Phòng"]}
                    </div>

                    <div class="room-type">
                        {room["Loại phòng"]}
                    </div>

                    <div class="room-price">
                        {money(room["Giá/đêm"])}
                    </div>

                    <div class="room-status">
                        {status_icon}
                        {status}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <div class="info-card">

        🟢 Trống
        &nbsp;&nbsp;
        🟣 Đã đặt
        &nbsp;&nbsp;
        🔵 Đang ở
        &nbsp;&nbsp;
        🟡 Đang dọn
        &nbsp;&nbsp;
        🔴 Bảo trì

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 14. QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Quản lý phòng":

    st.markdown(
        '<div class="page-title">🛏️ Quản lý phòng</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Quản lý 50 phòng của Charm Pearl Hotel</div>',
        unsafe_allow_html=True
    )

    rooms = st.session_state.rooms

    c1, c2, c3 = st.columns(3)

    with c1:

        floor_filter = st.selectbox(
            "Tầng",
            ["Tất cả", 1, 2, 3, 4, 5]
        )

    with c2:

        type_filter = st.selectbox(
            "Loại phòng",
            ["Tất cả"] + list(ROOM_TYPES.keys())
        )

    with c3:

        status_filter = st.selectbox(
            "Trạng thái",
            ["Tất cả"] + STATUSES
        )

    filtered = rooms.copy()

    if floor_filter != "Tất cả":

        filtered = filtered[
            filtered["Tầng"] == floor_filter
        ]

    if type_filter != "Tất cả":

        filtered = filtered[
            filtered["Loại phòng"] == type_filter
        ]

    if status_filter != "Tất cả":

        filtered = filtered[
            filtered["Trạng thái"] == status_filter
        ]

    columns = st.columns(5)

    for i, (_, room) in enumerate(
        filtered.iterrows()
    ):

        with columns[i % 5]:

            status = room["Trạng thái"]

            icon = {
                "Trống": "🟢",
                "Đã đặt": "🟣",
                "Đang ở": "🔵",
                "Đang dọn": "🟡",
                "Bảo trì": "🔴"
            }.get(status, "⚪")

            st.markdown(
                f"""
                <div class="room-card">

                    <div class="room-number">
                        {room["Phòng"]}
                    </div>

                    <div class="room-type">
                        {room["Loại phòng"]}
                    </div>

                    <div class="room-price">
                        {money(room["Giá/đêm"])}
                    </div>

                    <div class="room-status">
                        {icon} {status}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.subheader(
        "🔧 Cập nhật trạng thái phòng"
    )

    with st.form("update_room"):

        c1, c2 = st.columns(2)

        with c1:

            room_number = st.selectbox(
                "Chọn phòng",
                rooms["Phòng"].tolist()
            )

        with c2:

            new_status = st.selectbox(
                "Trạng thái mới",
                STATUSES
            )

        submit = st.form_submit_button(
            "CẬP NHẬT PHÒNG",
            use_container_width=True
        )

    if submit:

        set_room_status(
            room_number,
            new_status
        )

        st.success(
            f"Phòng {room_number} đã chuyển sang '{new_status}'."
        )

        st.rerun()


# =========================================================
# 15. ĐẶT PHÒNG
# =========================================================

elif menu == "📅 Đặt phòng":

    st.markdown(
        '<div class="page-title">📅 Đặt phòng</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Tạo đặt phòng mới cho khách hàng</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-card">

        <b>Quy trình:</b>
        Chọn ngày → Chọn loại phòng →
        Chọn phòng → Nhập thông tin khách →
        Xác nhận đặt phòng.

        </div>
        """,
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
            value=date.today() + timedelta(days=1),
            min_value=date.today() + timedelta(days=1)
        )

    # Kiểm tra ngày

    if checkout <= checkin:

        st.error(
            "Ngày trả phòng phải sau ngày nhận phòng."
        )

    else:

        nights = (
            checkout - checkin
        ).days

        # =================================================
        # CHỌN LOẠI PHÒNG
        # =================================================

        room_type = st.selectbox(
            "Loại phòng",
            list(ROOM_TYPES.keys())
        )

        room_info = ROOM_TYPES[room_type]

        st.info(
            f"{room_info['description']} "
            f"· Tối đa {room_info['capacity']} khách "
            f"· {money(room_info['price'])}/đêm"
        )

        # =================================================
        # TÌM PHÒNG KHÔNG BỊ TRÙNG
        # =================================================

        candidate_rooms = st.session_state.rooms[
            st.session_state.rooms["Loại phòng"]
            == room_type
        ].copy()

        available_rooms = []

        for _, room in candidate_rooms.iterrows():

            if room["Trạng thái"] == "Bảo trì":
                continue

            if room["Trạng thái"] == "Đang dọn":
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
                "Không có phòng phù hợp trong khoảng thời gian này. "
                "Em hãy đổi ngày hoặc loại phòng."
            )

        else:

            room = st.selectbox(
                f"Phòng còn trống ({len(available_rooms)} phòng)",
                available_rooms
            )

            st.success(
                f"Phòng {room} đang có thể đặt."
            )

            # =============================================
            # THÔNG TIN KHÁCH
            # =============================================

            st.subheader(
                "👤 Thông tin khách hàng"
            )

            c1, c2 = st.columns(2)

            with c1:

                guest_name = st.text_input(
                    "Họ và tên *",
                    placeholder="Nguyễn Văn A"
                )

                phone = st.text_input(
                    "Số điện thoại *",
                    placeholder="0901234567"
                )

            with c2:

                guest_count = st.number_input(
                    "Số khách *",
                    min_value=1,
                    max_value=room_info["capacity"],
                    value=1
                )

                note = st.text_area(
                    "Ghi chú",
                    placeholder="Yêu cầu đặc biệt của khách..."
                )

            # =============================================
            # TÍNH TIỀN
            # =============================================

            room_price = room_info["price"]

            room_total = (
                room_price * nights
            )

            st.markdown(
                f"""
                <div class="info-card">

                <h3>💰 Chi tiết đặt phòng</h3>

                <p>
                Phòng:
                <b>{room}</b>
                </p>

                <p>
                Loại:
                <b>{room_type}</b>
                </p>

                <p>
                Thời gian:
                <b>{nights} đêm</b>
                </p>

                <p>
                Giá:
                <b>{money(room_price)}/đêm</b>
                </p>

                <hr>

                <h2>
                Tổng tiền:
                {money(room_total)}
                </h2>

                </div>
                """,
                unsafe_allow_html=True
            )

            # =============================================
            # XÁC NHẬN
            # =============================================

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
                    room,
                    checkin,
                    checkout
                ):

                    st.error(
                        "Phòng vừa được đặt bởi khách khác. "
                        "Vui lòng chọn phòng khác."
                    )

                else:

                    booking_id = create_booking_id()

                    new_booking = pd.DataFrame(
                        [[
                            booking_id,
                            room,
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
                        columns=st.session_state.bookings.columns
                    )

                    st.session_state.bookings = pd.concat(
                        [
                            st.session_state.bookings,
                            new_booking
                        ],
                        ignore_index=True
                    )

                    set_room_status(
                        room,
                        "Đã đặt"
                    )

                    st.success(
                        f"ĐẶT PHÒNG THÀNH CÔNG — Mã đặt phòng: {booking_id}"
                    )

                    st.info(
                        f"Phòng {room} · {guest_name} · "
                        f"{nights} đêm · {money(room_total)}"
                    )

                    st.balloons()


# =========================================================
# 16. CHECK-IN
# =========================================================

elif menu == "🛎️ Check-in":

    st.markdown(
        '<div class="page-title">🛎️ Check-in</div>',
        unsafe_allow_html=True
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
            "Chọn mã đặt phòng",
            pending["Mã đặt phòng"].tolist()
        )

        booking_index = pending.index[
            pending["Mã đặt phòng"]
            == booking_id
        ][0]

        booking = bookings.loc[
            booking_index
        ]

        st.markdown(
            f"""
            <div class="info-card">

            <h3>Thông tin đặt phòng</h3>

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

            <br><br>

            <b>Số khách:</b>
            {booking["Số khách"]}

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
                booking_index,
                "Trạng thái"
            ] = "Đang ở"

            set_room_status(
                booking["Phòng"],
                "Đang ở"
            )

            st.success(
                f"Khách {booking['Tên khách']} đã check-in phòng {booking['Phòng']}."
            )

            st.rerun()


# =========================================================
# 17. CHECK-OUT
# =========================================================

elif menu == "🚪 Check-out":

    st.markdown(
        '<div class="page-title">🚪 Check-out</div>',
        unsafe_allow_html=True
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

        booking_index = staying.index[
            staying["Mã đặt phòng"]
            == booking_id
        ][0]

        booking = bookings.loc[
            booking_index
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
            + service_fee
        )

        st.markdown(
            f"""
            <div class="info-card">

            <h2>
            Tổng thanh toán:
            {money(total)}
            </h2>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "💳 THANH TOÁN & CHECK-OUT",
            type="primary",
            use_container_width=True
        ):

            st.session_state.bookings.loc[
                booking_index,
                "Dịch vụ"
            ] = service_fee

            st.session_state.bookings.loc[
                booking_index,
                "Tổng tiền"
            ] = total

            st.session_state.bookings.loc[
                booking_index,
                "Trạng thái"
            ] = "Đã trả phòng"

            set_room_status(
                booking["Phòng"],
                "Đang dọn"
            )

            st.success(
                f"Đã thanh toán và check-out phòng {booking['Phòng']}."
            )

            st.rerun()


# =========================================================
# 18. KHÁCH HÀNG / BOOKING
# =========================================================

elif menu == "👥 Khách hàng":

    st.markdown(
        '<div class="page-title">👥 Khách hàng</div>',
        unsafe_allow_html=True
    )

    bookings = st.session_state.bookings.copy()

    if bookings.empty:

        st.info(
            "Chưa có dữ liệu khách hàng."
        )

    else:

        search = st.text_input(
            "🔎 Tìm theo tên, số điện thoại, phòng hoặc mã booking"
        )

        if search:

            mask = bookings.astype(str).apply(
                lambda column:
                column.str.contains(
                    search,
                    case=False,
                    na=False
                )
            ).any(axis=1)

            bookings = bookings[mask]

        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 19. DỊCH VỤ
# =========================================================

elif menu == "🍽️ Dịch vụ":

    st.markdown(
        '<div class="page-title">🍽️ Dịch vụ khách sạn</div>',
        unsafe_allow_html=True
    )

    services = st.session_state.services.copy()

    display_services = services.copy()

    display_services["Đơn giá"] = (
        display_services["Đơn giá"]
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

    with st.form("service_form"):

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
# 20. HÓA ĐƠN
# =========================================================

elif menu == "🧾 Hóa đơn":

    st.markdown(
        '<div class="page-title">🧾 Hóa đơn</div>',
        unsafe_allow_html=True
    )

    bookings = st.session_state.bookings

    if bookings.empty:

        st.info(
            "Chưa có hóa đơn."
        )

    else:

        booking_id = st.selectbox(
            "Chọn mã đặt phòng",
            bookings["Mã đặt phòng"].tolist()
        )

        booking = bookings[
            bookings["Mã đặt phòng"]
            == booking_id
        ].iloc[0]

        st.markdown(
            f"""
            <div class="info-card">

            <div style="
                text-align:center;
            ">

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
# 21. DOANH THU
# =========================================================

elif menu == "💰 Doanh thu":

    st.markdown(
        '<div class="page-title">💰 Doanh thu</div>',
        unsafe_allow_html=True
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
            "Khoản thu": [
                "Tiền phòng",
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
        chart.set_index(
            "Khoản thu"
        )
    )

    if not bookings.empty:

        st.subheader(
            "Chi tiết giao dịch"
        )

        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 22. BÁO CÁO
# =========================================================

elif menu == "📊 Báo cáo":

    st.markdown(
        '<div class="page-title">📊 Báo cáo vận hành</div>',
        unsafe_allow_html=True
    )

    rooms = st.session_state.rooms
    bookings = st.session_state.bookings

    total_rooms = len(rooms)

    occupied = len(
        rooms[
            rooms["Trạng thái"]
            == "Đang ở"
        ]
    )

    reserved = len(
        rooms[
            rooms["Trạng thái"]
            == "Đã đặt"
        ]
    )

    available = len(
        rooms[
            rooms["Trạng thái"]
            == "Trống"
        ]
    )

    occupancy = (
        occupied / total_rooms
        if total_rooms > 0
        else 0
    )

    total_revenue = (
        bookings["Tổng tiền"].sum()
        if not bookings.empty
        else 0
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Tổng phòng",
        total_rooms
    )

    c2.metric(
        "Phòng trống",
        available
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
        "Công suất",
        f"{occupancy:.0%}"
    )

    st.progress(
        occupancy
    )

    st.subheader(
        "📊 Trạng thái phòng"
    )

    status_chart = rooms[
        "Trạng thái"
    ].value_counts()

    st.bar_chart(
        status_chart
    )

    st.subheader(
        "📋 Danh sách phòng"
    )

    display_rooms = rooms.copy()

    display_rooms["Giá/đêm"] = (
        display_rooms["Giá/đêm"]
        .apply(money)
    )

    st.dataframe(
        display_rooms,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "📅 Danh sách đặt phòng"
    )

    if bookings.empty:

        st.info(
            "Chưa có đặt phòng."
        )

    else:

        st.dataframe(
            bookings,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 23. FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        <br>

        CHARM PEARL HOTEL · VŨNG TÀU

        <br>

        Hotel Management System

        <br><br>

        © 2026

    </div>
    """,
    unsafe_allow_html=True
)
