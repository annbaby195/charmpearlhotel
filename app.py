import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pathlib import Path
import base64

# =========================================================
# 1. CẤU HÌNH
# =========================================================

st.set_page_config(
    page_title="Charm Pearl Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE = Path(__file__).parent

LOGO = BASE / "IMG_LOGO1.jpg"
BANNER = BASE / "IMG_BANNER2.jpg"
BG = BASE / "IMG_NENCHIM3.jpg"

HOTEL = "CHARM PEARL HOTEL"
LOCATION = "VŨNG TÀU"

# =========================================================
# 2. HÀM
# =========================================================

def money(x):
    return f"{int(x):,}".replace(",", ".") + " VNĐ"


def image_ok(path):
    return path.exists()


def status_icon(status):
    return {
        "Trống": "🟢",
        "Đã đặt": "🟣",
        "Đang ở": "🔵",
        "Đang dọn": "🟡",
        "Bảo trì": "🔴"
    }.get(status, "⚪")


ROOM_TYPES = {
    "Standard": {"price": 550000, "capacity": 2},
    "Deluxe": {"price": 750000, "capacity": 2},
    "Suite": {"price": 1200000, "capacity": 3},
    "Family": {"price": 1500000, "capacity": 4}
}

STATUSES = [
    "Trống",
    "Đã đặt",
    "Đang ở",
    "Đang dọn",
    "Bảo trì"
]


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
# 3. SESSION
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

    st.session_state.services = pd.DataFrame([
        ["DV001", "Ăn sáng", 100000],
        ["DV002", "Cà phê", 45000],
        ["DV003", "Giặt ủi", 80000],
        ["DV004", "Minibar", 60000],
        ["DV005", "Extra Bed", 200000],
        ["DV006", "Spa", 300000],
        ["DV007", "Đưa đón sân bay", 350000]
    ], columns=["Mã", "Dịch vụ", "Đơn giá"])


# =========================================================
# 4. CSS - GIAO DIỆN MỚI
# =========================================================

st.markdown("""
<style>

.stApp {
    font-family: Arial, sans-serif;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #082c3c 0%,
        #0d4558 55%,
        #123f4e 100%
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* LOGO */

.logo-small img {
    border-radius: 12px;
}

/* HERO */

.hero {
    background: rgba(255,255,255,0.94);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 25px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.08);
    text-align: center;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    color: #123c4c;
    letter-spacing: 2px;
}

.hero-sub {
    color: #70828b;
    font-size: 16px;
}

/* DASHBOARD CARD */

.card {
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 3px 15px rgba(0,0,0,0.07);
    min-height: 115px;
}

.card-title {
    color: #72828a;
    font-size: 14px;
}

.card-number {
    color: #123c4c;
    font-size: 29px;
    font-weight: 800;
    margin-top: 8px;
}

/* ROOM */

.room {
    background: rgba(255,255,255,0.96);
    border-radius: 15px;
    padding: 14px;
    margin-bottom: 12px;
    border: 1px solid #e4e9ec;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.room-number {
    font-size: 22px;
    font-weight: 800;
    color: #143d4d;
}

.room-type {
    color: #71828a;
    font-size: 13px;
}

.room-status {
    margin-top: 8px;
    font-weight: 600;
}

/* SECTION */

.section {
    font-size: 25px;
    font-weight: 800;
    color: #143d4d;
    margin-top: 20px;
    margin-bottom: 15px;
}

/* BUTTON */

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 5. NỀN CHÌM
# =========================================================

if image_ok(BG):

    encoded = base64.b64encode(
        BG.read_bytes()
    ).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
            linear-gradient(
                rgba(245,248,249,0.93),
                rgba(245,248,249,0.93)
            ),
            url("data:image/jpeg;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 6. SIDEBAR
# =========================================================

with st.sidebar:

    # LOGO NHỎ BÊN TRÁI
    if image_ok(LOGO):

        st.image(
            str(LOGO),
            width=90
        )

    st.markdown("## CHARM PEARL")
    st.caption("HOTEL MANAGEMENT SYSTEM")

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
            "📊 Báo cáo"
        ]
    )

    st.divider()

    st.caption("CHARM PEARL HOTEL")
    st.caption("Vũng Tàu")
    st.caption("50 phòng · 5 tầng")


# =========================================================
# 7. DASHBOARD
# =========================================================

if menu == "🏠 Dashboard":

    # HERO
    st.markdown(
        '<div class="hero">'
        '<div class="hero-title">CHARM PEARL HOTEL</div>'
        '<div class="hero-sub">'
        'Hotel Management System · Vũng Tàu'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # BANNER Ở GIỮA
    if image_ok(BANNER):

        left, center, right = st.columns([1, 2.4, 1])

        with center:

            st.image(
                str(BANNER),
                use_container_width=True
            )

    st.markdown(
        '<div class="section">Tổng quan khách sạn</div>',
        unsafe_allow_html=True
    )

    rooms = st.session_state.rooms
    bookings = st.session_state.bookings

    total = len(rooms)

    empty = len(
        rooms[rooms["Trạng thái"] == "Trống"]
    )

    reserved = len(
        rooms[rooms["Trạng thái"] == "Đã đặt"]
    )

    occupied = len(
        rooms[rooms["Trạng thái"] == "Đang ở"]
    )

    revenue = (
        0
        if bookings.empty
        else bookings["Tổng tiền"].sum()
    )

    cards = st.columns(5)

    values = [
        ("🏨", "Tổng phòng", total),
        ("🟢", "Phòng trống", empty),
        ("🟣", "Đã đặt", reserved),
        ("🔵", "Đang ở", occupied),
        ("💰", "Doanh thu", money(revenue))
    ]

    for col, item in zip(cards, values):

        with col:

            st.markdown(
                f"""
                <div class="card">
                    <div class="card-title">
                        {item[0]} {item[1]}
                    </div>
                    <div class="card-number">
                        {item[2]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="section">Sơ đồ 50 phòng</div>',
        unsafe_allow_html=True
    )

    floor = st.selectbox(
        "Chọn tầng",
        ["Tất cả", 1, 2, 3, 4, 5]
    )

    if floor == "Tất cả":
        show_rooms = rooms
    else:
        show_rooms = rooms[
            rooms["Tầng"] == floor
        ]

    cols = st.columns(5)

    for index, (_, room) in enumerate(
        show_rooms.iterrows()
    ):

        with cols[index % 5]:

            st.markdown(
                f"""
                <div class="room">

                    <div class="room-number">
                        🛏️ {room["Phòng"]}
                    </div>

                    <div class="room-type">
                        {room["Loại phòng"]}
                        · Tầng {room["Tầng"]}
                    </div>

                    <div>
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
# 8. QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Phòng":

    st.title("🛏️ Quản lý phòng")

    rooms = st.session_state.rooms

    c1, c2, c3 = st.columns(3)

    with c1:

        floor = st.selectbox(
            "Tầng",
            ["Tất cả", 1, 2, 3, 4, 5]
        )

    with c2:

        room_type = st.selectbox(
            "Loại phòng",
            ["Tất cả"] + list(ROOM_TYPES.keys())
        )

    with c3:

        status = st.selectbox(
            "Trạng thái",
            ["Tất cả"] + STATUSES
        )

    result = rooms.copy()

    if floor != "Tất cả":
        result = result[result["Tầng"] == floor]

    if room_type != "Tất cả":
        result = result[
            result["Loại phòng"] == room_type
        ]

    if status != "Tất cả":
        result = result[
            result["Trạng thái"] == status
        ]

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Cập nhật trạng thái")

    with st.form("room_status"):

        room = st.selectbox(
            "Phòng",
            rooms["Phòng"].tolist()
        )

        new_status = st.selectbox(
            "Trạng thái mới",
            STATUSES
        )

        submit = st.form_submit_button(
            "CẬP NHẬT",
            use_container_width=True
        )

    if submit:

        st.session_state.rooms.loc[
            st.session_state.rooms["Phòng"] == room,
            "Trạng thái"
        ] = new_status

        st.success(
            f"Phòng {room}: {new_status}"
        )

        st.rerun()


# =========================================================
# 9. ĐẶT PHÒNG
# =========================================================

elif menu == "📅 Đặt phòng":

    st.title("📅 Đặt phòng")

    c1, c2 = st.columns(2)

    with c1:

        check_in = st.date_input(
            "Ngày check-in",
            date.today()
        )

    with c2:

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
            "Loại phòng",
            list(ROOM_TYPES.keys())
        )

        suitable = st.session_state.rooms[
            st.session_state.rooms["Loại phòng"]
            == room_type
        ]

        available = []

        for _, r in suitable.iterrows():

            if r["Trạng thái"] in [
                "Bảo trì",
                "Đang dọn"
            ]:
                continue

            available.append(r["Phòng"])

        if not available:

            st.error(
                "Không còn phòng phù hợp."
            )

        else:

            room = st.selectbox(
                "Chọn phòng",
                available
            )

            st.success(
                f"Còn {len(available)} phòng "
                f"{room_type}."
            )

            c1, c2 = st.columns(2)

            with c1:

                guest = st.text_input(
                    "Tên khách *"
                )

                phone = st.text_input(
                    "Số điện thoại *"
                )

            with c2:

                capacity = ROOM_TYPES[
                    room_type
                ]["capacity"]

                guests = st.number_input(
                    "Số khách",
                    1,
                    capacity,
                    1
                )

                note = st.text_area(
                    "Ghi chú"
                )

            price = ROOM_TYPES[
                room_type
            ]["price"]

            total = price * nights

            st.info(
                f"Phòng {room} · "
                f"{nights} đêm · "
                f"Tổng {money(total)}"
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

                    old = st.session_state.bookings

                    number = len(old) + 1

                    booking_id = (
                        f"BK{number:04d}"
                    )

                    new = pd.DataFrame([{
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
                    }])

                    st.session_state.bookings = pd.concat(
                        [
                            st.session_state.bookings,
                            new
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


# =========================================================
# 10. CHECK-IN
# =========================================================

elif menu == "🛎️ Check-in":

    st.title("🛎️ Check-in")

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
            waiting["Mã booking"]
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
# 11. CHECK-OUT
# =========================================================

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
            staying["Mã booking"]
        )

        selected = staying[
            staying["Mã booking"] == booking_id
        ].iloc[0]

        extra = st.number_input(
            "Dịch vụ phát sinh",
            0,
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
# 12. KHÁCH HÀNG
# =========================================================

elif menu == "👥 Khách hàng":

    st.title("👥 Khách hàng")

    bookings = st.session_state.bookings

    if bookings.empty:

        st.info(
            "Chưa có dữ liệu khách hàng."
        )

    else:

        keyword = st.text_input(
            "🔎 Tìm kiếm"
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
# 13. DỊCH VỤ
# =========================================================

elif menu == "🍽️ Dịch vụ":

    st.title("🍽️ Dịch vụ khách sạn")

    st.dataframe(
        st.session_state.services,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Thêm dịch vụ")

    with st.form("service_form"):

        c1, c2, c3 = st.columns(3)

        with c1:
            code = st.text_input("Mã dịch vụ")

        with c2:
            name = st.text_input("Tên dịch vụ")

        with c3:
            price = st.number_input(
                "Đơn giá",
                0,
                step=10000
            )

        submit = st.form_submit_button(
            "THÊM DỊCH VỤ",
            use_container_width=True
        )

    if submit and code and name:

        new = pd.DataFrame(
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
                new
            ],
            ignore_index=True
        )

        st.success(
            "Đã thêm dịch vụ."
        )

        st.rerun()


# =========================================================
# 14. HÓA ĐƠN
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
            "Chọn booking",
            bookings["Mã booking"]
        )

        invoice = bookings[
            bookings["Mã booking"]
            == booking_id
        ].iloc[0]

        st.markdown(
            f"""
            ### CHARM PEARL HOTEL

            **Mã booking:** {invoice["Mã booking"]}

            **Khách hàng:** {invoice["Khách hàng"]}

            **Phòng:** {invoice["Phòng"]}

            **Check-in:** {invoice["Check-in"]}

            **Check-out:** {invoice["Check-out"]}

            ---

            **Tiền phòng:** {money(invoice["Tiền phòng"])}

            **Dịch vụ:** {money(invoice["Dịch vụ"])}

            ### TỔNG: {money(invoice["Tổng tiền"])}
            """
        )


# =========================================================
# 15. DOANH THU
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

    total = (
        room_revenue
        + service_revenue
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Doanh thu phòng",
        money(room_revenue)
    )

    c2.metric(
        "Dịch vụ",
        money(service_revenue)
    )

    c3.metric(
        "Tổng doanh thu",
        money(total)
    )

    chart = pd.DataFrame({
        "Khoản thu": [
            "Phòng",
            "Dịch vụ"
        ],
        "Doanh thu": [
            room_revenue,
            service_revenue
        ]
    })

    st.bar_chart(
        chart.set_index("Khoản thu")
    )


# =========================================================
# 16. BÁO CÁO
# =========================================================

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

    st.bar_chart(
        status_count
    )

    st.subheader(
        "Danh sách phòng"
    )

    st.dataframe(
        rooms,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "© Charm Pearl Hotel · Vũng Tàu · "
    "Hotel Management System · 50 Rooms"
)
