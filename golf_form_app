import os
import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
# =========================
# 1. 기본 설정 및 파일 관리
# =========================
st.set_page_config(page_title="라운딩 신청 컨시어지", page_icon="⛳", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

SCHEDULE_FILE = os.path.join(DATA_DIR, "schedules.xlsx")
SUBMISSION_FILE = os.path.join(DATA_DIR, "submissions.xlsx")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.xlsx")
ADMIN_PASSWORD = "042200"

REQUIRED_COLS = ["month", "date", "time", "golf_club", "course", "status"]

# --- 커스텀 스타일 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #F8F9FA;
    }

    /* 제목 왼쪽 수직 바 스타일 */
    .section-title {
        border-left: 6px solid #1B4332; /* 골프 그린 색상 */
        padding-left: 15px;
        margin-top: 30px;
        margin-bottom: 20px;
        line-height: 1.2;
    }
    .section-title h3 {
        margin: 0 !important;
        padding: 0 !important;
        font-weight: 700 !important;
        color: #1A1C1E !important;
        font-size: 1.5rem !important;
    }
    /* 상단 슬림형 배너 스타일 */
    .header-banner {
        background: linear-gradient(135deg, #1B4332 0%, #2D3136 100%);
        padding: 20px 15px; /* 상하 패딩을 50px -> 20px로 축소 */
        border-radius: 16px; /* 모서리 곡률도 살짝 줄여서 날렵하게 */
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 20px; /* 배너와 아래 박스 사이 간격도 축소 */
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .header-banner h1 { 
        font-size: 1.6rem !important; /* 글자 크기를 3.6rem */
        font-weight: 700 !important; 
        margin: 0 !important; /* 제목 주변 불필요한 여백 제거 */
        letter-spacing: -0.05rem;
    }

    /* 카드 스타일링 */
    .stCard {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        border: 1px solid #E9ECEF;
        margin-bottom: 20px;
    }

    /* 입력 필드 레이블 스타일 */
    [data-testid="stTextLabel"] {
        font-weight: 600 !important;
        color: #495057 !important;
    }

    /* 버튼 스타일: 포레스트 그린 (골프 느낌) */
    .stButton>button {
        border-radius: 14px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
    }
    .stButton>button[kind="primary"] {
        background: #1B4332 !important; /* Deep Forest Green */
        color: white !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(27, 67, 50, 0.2);
    }

    /* 탭 메뉴 스타일링 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #F1F3F5;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 8px;
        padding: 8px 16px;
        background-color: transparent;
        border: none;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 2. 핵심 로직 함수
# =========================
def create_default_files():
    if not os.path.exists(SCHEDULE_FILE):
        pd.DataFrame(columns=REQUIRED_COLS).to_excel(SCHEDULE_FILE, index=False)

    if not os.path.exists(SUBMISSION_FILE):
        pd.DataFrame(
            columns=["submitted_at", "month", "name", "priority", "date", "time", "golf_club", "course"]
        ).to_excel(SUBMISSION_FILE, index=False)

    if not os.path.exists(SETTINGS_FILE):
        pd.DataFrame([{"deadline": "2026-03-31 23:59:59"}]).to_excel(SETTINGS_FILE, index=False)

    if not os.path.exists(SUBMISSION_FILE):
        pd.DataFrame(
            columns=["submitted_at", "month", "name", "priority", "date", "time", "golf_club", "course"]
        ).to_excel(SUBMISSION_FILE, index=False)

    if not os.path.exists(SETTINGS_FILE):
        pd.DataFrame([{"deadline": "2026-03-31 23:59:59"}]).to_excel(SETTINGS_FILE, index=False)


def get_deadline():
    create_default_files()
    df = pd.read_excel(SETTINGS_FILE)
    return pd.to_datetime(df.loc[0, "deadline"])


def update_deadline(new_date, new_time):
    new_dt = datetime.combine(new_date, new_time)
    pd.DataFrame([{"deadline": new_dt.strftime("%Y-%m-%d %H:%M:%S")}]).to_excel(SETTINGS_FILE, index=False)
    return new_dt


def load_schedule():
    create_default_files()
    df = pd.read_excel(SCHEDULE_FILE).fillna("").applymap(lambda x: str(x).strip())

    if "status" not in df.columns:
        df["status"] = "published"

    for col in REQUIRED_COLS:
        if col not in df.columns:
            df[col] = ""

    df["option_label"] = df["date"] + " | " + df["time"] + " | " + df["golf_club"] + " | " + df["course"]
    return df


def save_schedule(df):
    df.to_excel(SCHEDULE_FILE, index=False)


def add_schedule(month, date, time, golf_club, course, status="draft"):
    df = load_schedule().drop(columns=["option_label"], errors="ignore")

    new_row = pd.DataFrame([{
        "month": str(month).strip(),
        "date": str(date).strip(),
        "time": str(time).strip(),
        "golf_club": str(golf_club).strip(),
        "course": str(course).strip(),
        "status": str(status).strip()
    }])

    duplicate = (
        (df["date"].astype(str).str.strip() == str(date).strip()) &
        (df["time"].astype(str).str.strip() == str(time).strip()) &
        (df["golf_club"].astype(str).str.strip() == str(golf_club).strip()) &
        (df["course"].astype(str).str.strip() == str(course).strip())
    )

    if duplicate.any():
        return False, "동일한 스케줄이 이미 존재합니다."

    df = pd.concat([df, new_row], ignore_index=True)
    save_schedule(df)
    return True, "스케줄이 저장되었습니다."


def publish_schedule_by_index(idx):
    df = load_schedule().drop(columns=["option_label"], errors="ignore")

    if idx not in df.index:
        return False, "게시할 스케줄을 찾을 수 없습니다."

    df.loc[idx, "status"] = "published"
    save_schedule(df)
    return True, "스케줄이 게시되었습니다."


def delete_schedule_by_index(idx):
    df = load_schedule().drop(columns=["option_label"], errors="ignore")

    if idx not in df.index:
        return False, "삭제할 스케줄을 찾을 수 없습니다."

    df = df.drop(index=idx).reset_index(drop=True)
    save_schedule(df)
    return True, "스케줄이 삭제되었습니다."


def update_schedule_field(idx, field_name, new_value):
    df = load_schedule().drop(columns=["option_label"], errors="ignore")

    if idx not in df.index:
        return False, "수정할 스케줄을 찾을 수 없습니다."

    if field_name not in df.columns:
        return False, "수정 가능한 항목이 아닙니다."

    df.loc[idx, field_name] = str(new_value).strip()
    save_schedule(df)
    return True, f"{field_name} 항목이 수정되었습니다."

def load_submissions():
    return pd.read_excel(SUBMISSION_FILE).fillna("")


def save_submission(name, month, selected_rows):
    df_old = load_submissions()
    submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = [{"submitted_at": submitted_at, "month": month, "name": name, **item} for item in selected_rows]
    pd.concat([df_old, pd.DataFrame(new_data)], ignore_index=True).to_excel(SUBMISSION_FILE, index=False)


def delete_existing_submission(name, month):
    df = load_submissions()
    df = df[
        ~(
            (df["name"].astype(str).str.strip() == name.strip()) &
            (df["month"].astype(str).str.strip() == month.strip())
        )
    ]
    df.to_excel(SUBMISSION_FILE, index=False)


def get_existing_submission(name, month):
    df = load_submissions()
    return df[
        (df["name"].astype(str).str.strip() == name.strip()) &
        (df["month"].astype(str).str.strip() == month.strip())
    ]


def render_deadline_static(deadline_dt):
    deadline_str = deadline_dt.strftime("%Y년 %m월 %d일 %H:%M")
    is_closed = datetime.now() > deadline_dt

    status_color = "#E03131" if is_closed else "#1B4332"
    status_text = "⛔ 신청이 마감되었습니다" if is_closed else "✅ 지금은 신청 가능 기간입니다"

    html_code = f"""
    <div style="background: white; border: 1px solid #E9ECEF; border-radius: 20px; padding: 25px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.02); margin-bottom: 30px;">
        <div style="font-size: 0.95rem; color: #868E96; font-weight: 400; margin-bottom: 8px;">신청 제출 마감 일시</div>
        <div style="font-size: 1.6rem; font-weight: 700; color: #212529; margin-bottom: 12px; letter-spacing: -0.5px;">{deadline_str}</div>
        <div style="font-size: 0.9rem; font-weight: 600; color: {status_color}; background: {status_color}10; display: inline-block; padding: 6px 16px; border-radius: 50px;">
            {status_text}
        </div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def format_korean_date(date_value):
    weekday_map = ["월", "화", "수", "목", "금", "토", "일"]
    weekday = weekday_map[date_value.weekday()]
    return f"{date_value.month}/{date_value.day}({weekday})"


def get_course_options(golf_club):
    if golf_club == "오크힐스CC":
        return ["힐코스", "브릿지코스"]
    elif golf_club == "플라자CC":
        return ["타이거코스(OUT)", "타이거코스(IN)", "라이온코스(OUT)", "라이온코스(IN)"]
    return []

    st.markdown(html_code, unsafe_allow_html=True)

def update_schedule_status(idx, is_published):
    df = load_schedule().drop(columns=["option_label"], errors="ignore")

    if idx not in df.index:
        return False, "해당 스케줄을 찾을 수 없습니다."

    df.loc[idx, "status"] = "published" if is_published else "draft"
    save_schedule(df)
    return True, "상태가 변경되었습니다."

# =========================
# 3. 메인 화면 구성
# =========================
schedule_df = load_schedule()
schedule_df = schedule_df[schedule_df["status"] == "published"].reset_index(drop=True)

current_month = schedule_df["month"].iloc[0] if not schedule_df.empty else "이번 달"
deadline_dt = get_deadline()
is_closed = datetime.now() > deadline_dt 

# 타이틀 배너
st.markdown(f'''
<div class="header-banner">
    <h1>⛳{current_month} 라운딩 신청 폼</h1>
</div>
''', unsafe_allow_html=True)

# [수정] 카운트다운 대신 정적 날짜 카드 표시
render_deadline_static(deadline_dt)

if is_closed:
    st.error("⏳ 설정된 신청 마감 시간이 지났습니다. 신규 신청 및 수정이 불가능합니다.")

# 라운딩 일정 리스트
st.markdown('<div class="section-title"><h3> 라운딩 일정 리스트</h3></div>', unsafe_allow_html=True)
with st.container():
    disp_df = schedule_df[["date", "time", "golf_club", "course"]].copy()
    disp_df.columns = ["날짜", "시간", "골프장", "코스"]

    # 번호 컬럼 추가
    st.dataframe(
        disp_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "날짜": st.column_config.TextColumn("날짜", width="small"),
            "시간": st.column_config.TextColumn("시간", width="small"),
            "골프장": st.column_config.TextColumn("골프장", width="medium"),
            "코스": st.column_config.TextColumn("코스", width="medium"),
        }
    )

# 신청 폼 카드
st.markdown('<div class="section-title"><h3> 라운딩 신청 폼</h3></div>', unsafe_allow_html=True)
with st.container():
    name = st.text_input("신청자 성함", placeholder="본명을 입력해주세요", disabled=is_closed)

    if name.strip():
        existing = get_existing_submission(name.strip(), current_month)
        if not existing.empty:
            st.info(f"✨ {name}님, 기존 신청 내역이 존재합니다. 다시 제출하면 최신 정보로 업데이트됩니다.")
            st.dataframe(existing[["priority", "date", "time", "golf_club", "course"]].sort_values("priority"), 
                         use_container_width=True, hide_index=True)

    all_options = schedule_df["option_label"].tolist()
    blank_option = "🏁 일정을 선택하세요"

    c1, c2, c3 = st.columns(3)
    with c1: rank1 = st.selectbox("1순위 희망", [blank_option] + all_options, disabled=is_closed)
    with c2: rank2 = st.selectbox("2순위 희망", [blank_option] + [o for o in all_options if o != rank1], disabled=is_closed)
    with c3: rank3 = st.selectbox("3순위 희망", [blank_option] + [o for o in all_options if o not in [rank1, rank2]], disabled=is_closed)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 신청서 제출하기", use_container_width=True, type="primary", disabled=is_closed):
    clean_name = name.strip()
    if not clean_name:
        st.error("신청자 성함을 입력해 주세요.")
    elif any(r == blank_option for r in [rank1, rank2, rank3]):
        st.error("1순위부터 3순위까지 희망 일정을 모두 선택해 주세요.")
    else:
        label_to_row = {r["option_label"]: r.to_dict() for _, r in schedule_df.iterrows()}
        selected_rows = [
            {"priority": "1순위", **label_to_row[rank1]},
            {"priority": "2순위", **label_to_row[rank2]},
            {"priority": "3순위", **label_to_row[rank3]},
        ]
        delete_existing_submission(clean_name, current_month)
        save_submission(clean_name, current_month, selected_rows)
        st.success(f"🎊 {clean_name}님, 라운딩 신청이 완료되었습니다. 행운을 빕니다!")
        st.balloons()

# =========================
# 4. 관리자 모드
# =========================
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
with st.expander("🔐 관리자 시스템 (Admin Only)"):

    # 세션 상태 초기화
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    # -------------------------
    # 1) 로그인 전
    # -------------------------
    if not st.session_state.admin_auth:
        admin_pw = st.text_input("Access Password", type="password", key="admin_login_pw")
        if st.button("로그인", use_container_width=True, key="admin_login_btn"):
            if admin_pw == ADMIN_PASSWORD:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("비밀번호가 일치하지 않습니다.")

    # -------------------------
    # 2) 로그인 후
    # -------------------------
    else:
        ac1, ac2 = st.columns([4, 1])
        with ac1:
            st.markdown("#### 접수 현황")
        with ac2:
            if st.button("로그아웃", use_container_width=True, key="admin_logout_btn"):
                st.session_state.admin_auth = False
                st.rerun()

        # =========================
        # 현황 리포트
        # =========================
        subs = load_submissions()

        if subs.empty:
            st.info("현재 접수된 신청 데이터가 없습니다.")
        else:
            tab1, tab2 = st.tabs(["전체 제출 내역", "일정별 신청 현황"])

            with tab1:
                show_sub_df = subs.copy()
                expected_cols = ["submitted_at", "month", "name", "priority", "date", "time", "golf_club", "course"]
                existing_cols = [c for c in expected_cols if c in show_sub_df.columns]
                show_sub_df = show_sub_df[existing_cols]

                if len(existing_cols) == 8:
                    show_sub_df.columns = ["제출시각", "월", "이름", "순위", "날짜", "시간", "골프장명", "코스"]

                st.dataframe(show_sub_df, use_container_width=True, hide_index=True)

                with open(SUBMISSION_FILE, "rb") as f:
                    st.download_button(
                        label="📥 제출 결과 엑셀 다운로드",
                        data=f,
                        file_name=f"golf_submissions_{datetime.now().strftime('%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        key="download_submission_excel"
                    )

            with tab2:
                grouped = subs.groupby(["date", "time", "golf_club", "course"], sort=False)

                for (date, time, golf_club, course), group in grouped:
                    st.markdown(f"**📍 {date} | {time} | {golf_club} | {course}**")

                    priority_order = {"1순위": 1, "2순위": 2, "3순위": 3}
                    view_df = group[["name", "priority"]].copy()
                    view_df.columns = ["이름", "순위"]
                    view_df["정렬순서"] = view_df["순위"].map(priority_order)
                    view_df = view_df.sort_values(["정렬순서", "이름"]).drop(columns=["정렬순서"])

                    p1 = (group["priority"] == "1순위").sum()
                    p2 = (group["priority"] == "2순위").sum()
                    p3 = (group["priority"] == "3순위").sum()

                    st.caption(f"총 {len(group)}명 (1순위: {p1} / 2순위: {p2} / 3순위: {p3})")
                    st.dataframe(view_df, use_container_width=True, hide_index=True)
                    st.markdown("---")

        st.markdown("<br><br>", unsafe_allow_html=True)

        # =========================
        # 데이터 초기화
        # =========================
        with st.expander("🧨 데이터 초기화"):
            st.warning("이 작업은 되돌릴 수 없습니다.")
            if st.checkbox("삭제에 동의하며, 모든 데이터를 초기화합니다.", key="reset_confirm_check"):
                if st.button("데이터 리셋 실행", type="secondary", use_container_width=True, key="reset_data_btn"):
                    subs = load_submissions()
                    empty_df = pd.DataFrame(columns=subs.columns)
                    empty_df.to_excel(SUBMISSION_FILE, index=False)
                    st.toast("데이터가 초기화되었습니다.")
                    st.rerun()

        # =========================
        # 상단 관리자 탭
        # =========================
        admin_tab1, admin_tab2 = st.tabs(["⏰ 마감 기한 조정", "🗂️ 스케줄 관리"])

        # =========================
        # 탭 1) 마감 기한 조정
        # =========================
        with admin_tab1:
            st.markdown("##### ⏰ 마감 기한 조정")

            col_date, col_time = st.columns(2)
            new_d = col_date.date_input("마감 날짜", deadline_dt.date(), key="admin_deadline_date")
            new_t = col_time.time_input("마감 시간", deadline_dt.time(), key="admin_deadline_time")

            if st.button("설정 저장", use_container_width=True, key="save_deadline_btn"):
                update_deadline(new_d, new_t)
                st.toast("마감 기한이 업데이트되었습니다.")
                st.rerun()

        # =========================
        # 탭 2) 스케줄 관리
        # =========================
        with admin_tab2:
            st.markdown("##### 현재 스케줄")
            schedule_manage_df = load_schedule().drop(columns=["option_label"], errors="ignore")

            if schedule_manage_df.empty:
                st.info("등록된 스케줄이 없습니다.")
            else:
                view_df = schedule_manage_df.copy()

                # status -> 토글용 boolean 변환
                view_df["게시"] = view_df["status"].apply(lambda x: True if str(x).strip() == "published" else False)

                # 표시용 컬럼만 정리
                editor_df = view_df[["month", "date", "time", "golf_club", "course", "게시"]].copy()
                editor_df.columns = ["월", "날짜", "시간", "골프장", "코스", "게시"]

                edited_df = st.data_editor(
                    editor_df,
                    use_container_width=True,
                    hide_index=False,
                    column_config={
                        "월": st.column_config.TextColumn("월", disabled=True),
                        "날짜": st.column_config.TextColumn("날짜", disabled=True),
                        "시간": st.column_config.TextColumn("시간", disabled=True),
                        "골프장": st.column_config.TextColumn("골프장", disabled=True),
                        "코스": st.column_config.TextColumn("코스", disabled=True),
                        "게시": st.column_config.CheckboxColumn("게시", help="ON = 게시됨 / OFF = 보류중"),
                    },
                    key="schedule_status_editor"
                )

                if st.button("게시 상태 저장", use_container_width=True, key="save_status_toggle_btn"):
                    original_df = schedule_manage_df.copy().reset_index(drop=True)
                    changed = False

                    for i in range(len(edited_df)):
                        new_is_published = bool(edited_df.loc[i, "게시"])
                        new_status = "published" if new_is_published else "draft"

                        if str(original_df.loc[i, "status"]).strip() != new_status:
                            original_df.loc[i, "status"] = new_status
                            changed = True

                    if changed:
                        save_schedule(original_df)
                        st.success("게시 상태가 업데이트되었습니다.")
                        st.rerun()
                    else:
                        st.info("변경된 상태가 없습니다.")

            tab_s1, tab_s2 = st.tabs([
                "스케줄 추가",
                "스케줄 삭제"
            ])

            with tab_s1:
                st.markdown("###### ➕ 스케줄 추가")

                c1, c2 = st.columns(2)

                # 날짜 선택
                add_date_obj = c1.date_input("일자", key="add_date_obj")

                weekday_map = ["월", "화", "수", "목", "금", "토", "일"]
                weekday = weekday_map[add_date_obj.weekday()]

                add_month = f"{add_date_obj.month}월"
                add_date = f"{add_date_obj.month}/{add_date_obj.day}({weekday})"

                # 시간 입력
                add_time = c2.text_input(
                    "시간",
                    placeholder="예: 07:12",
                    key="add_time"
                )

                c3, c4 = st.columns(2)

                # 골프장 선택
                add_golf = c3.selectbox(
                    "골프장",
                    ["오크힐스CC", "플라자CC"],
                    key="add_golf"
                )

                # 골프장별 코스 선택
                if add_golf == "오크힐스CC":
                    course_options = ["힐코스", "브릿지코스"]
                else:
                    course_options = [
                        "타이거코스(OUT)",
                        "타이거코스(IN)",
                        "라이온코스(OUT)",
                        "라이온코스(IN)"
                    ]

                add_course = c4.selectbox(
                    "코스",
                    course_options,
                    key="add_course"
                )

                if st.button("스케줄 저장", use_container_width=True, key="btn_add_schedule"):

                    if not all([add_month, add_date, add_time, add_golf, add_course]):
                        st.warning("모든 항목을 입력해 주세요.")

                    else:
                        ok, msg = add_schedule(
                            add_month,
                            add_date,
                            add_time.strip(),
                            add_golf,
                            add_course,
                            status="draft"
                        )

                        if ok:
                            st.success("스케줄이 저장되었습니다. (보류 상태)")
                            st.rerun()
                        else:
                            st.error(msg)
            with tab_s2:
                st.markdown("###### 🗑️ 스케줄 삭제")

                if schedule_manage_df.empty:
                    st.info("삭제할 스케줄이 없습니다.")
                else:
                    delete_options = schedule_manage_df.apply(
                        lambda x: f"{x.name} | {x['month']} | {x['date']} | {x['time']} | {x['golf_club']} | {x['course']}",
                        axis=1
                    ).tolist()

                    selected_delete = st.selectbox(
                        "삭제할 스케줄 선택",
                        delete_options,
                        key="delete_schedule_select"
                    )

                    if st.button("선택 스케줄 삭제", use_container_width=True, key="btn_delete_schedule"):
                        delete_idx = int(selected_delete.split("|")[0].strip())
                        ok, msg = delete_schedule_by_index(delete_idx)

                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
