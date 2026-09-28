import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pathlib import Path
import base64
import re

# =========================================================
# CHARM PEARL HOTEL
# HOTEL MANAGEMENT SYSTEM
# =========================================================

st.set_page_config(
    page_title="Charm Pearl Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 1. FILE ẢNH
# =========================================================

BASE = Path(__file__).parent

LOGO = BASE / "IMG_LOGO11.jpg"
BANNER = BASE / "IMG_BANNER2.jpg"
BACKGROUND = BASE / "IMG_NENCHIM3.jpg"


# =========================================================
# 2. THÔNG TIN KHÁCH SẠN
# =========================================================

HOTEL_NAME = "CHARM PEARL HOTEL"
HOTEL_LOCATION = "Vũng Tàu"

ROOM_TYPES = {
    "Standard": {
        "price": 550000,
        "capacity": 2,
        "description": "Phòng tiêu chuẩn, tiện nghi và phù hợp cho 1–2 khách."
    },

    "Deluxe": {
        "price": 750000,
        "capacity": 2,
        "description": "Phòng Deluxe rộng rãi, thiết kế hiện đại và thoải mái."
    },

    "Suite": {
        "price": 1200000,
        "capacity": 3,
        "description": "Phòng Suite cao cấp với không gian nghỉ dưỡng rộng rãi."
    },

    "Family": {
        "price": 1500000,
        "capacity": 4,
        "description": "Phòng Family phù hợp cho gia đình hoặc nhóm khách."
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
# 3. HÀM CƠ BẢN
# =========================================================

def money(value):
    try:
        return f"{int(value):,}".replace(",", ".") + " VNĐ"
    except:
        return "0 VNĐ"


def exists(path):
    return path.exists()


def status_icon(status):
    return {
        "Trống": "🟢",
        "Đã đặt": "🟣",
        "Đang ở": "🔵",
        "Đang dọn": "🟡",
        "Bảo trì": "🔴"
    }.get(status, "⚪")


# =========================================================
# 4. TẠO 50 PHÒNG
# =========================================================

def create_rooms():

    data = []

    for floor in range(1, 6):

        for number in range(1, 11):

            room = f"{floor}{number:02d}"

            if number <= 4:
                room_type = "Standard"

            elif number <= 8:
                room_type = "Deluxe"

            elif number == 9:
                room_type = "Suite"

            else:
                room_type = "Family"

            data.append({
                "Phòng": room,
                "Tầng": floor,
                "Loại phòng": room_type,
                "Giá": ROOM_TYPES[room_type]["price"],
                "Sức chứa": ROOM_TYPES[room_type]["capacity"],
                "Trạng thái": "Trống"
            })

    return pd.DataFrame(data)


# =========================================================
# 5. SESSION STATE
# =========================================================

if "rooms" not in st.session_state:
    st.session_state.rooms = create_rooms()


if "bookings" not in st.session_state:

    st.session_state.bookings = pd.DataFrame(
        columns=[
            "Mã booking",
            "Phòng",
            "Khách hàng",
            "Số điện thoại",
            "Số khách",
            "Check-in",
            "Check-out",
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
            ["DV006", "Spa", 300000],
            ["DV007", "Đưa đón sân bay", 350000]
        ],
        columns=[
            "Mã",
            "Dịch vụ",
            "Đơn giá"
        ]
    )


# =========================================================
# 6. CHAT HISTORY
# =========================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content":
                "Xin chào! Tôi là trợ lý ảo của "
                "Charm Pearl Hotel. 🏨\n\n"
                "Tôi có thể hỗ trợ bạn về phòng, "
                "giá phòng, dịch vụ, phòng trống "
                "và hướng dẫn đặt phòng."
        }
    ]


# =========================================================
# 7. CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    font-family: Arial, sans-serif;
}

/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
        180deg,
        #082c3c 0%,
        #0d4558 55%,
        #123f4e 100%
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}


