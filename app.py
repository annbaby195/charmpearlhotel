import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pathlib import Path

# ============================================================
# CẤU HÌNH
# ============================================================

st.set_page_config(
    page_title="Charm Pearl Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE = Path(__file__).parent

HOTEL_NAME = "CHARM PEARL HOTEL"
LOCATION = "VŨNG TÀU"

# ============================================================
# FILE HÌNH ẢNH
# ============================================================

LOGO = BASE / "IMG_LOGO11.jpg"
BANNER = BASE / "IMG_BANNER2.jpg"
BACKGROUND = BASE / "IMG_NENCHIM3.jpg"

ROOM_IMAGES = {
    "Deluxe Room King": [
        BASE / "DELUXEROOMKING.jpg"
    ],

    "Deluxe Room Twins": [
        BASE / "DELUXEROOMTWINS.jpg"
    ],

    "Premier Garden": [
        BASE / "PREMIERGARDEN1.jpg",
        BASE / "PREMIERGARDEN2.jpg"
    ],

    "Premier Ocean": [
        BASE / "PREMIEROCEAN1.jpg",
        BASE / "PREMIEROCEAN2.jpg"
    ],

    "Princess Suite": [
        BASE / "PRINCESSSUITE1.jpg",
        BASE / "PRINCESSSUITE2.jpg"
    ],

    "Royal Suite Villa": [
        BASE / "ROYALSUITEVILLA1.jpg",
        BASE / "ROYALSUITEVILLA2.jpg",
        BASE / "ROYALSUITEVILLA3.jpg",
        BASE / "ROYALSUITEVILLA4.jpg"
    ]
}

# ============================================================
# THÔNG TIN HẠNG PHÒNG
# ============================================================

ROOM_TYPES = {
    "Deluxe Room King": {
        "price": 850000,
        "capacity": 2,
        "description": "Phòng giường King, phù hợp cho 1–2 khách."
    },

    "Deluxe Room Twins": {
        "price": 850000,
        "capacity": 2,
        "description": "Phòng 2 giường đơn, phù hợp cho bạn bè hoặc đồng nghiệp."
    },

    "Premier Garden": {
        "price": 1100000,
        "capacity": 2,
        "description": "Phòng hướng vườn, không gian nghỉ dưỡng yên tĩnh."
    },

    "Premier Ocean": {
        "price": 1300000,
        "capacity": 2,
        "description": "Phòng hướng biển, phù hợp cho kỳ nghỉ tại Vũng Tàu."
    },

    "Princess Suite": {
        "price": 1800000,
        "capacity": 3,
        "description": "Suite rộng rãi, phù hợp cho gia đình nhỏ hoặc nhóm khách."
    },

    "Royal Suite Villa": {
        "price": 3000000,
        "capacity": 4,
        "description": "Villa cao cấp, không gian riêng tư và rộng rãi."
    }
}

STATUSES = [
    "Trống",
    "Đã đặt",
    "Đang ở",
    "Đang dọn",
    "Bảo trì"
]

# ============================================================
# HÀM
# ============================================================

def money(value):
    return f"{int(value):,}".replace(",", ".") + " VNĐ"


def image_exists(path):
    return path.exists()


def get_first_image(room_type):
    images = ROOM_IMAGES.get(room_type, [])

    for image in images:
        if image.exists():
            return image

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


# ============================================================
# TẠO 50 PHÒNG
# ============================================================

def create_rooms():

    rooms = []

    room_distribution = [
        (1, 10, "Deluxe Room King"),
        (11, 20, "Deluxe Room Twins"),
        (21, 28, "Premier Garden"),
        (29, 36, "Premier Ocean"),
        (37, 44, "Princess Suite"),
        (45, 50, "Royal Suite Villa")
    ]

    counter = 1

    for start, end, room_type in room_distribution:

        for _ in range(start, end + 1):

            floor = ((counter - 1) // 10) + 1
            room_number = f"{floor}{((counter - 1) % 10) + 1:02d}"

            rooms.append({
                "Phòng": room_number,
                "Tầng": floor,
                "Loại phòng": room_type,
                "Giá": ROOM_TYPES[room_type]["price"],
                "Sức chứa": ROOM_TYPES[room_type]["capacity"],
                "Trạng thái": "Trống"
            })

            counter += 1

    return pd.DataFrame(rooms)


# ============================================================
# SESSION STATE
# ============================================================

if "rooms" not in st.session_state:
    st.session_state.rooms = create_rooms()

if "bookings" not in st.session_state:

    st.session_state.bookings = pd.DataFrame(
        columns=[
            "Mã booking",
            "Phòng",
            "Loại phòng",
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
        columns=["Mã", "Dịch vụ", "Đơn giá"]
    )

if "chat_messages" not in st.session_state:

    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content":
            "Xin chào! Tôi là trợ lý của Charm Pearl Hotel. "
            "Tôi có thể hỗ trợ bạn về phòng, giá phòng, đặt phòng, "
            "check-in, check-out và các dịch vụ của khách sạn."
        }
    ]


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f4f7f8;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #073247,
            #0b4a62,
            #08364b
        );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #123e52;
        letter-spacing: 2px;
        margin-top: 10px;
    }

    .hero-subtitle {
        text-align: center;
        color: #6c7e87;
        font-size: 16px;
        margin-bottom: 20px;
    }

    .info-box {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #e1e7ea;
        margin-bottom: 20px;
    }

    .room-title {
        font-size: 22px;
        font-weight: 700;
        color: #123e52;
    }

    .price {
        font-size: 20px;
        font-weight: 700;
        color: #b08028;
    }

    .small-text {
        color: #71818a;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# NỀN CHÌM
# ============================================================

if BACKGROUND.exists():

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
            linear-gradient(
                rgba(245,248,249,0.94),
                rgba(245,248,249,0.94)
            ),
            url("data:image/jpeg;base64,"""
        +
        __import__("base64").b64encode(
            BACKGROUND.read_bytes()
        ).decode()
        +
        """");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    if LOGO.exists():
        st.image(str(LOGO), width=95)

    st.markdown("## CHARM PEARL HOTEL")
    st.caption("HOTEL MANAGEMENT SYSTEM")

    st.divider()

    menu = st.radio(
        "MENU QUẢN LÝ",
        [
            "🏠 Tổng quan",
            "🛏️ Quản lý phòng",
            "📸 Hạng phòng",
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


# ============================================================
# TỔNG QUAN
# ============================================================

if menu == "🏠 Tổng quan":

    st.markdown(
        '<div class="hero-title">CHARM PEARL HOTEL</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Hotel Management System · Vũng Tàu'
        '</div>',
        unsafe_allow_html=True
    )

    if BANNER.exists():

        left, center, right = st.columns([1, 2.2, 1])

        with center:
            st.image(
                str(BANNER),
                use_container_width=True
            )

    rooms = st.session_state.rooms
    bookings = st.session_state.bookings

    total_rooms = len(rooms)

    available_rooms = len(
        rooms[rooms["Trạng thái"] == "Trống"]
    )

    reserved_rooms = len(
        rooms[rooms["Trạng thái"] == "Đã đặt"]
    )

    occupied_rooms = len(
        rooms[rooms["Trạng thái"] == "Đang ở"]
    )

    revenue = (
        bookings["Tổng tiền"].sum()
        if not bookings.empty
        else 0
    )

    st.subheader("Tổng quan khách sạn")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🏨 Tổng phòng", total_rooms)
    c2.metric("🟢 Phòng trống", available_rooms)
    c3.metric("🟣 Đã đặt", reserved_rooms)
    c4.metric("🔵 Đang ở", occupied_rooms)
    c5.metric("💰 Doanh thu", money(revenue))

    st.divider()

    st.subheader("Sơ đồ phòng")

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

    for index, (_, room) in enumerate(display_rooms.iterrows()):

        with columns[index % 5]:

            with st.container(border=True):

                st.markdown(
                    f"### 🛏️ {room['Phòng']}"
                )

                st.write(
                    room["Loại phòng"]
                )

                st.write(
                    money(room["Giá"]) + " / đêm"
                )

                st.write(
                    f"{status_icon(room['Trạng thái'])} "
                    f"{room['Trạng thái']}"
                )


# ============================================================
# HẠNG PHÒNG + HÌNH ẢNH
# ============================================================

elif menu == "📸 Hạng phòng":

    st.title("📸 Hạng phòng")

    st.write(
        "Khám phá các hạng phòng hiện có tại Charm Pearl Hotel."
    )

    for room_type, info in ROOM_TYPES.items():

        st.divider()

        st.subheader(room_type)

        images = [
            image for image in ROOM_IMAGES[room_type]
            if image.exists()
        ]

        if images:

            image_columns = st.columns(
                min(len(images), 4)
            )

            for i, image in enumerate(images):

                with image_columns[
                    i % len(image_columns)
                ]:

                    st.image(
                        str(image),
                        use_container_width=True
                    )

        else:

            st.info(
                "Chưa có hình ảnh cho hạng phòng này."
            )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Giá từ",
            money(info["price"])
        )

        c2.metric(
            "Sức chứa",
            f"{info['capacity']} khách"
        )

        c3.write(
            "**Mô tả**\n\n"
            + info["description"]
        )


# ============================================================
# QUẢN LÝ PHÒNG
# ============================================================

elif menu == "🛏️ Quản lý phòng":

    st.title("🛏️ Quản lý phòng")

    rooms = st.session_state.rooms

    c1, c2, c3 = st.columns(3)

    with c1:

        floor_filter = st.selectbox(
            "Tầng",
            ["Tất cả", 1, 2, 3, 4, 5]
        )

    with c2:

        type_filter = st.selectbox(
            "Hạng phòng",
            ["Tất cả"] + list(ROOM_TYPES.keys())
        )

    with c3:

        status_filter = st.selectbox(
            "Trạng thái",
            ["Tất cả"] + STATUSES
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

    with st.form("update_room"):

        room_number = st.selectbox(
            "Phòng",
            rooms["Phòng"].tolist()
        )

        new_status = st.selectbox(
            "Trạng thái mới",
            STATUSES
        )

        update = st.form_submit_button(
            "CẬP NHẬT",
            use_container_width=True
        )

    if update:

        st.session_state.rooms.loc[
            st.session_state.rooms["Phòng"] == room_number,
            "Trạng thái"
        ] = new_status

        st.success(
            f"Phòng {room_number} đã chuyển sang "
            f"trạng thái: {new_status}"
        )

        st.rerun()


# ============================================================
# ĐẶT PHÒNG
# ============================================================

elif menu == "📅 Đặt phòng":

    st.title("📅 Đặt phòng")

    st.info(
        "Chọn ngày lưu trú và hạng phòng. "
        "Hệ thống sẽ lọc những phòng có thể đặt."
    )

    c1, c2 = st.columns(2)

    with c1:

        check_in = st.date_input(
            "Ngày check-in",
            value=date.today()
        )

    with c2:

        check_out = st.date_input(
            "Ngày check-out",
            value=date.today() + timedelta(days=1)
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

        room_price = ROOM_TYPES[
            room_type
        ]["price"]

        room_capacity = ROOM_TYPES[
            room_type
        ]["capacity"]

        st.write(
            f"**{room_type}** · "
            f"{money(room_price)}/đêm · "
            f"Tối đa {room_capacity} khách"
        )

        # --------------------------------------------
        # KIỂM TRA PHÒNG ĐÃ BỊ BOOK TRÙNG NGÀY
        # --------------------------------------------

        suitable_rooms = st.session_state.rooms[
            st.session_state.rooms["Loại phòng"]
            == room_type
        ]

        available_rooms = []

        for _, room in suitable_rooms.iterrows():

            room_number = room["Phòng"]

            if room["Trạng thái"] == "Bảo trì":
                continue

            if room["Trạng thái"] == "Đang dọn":
                continue

            conflict = False

            bookings = st.session_state.bookings

            if not bookings.empty:

                room_bookings = bookings[
                    bookings["Phòng"] == room_number
                ]

                for _, booking in room_bookings.iterrows():

                    if booking["Trạng thái"] in [
                        "Đã trả phòng",
                        "Đã hủy"
                    ]:
                        continue

                    old_checkin = booking["Check-in"]
                    old_checkout = booking["Check-out"]

                    if (
                        check_in < old_checkout
                        and check_out > old_checkin
                    ):
                        conflict = True
                        break

            if not conflict:
                available_rooms.append(room_number)

        if not available_rooms:

            st.error(
                "Không còn phòng phù hợp trong khoảng thời gian này."
            )

        else:

            room = st.selectbox(
                "Chọn phòng",
                available_rooms
            )

            st.success(
                f"Có {len(available_rooms)} phòng "
                f"{room_type} có thể đặt."
            )

            c1, c2 = st.columns(2)

            with c1:

                guest_name = st.text_input(
                    "Họ tên khách *"
                )

                phone = st.text_input(
                    "Số điện thoại *"
                )

            with c2:

                guests = st.number_input(
                    "Số khách",
                    min_value=1,
                    max_value=room_capacity,
                    value=1
                )

                note = st.text_area(
                    "Ghi chú"
                )

            room_total = (
                room_price * nights
            )

            st.metric(
                "Tổng tiền phòng",
                money(room_total)
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

                    current_bookings = (
                        st.session_state.bookings
                    )

                    booking_number = (
                        len(current_bookings) + 1
                    )

                    booking_id = (
                        f"BK{booking_number:04d}"
                    )

                    new_booking = pd.DataFrame(
                        [{
                            "Mã booking": booking_id,
                            "Phòng": room,
                            "Loại phòng": room_type,
                            "Khách hàng": guest_name,
                            "Số điện thoại": phone,
                            "Số khách": guests,
                            "Check-in": check_in,
                            "Check-out": check_out,
                            "Số đêm": nights,
                            "Tiền phòng": room_total,
                            "Dịch vụ": 0,
                            "Tổng tiền": room_total,
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
                        st.session_state.rooms["Phòng"] == room,
                        "Trạng thái"
                    ] = "Đã đặt"

                    st.success(
                        f"Đặt phòng thành công! "
                        f"Mã booking: {booking_id}"
                    )

                    st.balloons()


# ============================================================
# CHECK-IN
# ============================================================

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
            "Mã booking",
            waiting["Mã booking"].tolist()
        )

        selected = waiting[
            waiting["Mã booking"] == booking_id
        ].iloc[0]

        st.subheader(
            f"Booking {booking_id}"
        )

        c1, c2, c3 = st.columns(3)

        c1.write(
            f"**Khách:** {selected['Khách hàng']}"
        )

        c2.write(
            f"**Phòng:** {selected['Phòng']}"
        )

        c3.write(
            f"**Hạng:** {selected['Loại phòng']}"
        )

        st.write(
            f"**Check-in:** {selected['Check-in']}"
        )

        st.write(
            f"**Check-out:** {selected['Check-out']}"
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


# ============================================================
# CHECK-OUT
# ============================================================

elif menu == "🚪 Check-out":

    st.title("🚪 Check-out")

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

        total = (
            selected["Tiền phòng"] + extra
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


# ============================================================
# KHÁCH HÀNG
# ============================================================

elif menu == "👥 Khách hàng":

    st.title("👥 Khách hàng")

    bookings = st.session_state.bookings

    if bookings.empty:

        st.info(
            "Chưa có dữ liệu khách hàng."
        )

    else:

        keyword = st.text_input(
            "🔎 Tìm khách hàng"
        )

        data = bookings.copy()

        if keyword:

            mask = data.astype(str).apply(
                lambda column:
                column.str.contains(
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


# ============================================================
# DỊCH VỤ
# ============================================================

elif menu == "🍽️ Dịch vụ":

    st.title("🍽️ Dịch vụ khách sạn")

    st.dataframe(
        st.session_state.services,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Thêm dịch vụ")

    with st.form("add_service"):

        c1, c2, c3 = st.columns(3)

        with c1:
            code = st.text_input("Mã dịch vụ")

        with c2:
            name = st.text_input("Tên dịch vụ")

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


# ============================================================
# HÓA ĐƠN
# ============================================================

elif menu == "🧾 Hóa đơn":

    st.title("🧾 Hóa đơn")

    bookings = st.session_state.bookings

    if bookings.empty:

        st.info(
            "Chưa có booking để lập hóa đơn."
        )

    else:

        booking_id = st.selectbox(
            "Chọn booking",
            bookings["Mã booking"].tolist()
        )

        invoice = bookings[
            bookings["Mã booking"] == booking_id
        ].iloc[0]

        st.divider()

        st.subheader(
            "CHARM PEARL HOTEL"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.write(
                f"**Mã booking:** {invoice['Mã booking']}"
            )

            st.write(
                f"**Khách hàng:** {invoice['Khách hàng']}"
            )

            st.write(
                f"**Số điện thoại:** {invoice['Số điện thoại']}"
            )

        with c2:

            st.write(
                f"**Phòng:** {invoice['Phòng']}"
            )

            st.write(
                f"**Check-in:** {invoice['Check-in']}"
            )

            st.write(
                f"**Check-out:** {invoice['Check-out']}"
            )

        st.divider()

        st.write(
            f"Tiền phòng: **{money(invoice['Tiền phòng'])}**"
        )

        st.write(
            f"Dịch vụ: **{money(invoice['Dịch vụ'])}**"
        )

        st.success(
            f"TỔNG THANH TOÁN: {money(invoice['Tổng tiền'])}"
        )


# ============================================================
# DOANH THU
# ============================================================

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

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Doanh thu phòng",
        money(room_revenue)
    )

    c2.metric(
        "Doanh thu dịch vụ",
        money(service_revenue)
    )

    c3.metric(
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


# ============================================================
# BÁO CÁO
# ============================================================

elif menu == "📊 Báo cáo":

    st.title("📊 Báo cáo khách sạn")

    rooms = st.session_state.rooms

    status_count = (
        rooms["Trạng thái"]
        .value_counts()
        .reindex(
            STATUSES,
            fill_value=0
        )
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Tổng phòng",
        len(rooms)
    )

    c2.metric(
        "Phòng trống",
        int(status_count["Trống"])
    )

    c3.metric(
        "Đang ở",
        int(status_count["Đang ở"])
    )

    c4.metric(
        "Bảo trì",
        int(status_count["Bảo trì"])
    )

    st.subheader("Tình trạng phòng")

    st.bar_chart(
        status_count
    )

    st.subheader("Danh sách 50 phòng")

    st.dataframe(
        rooms,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CHATBOX KHÁCH HÀNG
# ============================================================

elif menu == "💬 Chat với khách":

    st.title("💬 Trợ lý Charm Pearl Hotel")

    st.write(
        "Khu vực trò chuyện dành cho khách hàng."
    )

    st.info(
        "Khách có thể hỏi về giá phòng, hạng phòng, "
        "đặt phòng, check-in, check-out và dịch vụ."
    )

    # Hiển thị lịch sử chat

    for message in st.session_state.chat_messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    # Ô nhập chat

    prompt = st.chat_input(
        "Nhập câu hỏi của bạn..."
    )

    if prompt:

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        question = prompt.lower().strip()

        # ------------------------------------------
        # XỬ LÝ CÂU HỎI
        # ------------------------------------------

        if (
            "giá" in question
            or "bao nhiêu" in question
        ):

            response = (
                "Charm Pearl Hotel hiện có 6 hạng phòng:\n\n"
                + "\n".join(
                    [
                        f"- {name}: {money(info['price'])}/đêm"
                        for name, info
                        in ROOM_TYPES.items()
                    ]
                )
            )

        elif (
            "phòng" in question
            and (
                "còn" in question
                or "trống" in question
            )
        ):

            rooms = st.session_state.rooms

            available = rooms[
                rooms["Trạng thái"] == "Trống"
            ]

            if available.empty:

                response = (
                    "Hiện tại khách sạn không còn phòng trống."
                )

            else:

                counts = (
                    available["Loại phòng"]
                    .value_counts()
                )

                response = (
                    "Hiện tại Charm Pearl Hotel còn:\n\n"
                    + "\n".join(
                        [
                            f"- {room_type}: {count} phòng"
                            for room_type, count
                            in counts.items()
                        ]
                    )
                )

        elif (
            "check-in" in question
            or "check in" in question
        ):

            response = (
                "Thời gian check-in tiêu chuẩn "
                "là từ 14:00."
            )

        elif (
            "check-out" in question
            or "check out" in question
        ):

            response = (
                "Thời gian check-out tiêu chuẩn "
                "là trước 12:00."
            )

        elif (
            "dịch vụ" in question
            or "service" in question
        ):

            services = st.session_state.services

            response = (
                "Các dịch vụ hiện có:\n\n"
                + "\n".join(
                    [
                        f"- {row['Dịch vụ']}: "
                        f"{money(row['Đơn giá'])}"
                        for _, row
                        in services.iterrows()
                    ]
                )
            )

        elif (
            "deluxe" in question
            or "premier" in question
            or "princess" in question
            or "royal" in question
        ):

            matched = None

            for room_type in ROOM_TYPES:

                if room_type.lower() in question:

                    matched = room_type
                    break

            if matched:

                info = ROOM_TYPES[matched]

                response = (
                    f"**{matched}**\n\n"
                    f"Giá: {money(info['price'])}/đêm\n\n"
                    f"Sức chứa: {info['capacity']} khách\n\n"
                    f"{info['description']}"
                )

            else:

                response = (
                    "Charm Pearl Hotel hiện có 6 hạng phòng: "
                    "Deluxe Room King, Deluxe Room Twins, "
                    "Premier Garden, Premier Ocean, "
                    "Princess Suite và Royal Suite Villa."
                )

        elif (
            "đặt phòng" in question
            or "booking" in question
            or "đặt" in question
        ):

            response = (
                "Bạn có thể vào mục **📅 Đặt phòng** "
                "ở menu bên trái để chọn ngày, "
                "hạng phòng và thông tin khách."
            )

        elif (
            "xin chào" in question
            or "hello" in question
            or "hi" in question
            or "chào" in question
        ):

            response = (
                "Xin chào! Rất vui được hỗ trợ bạn "
                "tại Charm Pearl Hotel."
            )

        else:

            response = (
                "Tôi có thể hỗ trợ bạn về:\n\n"
                "• Giá phòng\n"
                "• Hạng phòng\n"
                "• Phòng còn trống\n"
                "• Đặt phòng\n"
                "• Check-in / Check-out\n"
                "• Dịch vụ khách sạn\n\n"
                "Bạn muốn hỏi thông tin nào?"
            )

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "© Charm Pearl Hotel · Vũng Tàu · "
    "Hotel Management System · 50 Rooms"
)