/* ================================
   HERO
================================ */

.hero {

    background:
    rgba(255,255,255,0.95);

    padding: 28px;

    border-radius: 22px;

    text-align: center;

    margin-bottom: 22px;

    box-shadow:
    0 6px 25px rgba(0,0,0,0.08);
}

.hero-title {

    color: #123c4c;

    font-size: 38px;

    font-weight: 800;

    letter-spacing: 2px;
}

.hero-sub {

    color: #71828a;

    margin-top: 6px;

    font-size: 15px;
}


/* ================================
   SECTION
================================ */

.section-title {

    color: #143d4d;

    font-size: 25px;

    font-weight: 800;

    margin-top: 25px;

    margin-bottom: 15px;
}


/* ================================
   DASHBOARD CARD
================================ */

.dashboard-card {

    background:
    rgba(255,255,255,0.96);

    padding: 20px;

    border-radius: 17px;

    min-height: 110px;

    box-shadow:
    0 4px 18px rgba(0,0,0,0.07);

    border:
    1px solid #e7edef;
}

.dashboard-label {

    color: #75868e;

    font-size: 14px;
}

.dashboard-value {

    color: #123c4c;

    font-size: 27px;

    font-weight: 800;

    margin-top: 8px;
}


/* ================================
   ROOM CARD
================================ */

.room-card {

    background:
    rgba(255,255,255,0.97);

    padding: 14px;

    border-radius: 15px;

    margin-bottom: 12px;

    border:
    1px solid #e2e8eb;

    box-shadow:
    0 3px 12px rgba(0,0,0,0.05);
}

.room-number {

    color: #123c4c;

    font-size: 21px;

    font-weight: 800;
}

.room-type {

    color: #71828a;

    font-size: 13px;

    margin-top: 4px;
}

.room-status {

    font-weight: 700;

    margin-top: 8px;
}


/* ================================
   CHATBOX
================================ */

.chat-header {

    background:
    linear-gradient(
        135deg,
        #123c4c,
        #0b6075
    );

    color: white;

    padding: 24px;

    border-radius: 20px;

    margin-bottom: 20px;

    box-shadow:
    0 6px 25px rgba(0,0,0,0.12);
}

.chat-header h2 {

    margin: 0;
}

.chat-header p {

    margin-bottom: 0;

    opacity: 0.9;
}


/* ================================
   BUTTON
================================ */

.stButton > button {

    border-radius: 10px;

    font-weight: 700;

    min-height: 42px;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# 8. NỀN CHÌM
# =========================================================

if exists(BACKGROUND):

    try:

        encoded = base64.b64encode(
            BACKGROUND.read_bytes()
        ).decode()

        st.markdown(
            f"""
            <style>

            .stApp {{

                background-image:

                linear-gradient(
                    rgba(245,248,249,0.94),
                    rgba(245,248,249,0.94)
                ),

                url(
                    "data:image/jpeg;base64,{encoded}"
                );

                background-size: cover;

                background-position: center;

                background-attachment: fixed;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except:
        pass


# =========================================================
# 9. SIDEBAR
# =========================================================

with st.sidebar:

    # LOGO BÊN TRÁI

    if exists(LOGO):

        st.image(
            str(LOGO),
            width=85
        )

    st.markdown(
        "## CHARM PEARL"
    )

    st.caption(
        "HOTEL MANAGEMENT SYSTEM"
    )

    st.divider()

    menu = st.radio(
        "QUẢN LÝ",
        [
            "🏠 Dashboard",
            "🛏️ Phòng",
            "📅 Đặt phòng",
            "🛎️ Check-in",
            "🚪 Check-out",
            "👥 Khách hàng",
            "🍽️ Dịch vụ",
            "🧾 Hóa đơn",
            "💰 Doanh thu",
            "📊 Báo cáo",
            "💬 Chat với Charm Pearl"
        ]
    )

    st.divider()

    st.caption(
        "CHARM PEARL HOTEL"
    )

    st.caption(
        "Vũng Tàu"
    )

    st.caption(
        "50 phòng · 5 tầng"
    )


# =========================================================
# 10. DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                CHARM PEARL HOTEL
            </div>

            <div class="hero-sub">
                Hotel Management System · Vũng Tàu
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # BANNER CHÍNH GIỮA

    if exists(BANNER):

        left, center, right = st.columns(
            [1, 2.5, 1]
        )

        with center:

            st.image(
                str(BANNER),
                use_container_width=True
            )


    # THỐNG KÊ

    st.markdown(
        '<div class="section-title">'
        'Tổng quan khách sạn'
        '</div>',
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

    revenue = (
        0
        if bookings.empty
        else bookings["Tổng tiền"].sum()
    )

    cards = st.columns(5)

    card_data = [
        ("🏨", "Tổng phòng", total_rooms),
        ("🟢", "Phòng trống", empty_rooms),
        ("🟣", "Đã đặt", reserved_rooms),
        ("🔵", "Đang ở", occupied_rooms),
        ("💰", "Doanh thu", money(revenue))
    ]

    for col, item in zip(cards, card_data):

        with col:

            st.markdown(
                f"""
                <div class="dashboard-card">

                    <div class="dashboard-label">
                        {item[0]} {item[1]}
                    </div>

                    <div class="dashboard-value">
                        {item[2]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    # SƠ ĐỒ PHÒNG

    st.markdown(
        '<div class="section-title">'
        'Sơ đồ 50 phòng'
        '</div>',
        unsafe_allow_html=True
    )

    floor = st.selectbox(
        "Chọn tầng",
        ["Tất cả", 1, 2, 3, 4, 5],
        key="dashboard_floor"
    )

    if floor == "Tất cả":

        display_rooms = rooms

    else:

        display_rooms = rooms[
            rooms["Tầng"] == floor
        ]

    room_cols = st.columns(5)

    for index, (_, room) in enumerate(
        display_rooms.iterrows()
    ):

        with room_cols[index % 5]:

            st.markdown(
                f"""
                <div class="room-card">

                    <div class="room-number">
                        🛏️ {room["Phòng"]}
                    </div>

                    <div class="room-type">
                        {room["Loại phòng"]}
                        · Tầng {room["Tầng"]}
                    </div>

                    <div>
                        {money(room["Giá"])}
                        / đêm
                    </div>

                    <div>
                        👥 {room["Sức chứa"]} khách
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
# 11. QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Phòng":

    st.title(
        "🛏️ Quản lý phòng"
    )

    rooms = st.session_state.rooms

    col1, col2, col3 = st.columns(3)

    with col1:

        floor = st.selectbox(
            "Tầng",
            ["Tất cả", 1, 2, 3, 4, 5]
        )

    with col2:

        room_type = st.selectbox(
            "Loại phòng",
            ["Tất cả"] + list(ROOM_TYPES.keys())
        )

    with col3:

        status = st.selectbox(
            "Trạng thái",
            ["Tất cả"] + STATUSES
        )

    filtered = rooms.copy()

    if floor != "Tất cả":

        filtered = filtered[
            filtered["Tầng"] == floor
        ]

    if room_type != "Tất cả":

        filtered = filtered[
            filtered["Loại phòng"] == room_type
        ]

    if status != "Tất cả":

        filtered = filtered[
            filtered["Trạng thái"] == status
        ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "Cập nhật trạng thái phòng"
    )

    with st.form("room_update_form"):

        selected_room = st.selectbox(
            "Phòng",
            rooms["Phòng"].tolist()
        )

        selected_status = st.selectbox(
            "Trạng thái mới",
            STATUSES
        )

        submit = st.form_submit_button(
            "CẬP NHẬT",
            use_container_width=True
        )

    if submit:

        st.session_state.rooms.loc[
            st.session_state.rooms["Phòng"]
            == selected_room,
            "Trạng thái"
        ] = selected_status

        st.success(
            f"Phòng {selected_room} → "
            f"{selected_status}"
        )

        st.rerun()


# =========================================================
# 12. ĐẶT PHÒNG
# =========================================================

elif menu == "📅 Đặt phòng":

    st.title(
        "📅 Đặt phòng"
    )

    col1, col2 = st.columns(2)

    with col1:

        check_in = st.date_input(
            "Ngày check-in",
            date.today()
        )

    with col2:

        check_out = st.date_input(
            "Ngày check-out",
            date.today() + timedelta(days=1)
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
            list(ROOM_TYPES.keys())
        )

        available = st.session_state.rooms[
            (st.session_state.rooms["Loại phòng"] == room_type)
            &
            (st.session_state.rooms["Trạng thái"] == "Trống")
        ]

        if available.empty:

            st.error(
                "Hiện không còn phòng trống "
                "thuộc hạng này."
            )

        else:

            room = st.selectbox(
                "Chọn phòng",
                available["Phòng"].tolist()
            )

            st.success(
                f"Còn {len(available)} phòng "
                f"{room_type}."
            )

            col1, col2 = st.columns(2)

            with col1:

                guest = st.text_input(
                    "Tên khách *"
                )

                phone = st.text_input(
                    "Số điện thoại *"
                )

            with col2:

                capacity = ROOM_TYPES[
                    room_type
                ]["capacity"]

                guests = st.number_input(
                    "Số khách",
                    min_value=1,
                    max_value=capacity,
                    value=1
                )

                st.text_area(
                    "Ghi chú"
                )

            price = ROOM_TYPES[
                room_type
            ]["price"]

            total = price * nights

            st.info(
                f"Phòng {room} · "
                f"{nights} đêm · "
                f"{money(total)}"
            )

            if st.button(
                "📅 XÁC NHẬN ĐẶT PHÒNG",
                type="primary",
                use_container_width=True
            ):

                if not guest.strip():

                    st.error(
                        "Vui lòng nhập tên khách."
                    )

                elif not phone.strip():

                    st.error(
                        "Vui lòng nhập số điện thoại."
                    )

                else:

                    booking_number = (
                        len(st.session_state.bookings)
                        + 1
                    )

                    booking_id = (
                        f"BK{booking_number:04d}"
                    )

                    new_booking = pd.DataFrame(
                        [{
                            "Mã booking": booking_id,
                            "Phòng": room,
                            "Khách hàng": guest,
                            "Số điện thoại": phone,
                            "Số khách": guests,
                            "Check-in": check_in,
                            "Check-out": check_out,
                            "Số đêm": nights,
                            "Tiền phòng": total,
                            "Dịch vụ": 0,
                            "Tổng tiền": total,
                            "Trạng thái": "Đã đặt"
                        }]
                    )

                    st.session_state.bookings = pd.concat(
                        [
                            st.session_state.bookings,
                            new_booking
                        ],
                        ignore_index=True
                    )

                    st.session_state.rooms.loc[
                        st.session_state.rooms["Phòng"]
                        == room,
                        "Trạng thái"
                    ] = "Đã đặt"

                    st.success(
                        f"Đặt phòng thành công! "
                        f"Mã booking: {booking_id}"
                    )


# =========================================================
# 13. CHECK-IN
# =========================================================

elif menu == "🛎️ Check-in":

    st.title(
        "🛎️ Check-in"
    )

    bookings = st.session_state.bookings

    waiting = bookings[
        bookings["Trạng thái"] == "Đã đặt"
    ]

    if waiting.empty:

        st.info(
            "Không có booking chờ check-in."
        )

    else:

        booking_id = st.selectbox(
            "Mã booking",
            waiting["Mã booking"].tolist()
        )

        selected = waiting[
            waiting["Mã booking"] == booking_id
        ].iloc[0]

        st.info(
            f"""
            Khách: {selected["Khách hàng"]}

            Phòng: {selected["Phòng"]}

            Check-in: {selected["Check-in"]}

            Check-out: {selected["Check-out"]}
            """
        )

        if st.button(
            "🛎️ XÁC NHẬN CHECK-IN",
            type="primary",
            use_container_width=True
        ):

            index = st.session_state.bookings.index[
                st.session_state.bookings["Mã booking"]
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
                "Check-in thành công."
            )

            st.rerun()


# =========================================================
# 14. CHECK-OUT
# =========================================================

elif menu == "🚪 Check-out":

    st.title(
        "🚪 Check-out"
    )

    bookings = st.session_state.bookings

    staying = bookings[
        bookings["Trạng thái"] == "Đang ở"
    ]

    if staying.empty:

        st.info(
            "Không có khách đang ở."
        )

    else:

        booking_id = st.selectbox(
            "Booking",
            staying["Mã booking"].tolist()
        )

        selected = staying[
            staying["Mã booking"] == booking_id
        ].iloc[0]

        extra = st.number_input(
            "Dịch vụ phát sinh",
            min_value=0,
            step=50000
        )

        total = (
            selected["Tiền phòng"]
            + extra
        )

        st.metric(
            "Tổng thanh toán",
            money(total)
        )

        if st.button(
            "💳 THANH TOÁN & CHECK-OUT",
            type="primary",
            use_container_width=True
        ):

            index = st.session_state.bookings.index[
                st.session_state.bookings["Mã booking"]
                == booking_id
            ][0]

            st.session_state.bookings.loc[
                index,
                "Dịch vụ"
            ] = extra

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
                "Check-out thành công."
            )

            st.rerun()


# =========================================================
# 15. KHÁCH HÀNG
# =========================================================

elif menu == "👥 Khách hàng":

    st.title(
        "👥 Khách hàng"
    )

    bookings = st.session_state.bookings

    if bookings.empty:

        st.info(
            "Chưa có dữ liệu khách hàng."
        )

    else:

        keyword = st.text_input(
            "🔎 Tìm kiếm khách hàng"
        )

        data = bookings.copy()

        if keyword:

            mask = data.astype(str).apply(
                lambda x:
                x.str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            ).any(axis=1)

            data = data[mask]

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 16. DỊCH VỤ
# =========================================================

elif menu == "🍽️ Dịch vụ":

    st.title(
        "🍽️ Dịch vụ khách sạn"
    )

    st.dataframe(
        st.session_state.services,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader(
        "Thêm dịch vụ"
    )

    with st.form("service_form"):

        col1, col2, col3 = st.columns(3)

        with col1:

            code = st.text_input(
                "Mã dịch vụ"
            )

        with col2:

            name = st.text_input(
                "Tên dịch vụ"
            )

        with col3:

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

        if not code.strip():

            st.error(
                "Vui lòng nhập mã dịch vụ."
            )

        elif not name.strip():

            st.error(
                "Vui lòng nhập tên dịch vụ."
            )

        else:

            new_service = pd.DataFrame(
                [[code, name, price]],
                columns=[
                    "Mã",
                    "Dịch vụ",
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
# 17. HÓA ĐƠN
# =========================================================

elif menu == "🧾 Hóa đơn":

    st.title(
        "🧾 Hóa đơn"
    )

    bookings = st.session_state.bookings

    if bookings.empty:

        st.info(
            "Chưa có hóa đơn."
        )

    else:

        booking_id = st.selectbox(
            "Chọn booking",
            bookings["Mã booking"].tolist()
        )

        invoice = bookings[
            bookings["Mã booking"] == booking_id
        ].iloc[0]

        st.markdown(
            f"""
            ## CHARM PEARL HOTEL

            **Vũng Tàu**

            ---

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

            ### TỔNG: {money(invoice["Tổng tiền"])}
            """
        )


# =========================================================
# 18. DOANH THU
# =========================================================

elif menu == "💰 Doanh thu":

    st.title(
        "💰 Doanh thu"
    )

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

    total = (
        room_revenue
        + service_revenue
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Doanh thu phòng",
            money(room_revenue)
        )

    with col2:

        st.metric(
            "Dịch vụ",
            money(service_revenue)
        )

    with col3:

        st.metric(
            "Tổng doanh thu",
            money(total)
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
# 19. BÁO CÁO
# =========================================================

elif menu == "📊 Báo cáo":

    st.title(
        "📊 Báo cáo khách sạn"
    )

    rooms = st.session_state.rooms

    status_count = (
        rooms["Trạng thái"]
        .value_counts()
        .reindex(
            STATUSES,
            fill_value=0
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Tổng phòng",
            len(rooms)
        )

    with col2:

        st.metric(
            "Phòng trống",
            int(status_count["Trống"])
        )

    with col3:

        st.metric(
            "Đang ở",
            int(status_count["Đang ở"])
        )

    with col4:

        st.metric(
            "Bảo trì",
            int(status_count["Bảo trì"])
        )

    st.subheader(
        "Tình trạng phòng"
    )

    st.bar_chart(
        status_count
    )

    st.subheader(
        "Danh sách 50 phòng"
    )

    st.dataframe(
        rooms,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# 20. CHATBOX
# =========================================================

elif menu == "💬 Chat với Charm Pearl":

    st.markdown(
        """
        <div class="chat-header">

            <h2>💬 Charm Pearl Concierge</h2>

            <p>
                Trợ lý trực tuyến của Charm Pearl Hotel
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.info(
        "Bạn có thể hỏi về phòng, giá phòng, "
        "phòng còn trống, dịch vụ hoặc cách đặt phòng."
    )


    # =====================================================
    # HÀM XỬ LÝ CHAT
    # =====================================================

    def chatbot_response(question):

        q = question.lower().strip()

        rooms = st.session_state.rooms
        services = st.session_state.services


        # ---------------------------------------------
        # CHÀO HỎI
        # ---------------------------------------------

        if any(
            word in q
            for word in [
                "xin chào",
                "chào",
                "hello",
                "hi",
                "hey"
            ]
        ):

            return (
                "Xin chào! Tôi là trợ lý ảo "
                "của Charm Pearl Hotel. 🏨\n\n"
                "Tôi có thể giúp bạn tìm hiểu "
                "về phòng, giá phòng, dịch vụ "
                "và đặt phòng."
            )


        # ---------------------------------------------
        # TỔNG SỐ PHÒNG
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "bao nhiêu phòng",
                "mấy phòng",
                "số lượng phòng",
                "tổng số phòng"
            ]
        ):

            return (
                "Charm Pearl Hotel hiện có "
                "50 phòng trên 5 tầng."
            )


        # ---------------------------------------------
        # PHÒNG TRỐNG
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "phòng trống",
                "còn phòng",
                "còn phòng nào",
                "phòng nào còn",
                "phòng đang trống"
            ]
        ):

            available = rooms[
                rooms["Trạng thái"] == "Trống"
            ]

            if available.empty:

                return (
                    "Hiện tại hệ thống không ghi nhận "
                    "phòng trống."
                )

            result = []

            for room_type in ROOM_TYPES:

                count = len(
                    available[
                        available["Loại phòng"]
                        == room_type
                    ]
                )

                if count > 0:

                    result.append(
                        f"• {room_type}: {count} phòng"
                    )

            return (
                "Hiện Charm Pearl Hotel đang có:\n\n"
                + "\n".join(result)
            )


        # ---------------------------------------------
        # HỎI GIÁ PHÒNG
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "giá phòng",
                "giá bao nhiêu",
                "bao nhiêu tiền",
                "phòng bao nhiêu",
                "giá các phòng"
            ]
        ):

            result = []

            for room_type, info in ROOM_TYPES.items():

                result.append(
                    f"• {room_type}: "
                    f"{money(info['price'])}/đêm"
                )

            return (
                "Bảng giá phòng hiện tại:\n\n"
                + "\n".join(result)
            )


        # ---------------------------------------------
        # HỎI RIÊNG TỪNG HẠNG PHÒNG
        # ---------------------------------------------

        for room_type, info in ROOM_TYPES.items():

            if room_type.lower() in q:

                available = len(
                    rooms[
                        (rooms["Loại phòng"] == room_type)
                        &
                        (rooms["Trạng thái"] == "Trống")
                    ]
                )

                return (
                    f"🏨 {room_type}\n\n"
                    f"💰 Giá: {money(info['price'])}/đêm\n"
                    f"👥 Sức chứa: {info['capacity']} khách\n"
                    f"🟢 Hiện còn: {available} phòng\n\n"
                    f"{info['description']}"
                )


        # ---------------------------------------------
        # SỨC CHỨA
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "mấy người",
                "bao nhiêu người",
                "sức chứa",
                "ở được bao nhiêu"
            ]
        ):

            result = []

            for room_type, info in ROOM_TYPES.items():

                result.append(
                    f"• {room_type}: "
                    f"{info['capacity']} khách"
                )

            return (
                "Sức chứa các hạng phòng:\n\n"
                + "\n".join(result)
            )


        # ---------------------------------------------
        # DỊCH VỤ
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "dịch vụ",
                "tiện ích",
                "có những gì",
                "khách sạn có gì"
            ]
        ):

            result = []

            for _, service in services.iterrows():

                result.append(
                    f"• {service['Dịch vụ']}: "
                    f"{money(service['Đơn giá'])}"
                )

            return (
                "Charm Pearl Hotel hiện có "
                "các dịch vụ:\n\n"
                + "\n".join(result)
            )


        # ---------------------------------------------
        # SPA
        # ---------------------------------------------

        if "spa" in q:

            spa = services[
                services["Dịch vụ"]
                .str.lower()
                .str.contains("spa")
            ]

            if not spa.empty:

                price = spa.iloc[0]["Đơn giá"]

                return (
                    "Có. Charm Pearl Hotel có "
                    f"dịch vụ Spa với giá "
                    f"tham khảo {money(price)}."
                )

            return (
                "Bạn vui lòng liên hệ lễ tân "
                "để kiểm tra tình trạng dịch vụ Spa."
            )


        # ---------------------------------------------
        # ĂN SÁNG
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "ăn sáng",
                "bữa sáng",
                "breakfast"
            ]
        ):

            breakfast = services[
                services["Dịch vụ"]
                .str.lower()
                .str.contains("ăn sáng")
            ]

            if not breakfast.empty:

                price = breakfast.iloc[0]["Đơn giá"]

                return (
                    "Charm Pearl Hotel có dịch vụ "
                    f"ăn sáng với giá "
                    f"{money(price)}/khách."
                )

            return (
                "Bạn vui lòng liên hệ lễ tân "
                "để biết thông tin ăn sáng."
            )


        # ---------------------------------------------
        # CHECK-IN
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "check in",
                "check-in",
                "nhận phòng"
            ]
        ):

            return (
                "Bạn có thể thực hiện thủ tục "
                "check-in tại quầy lễ tân. "
                "Nếu đã có booking, vui lòng "
                "cung cấp mã đặt phòng khi nhận phòng."
            )


        # ---------------------------------------------
        # CHECK-OUT
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "check out",
                "check-out",
                "trả phòng"
            ]
        ):

            return (
                "Khi trả phòng, bạn vui lòng "
                "liên hệ quầy lễ tân để kiểm tra "
                "phòng và thanh toán các khoản "
                "phát sinh nếu có."
            )


        # ---------------------------------------------
        # ĐẶT PHÒNG
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "đặt phòng",
                "book phòng",
                "booking",
                "muốn đặt",
                "đặt giúp"
            ]
        ):

            return (
                "Bạn có thể đặt phòng trực tiếp "
                "trong mục 📅 Đặt phòng ở menu "
                "bên trái.\n\n"
                "Tại đó bạn có thể chọn ngày, "
                "hạng phòng, số phòng và nhập "
                "thông tin khách."
            )


        # ---------------------------------------------
        # VỊ TRÍ
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "ở đâu",
                "địa chỉ",
                "vị trí",
                "địa điểm"
            ]
        ):

            return (
                "Charm Pearl Hotel tọa lạc tại "
                "Vũng Tàu."
            )


        # ---------------------------------------------
        # CẢM ƠN
        # ---------------------------------------------

        if any(
            phrase in q
            for phrase in [
                "cảm ơn",
                "thank",
                "thanks"
            ]
        ):

            return (
                "Rất hân hạnh được hỗ trợ bạn. "
                "Nếu muốn đặt phòng, bạn có thể "
                "chọn mục 📅 Đặt phòng."
            )


        # ---------------------------------------------
        # KHÔNG HIỂU
        # ---------------------------------------------

        return (
            "Tôi chưa hiểu rõ câu hỏi của bạn.\n\n"
            "Bạn có thể thử hỏi:\n\n"
            "• Khách sạn có bao nhiêu phòng?\n"
            "• Còn phòng Deluxe không?\n"
            "• Giá phòng Suite bao nhiêu?\n"
            "• Family ở được mấy người?\n"
            "• Khách sạn có dịch vụ gì?\n"
            "• Có Spa không?\n"
            "• Tôi muốn đặt phòng."
        )


    # =====================================================
    # GỢI Ý NHANH
    # =====================================================

    st.markdown(
        "### Câu hỏi nhanh"
    )

    quick1, quick2, quick3, quick4 = st.columns(4)


    with quick1:

        if st.button(
            "🏨 Còn phòng?",
            use_container_width=True
        ):

            question = "Hiện khách sạn còn phòng nào?"


            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )


            answer = chatbot_response(
                question
            )


            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            st.rerun()


    with quick2:

        if st.button(
            "💰 Giá phòng",
            use_container_width=True
        ):

            question = "Giá các phòng bao nhiêu?"


            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )


            answer = chatbot_response(
                question
            )


            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            st.rerun()


    with quick3:

        if st.button(
            "🍽️ Dịch vụ",
            use_container_width=True
        ):

            question = "Khách sạn có những dịch vụ gì?"


            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )


            answer = chatbot_response(
                question
            )


            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            st.rerun()


    with quick4:

        if st.button(
            "📅 Đặt phòng",
            use_container_width=True
        ):

            question = "Tôi muốn đặt phòng."


            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )


            answer = chatbot_response(
                question
            )


            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            st.rerun()


    st.divider()


    # =====================================================
    # HIỂN THỊ LỊCH SỬ CHAT
    # =====================================================

    for message in st.session_state.chat_history:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # =====================================================
    # Ô CHAT
    # =====================================================

    user_message = st.chat_input(
        "Nhập câu hỏi cho Charm Pearl..."
    )


    if user_message:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_message
            }
        )


        answer = chatbot_response(
            user_message
        )


        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


        st.rerun()


    # NÚT XÓA CHAT

    if st.button(
        "🗑️ Xóa cuộc trò chuyện"
    ):

        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content":
                    "Xin chào! Tôi là trợ lý ảo "
                    "của Charm Pearl Hotel. "
                    "Tôi có thể hỗ trợ bạn về "
                    "phòng, giá và dịch vụ."
            }
        ]

        st.rerun()


# =========================================================
# 21. FOOTER
# =========================================================

st.divider()

st.caption(
    "© Charm Pearl Hotel · Vũng Tàu · "
    "Hotel Management System · 50 Rooms"
)
