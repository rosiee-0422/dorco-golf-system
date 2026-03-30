import os
import datetime as _dt
import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# ═══════════════════════════════════════════
# 1. 기본 설정
# ═══════════════════════════════════════════
st.set_page_config(
    page_title="라운딩 신청",
    page_icon="⛳",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ADMIN_PASSWORD = "042200"
REQUIRED_COLS  = ["month", "date", "time", "golf_club", "course", "status"]

# ═══════════════════════════════════════════
# 2. Supabase 연결
# ═══════════════════════════════════════════
@st.cache_resource
def get_supabase() -> Client:
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )

# ═══════════════════════════════════════════
# 3. CSS
# ═══════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400&display=swap');
:root{--bg:#f7f5f0;--surface:#fff;--green-d:#1a3228;--green-m:#2d5040;--gold:#b8963e;--gold-l:#d4af6a;--text:#1a1a18;--sub:#6b6b60;--hint:#a8a89a;--border:#e4e0d8;--danger:#8c3030;--success:#2d5040;}
*,*::before,*::after{box-sizing:border-box;}
html,body,[data-testid="stApp"],.stApp{font-family:'DM Sans',sans-serif!important;background:var(--bg)!important;color:var(--text)!important;}
header[data-testid="stHeader"],div[data-testid="stDecoration"],div[data-testid="stToolbar"]{display:none!important;}
.block-container{padding-top:2rem!important;padding-bottom:4rem!important;max-width:720px!important;}
.golf-hero{background:var(--green-d);border-radius:20px;padding:44px 40px 36px;margin-bottom:32px;position:relative;overflow:hidden;}
.golf-hero::before{content:'⛳';position:absolute;right:32px;top:50%;transform:translateY(-50%);font-size:72px;opacity:.12;line-height:1;}
.golf-hero .eyebrow{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-l);margin-bottom:10px;}
.golf-hero h1{font-family:'Cormorant Garamond',serif;font-size:2.4rem;font-weight:300;color:#fff;margin:0 0 6px;letter-spacing:-.01em;line-height:1.15;}
.golf-hero .sub{font-size:13px;color:rgba(255,255,255,.45);margin:0;font-weight:300;}
.deadline-card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:24px 28px;margin-bottom:28px;display:flex;align-items:center;justify-content:space-between;gap:16px;}
.deadline-card .dl-label{font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--hint);margin-bottom:4px;}
.deadline-card .dl-date{font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:400;color:var(--text);letter-spacing:-.01em;}
.deadline-card .dl-badge-open{background:rgba(45,80,64,.1);color:var(--green-m);border:1px solid rgba(45,80,64,.2);font-size:12px;font-weight:600;padding:6px 16px;border-radius:100px;white-space:nowrap;}
.deadline-card .dl-badge-closed{background:rgba(140,48,48,.08);color:var(--danger);border:1px solid rgba(140,48,48,.2);font-size:12px;font-weight:600;padding:6px 16px;border-radius:100px;white-space:nowrap;}
.sec-heading{font-family:'Cormorant Garamond',serif;font-size:1.4rem;font-weight:400;color:var(--text);letter-spacing:-.01em;margin:36px 0 16px;padding-bottom:10px;border-bottom:1px solid var(--border);}
.sec-heading span{font-family:'DM Mono',monospace;font-size:11px;font-weight:400;color:var(--gold);letter-spacing:.12em;text-transform:uppercase;vertical-align:middle;margin-right:10px;}
.closed-banner{background:rgba(140,48,48,.07);border:1px solid rgba(140,48,48,.18);border-radius:12px;padding:14px 20px;color:var(--danger);font-size:13px;font-weight:500;margin-bottom:20px;}
[data-testid="stTextInput"] input,[data-testid="stSelectbox"] div[data-baseweb="select"]>div,[data-testid="stDateInput"] input,[data-testid="stTextArea"] textarea{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:10px!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;font-size:14px!important;}
[data-testid="stTextInput"] label,[data-testid="stSelectbox"] label,[data-testid="stDateInput"] label{font-size:12px!important;font-weight:600!important;letter-spacing:.05em!important;text-transform:uppercase!important;color:var(--sub)!important;}
.stButton>button{border-radius:10px!important;font-family:'DM Sans',sans-serif!important;font-weight:500!important;font-size:14px!important;border:1px solid var(--border)!important;background:var(--surface)!important;color:var(--sub)!important;height:40px!important;}
.stButton>button:hover{border-color:var(--green-m)!important;color:var(--green-m)!important;}
[data-testid="stFormSubmitButton"] button{background:var(--green-d)!important;border:none!important;color:#fff!important;font-weight:600!important;height:48px!important;}
[data-testid="stFormSubmitButton"] button:hover{background:var(--green-m)!important;transform:translateY(-1px)!important;}
[data-testid="stSuccess"]{background:rgba(45,80,64,.07)!important;border:1px solid rgba(45,80,64,.2)!important;border-radius:10px!important;color:var(--success)!important;}
[data-testid="stError"]{background:rgba(140,48,48,.07)!important;border:1px solid rgba(140,48,48,.2)!important;border-radius:10px!important;color:var(--danger)!important;}
[data-testid="stWarning"]{background:rgba(184,150,62,.08)!important;border:1px solid rgba(184,150,62,.22)!important;border-radius:10px!important;color:#7a6020!important;}
[data-testid="stInfo"]{background:rgba(26,50,40,.05)!important;border:1px solid rgba(26,50,40,.12)!important;border-radius:10px!important;color:var(--green-d)!important;}
[data-testid="stDataFrame"]{border:1px solid var(--border)!important;border-radius:12px!important;overflow:hidden!important;}
[data-testid="stDataFrame"] th{background:var(--bg)!important;color:var(--hint)!important;font-size:10px!important;font-weight:600!important;letter-spacing:.1em!important;text-transform:uppercase!important;border-bottom:1px solid var(--border)!important;}
[data-testid="stDataFrame"] td{color:var(--text)!important;font-size:13px!important;border-bottom:1px solid var(--border)!important;}
[data-testid="stTabs"] [role="tablist"]{background:var(--bg)!important;border-radius:10px!important;padding:4px!important;border:1px solid var(--border)!important;}
[data-testid="stTabs"] [role="tab"]{border-radius:8px!important;font-size:13px!important;font-weight:500!important;color:var(--sub)!important;border:none!important;background:transparent!important;padding:6px 16px!important;}
[data-testid="stTabs"] [role="tab"][aria-selected="true"]{background:var(--surface)!important;color:var(--green-d)!important;box-shadow:0 1px 4px rgba(0,0,0,.08)!important;}
[data-testid="stExpander"]{border:1px solid var(--border)!important;border-radius:14px!important;background:var(--surface)!important;overflow:hidden!important;margin-top:48px!important;}
[data-testid="stExpander"] summary{font-size:13px!important;font-weight:500!important;color:var(--hint)!important;padding:14px 20px!important;}
[data-testid="stCheckbox"] label{color:var(--sub)!important;font-size:13px!important;}
[data-testid="stDownloadButton"] button{background:var(--bg)!important;border:1px solid var(--border)!important;color:var(--sub)!important;border-radius:10px!important;font-size:13px!important;height:40px!important;}
[data-testid="stDownloadButton"] button:hover{border-color:var(--gold)!important;color:var(--gold)!important;}
hr,[data-testid="stDivider"]{border-color:var(--border)!important;margin:28px 0!important;}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════
# 4. 데이터 함수
# ═══════════════════════════════════════════

def load_schedule() -> pd.DataFrame:
    sb = get_supabase()
    res = sb.table("schedules").select("*").execute()
    if not res.data:
        return pd.DataFrame(columns=REQUIRED_COLS + ["option_label"])
    df = pd.DataFrame(res.data)
    for col in REQUIRED_COLS:
        if col not in df.columns:
            df[col] = ""
    df["option_label"] = (
        df["date"].astype(str) + " | " + df["time"].astype(str) + " | " +
        df["golf_club"].astype(str) + " | " + df["course"].astype(str)
    )
    return df

def save_schedule_row(row: dict):
    sb = get_supabase()
    sb.table("schedules").insert(row).execute()

def update_schedule_row(row_id: int, data: dict):
    sb = get_supabase()
    sb.table("schedules").update(data).eq("id", row_id).execute()

def delete_schedule_row(row_id: int):
    sb = get_supabase()
    sb.table("schedules").delete().eq("id", row_id).execute()

def get_deadline() -> datetime:
    sb = get_supabase()
    res = sb.table("settings").select("value").eq("key", "deadline").execute()
    if not res.data:
        return datetime(2026, 12, 31, 23, 59, 59)
    return pd.to_datetime(res.data[0]["value"])

def update_deadline(new_date, new_time):
    new_dt = datetime.combine(new_date, new_time)
    sb = get_supabase()
    sb.table("settings").upsert({"key": "deadline", "value": new_dt.strftime("%Y-%m-%d %H:%M:%S")}).execute()
    return new_dt

def load_submissions() -> pd.DataFrame:
    sb = get_supabase()
    res = sb.table("submissions").select("*").execute()
    if not res.data:
        return pd.DataFrame(columns=["submitted_at","month","name","priority","date","time","golf_club","course"])
    return pd.DataFrame(res.data)

def save_submission(name: str, month: str, selected_rows: list):
    sb = get_supabase()
    submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = [{"submitted_at": submitted_at, "month": month, "name": name, **item} for item in selected_rows]
    sb.table("submissions").insert(rows).execute()

def delete_existing_submission(name: str, month: str):
    sb = get_supabase()
    sb.table("submissions").delete().eq("name", name).eq("month", month).execute()

def get_existing_submission(name: str, month: str) -> pd.DataFrame:
    sb = get_supabase()
    res = sb.table("submissions").select("*").eq("name", name).eq("month", month).execute()
    if not res.data:
        return pd.DataFrame()
    return pd.DataFrame(res.data)

def df_to_excel_bytes(df: pd.DataFrame) -> bytes:
    import io
    buf = io.BytesIO()
    df.to_excel(buf, index=False)
    return buf.getvalue()

def weekday_kr(d) -> str:
    return ["월","화","수","목","금","토","일"][d.weekday()]

def parse_date_from_str(raw) -> _dt.date:
    try:
        date_part = str(raw).strip().split("(")[0]
        m_part, d_part = date_part.split("/")
        return _dt.date(datetime.now().year, int(m_part), int(d_part))
    except Exception:
        return _dt.date.today()


# ═══════════════════════════════════════════
# 5. 공통 상수
# ═══════════════════════════════════════════
COURSE_MAP = {
    "오크힐스CC": ["힐코스", "브릿지코스"],
    "플라자CC":   ["타이거코스(OUT)", "타이거코스(IN)", "라이온코스(OUT)", "라이온코스(IN)"],
}
GOLF_LIST = list(COURSE_MAP.keys())


# ═══════════════════════════════════════════
# 6. 메인 화면
# ═══════════════════════════════════════════
full_schedule_df = load_schedule()
published_df     = full_schedule_df[full_schedule_df["status"] == "published"].reset_index(drop=True)
current_month    = published_df["month"].iloc[0] if not published_df.empty else "이번 달"
deadline_dt      = get_deadline()
is_closed        = datetime.now() > deadline_dt

st.markdown("""
<div class="golf-hero">
    <div class="eyebrow">Rounding Application</div>
    <h1>Dorco 라운딩<br>신청 컨시어지</h1>
    <p class="sub">Golf Schedule Reservation System</p>
</div>
""", unsafe_allow_html=True)

dl_str    = deadline_dt.strftime("%Y년 %m월 %d일")
badge_cls = "dl-badge-closed" if is_closed else "dl-badge-open"
badge_txt = "신청 마감" if is_closed else "신청 가능"
st.markdown(f"""
<div class="deadline-card">
    <div><div class="dl-label">신청 마감 일시</div><div class="dl-date">{dl_str}</div></div>
    <div class="{badge_cls}">{badge_txt}</div>
</div>
""", unsafe_allow_html=True)

if is_closed:
    st.markdown('<div class="closed-banner">⏳ 신청 기간이 종료되었습니다. 신규 신청 및 수정이 불가합니다.</div>', unsafe_allow_html=True)

st.markdown('<p class="sec-heading"><span>01</span>라운딩 일정</p>', unsafe_allow_html=True)
if published_df.empty:
    st.info("현재 공개된 라운딩 일정이 없습니다.")
else:
    disp = published_df[["date","time","golf_club","course"]].copy()
    disp.columns = ["날짜","시간","골프장","코스"]
    st.dataframe(disp, use_container_width=True, hide_index=True,
        column_config={
            "날짜":  st.column_config.TextColumn("날짜",   width="small"),
            "시간":  st.column_config.TextColumn("시간",   width="small"),
            "골프장":st.column_config.TextColumn("골프장", width="medium"),
            "코스":  st.column_config.TextColumn("코스",   width="medium"),
        })

st.markdown('<p class="sec-heading"><span>02</span>신청서 작성</p>', unsafe_allow_html=True)
name = st.text_input("신청자 성함", placeholder="본명을 입력해 주세요", disabled=is_closed)

if name.strip():
    existing = get_existing_submission(name.strip(), current_month)
    if not existing.empty:
        st.info(f"✨ **{name}**님의 기존 신청 내역이 있습니다. 재제출 시 최신 내용으로 업데이트됩니다.")
        prev = existing[["priority","date","time","golf_club","course"]].copy()
        prev.columns = ["순위","날짜","시간","골프장","코스"]
        st.dataframe(prev.sort_values("순위"), use_container_width=True, hide_index=True)

all_options  = published_df["option_label"].tolist()
blank_option = "— 일정 선택 —"

with st.form("application_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        rank1 = st.selectbox("1순위", [blank_option] + all_options, disabled=is_closed)
    with c2:
        rank2 = st.selectbox("2순위", [blank_option] + [o for o in all_options if o != rank1], disabled=is_closed)
    with c3:
        rank3 = st.selectbox("3순위", [blank_option] + [o for o in all_options if o not in [rank1, rank2]], disabled=is_closed)

    submitted = st.form_submit_button("신청서 제출하기", use_container_width=True, disabled=is_closed)
    if submitted:
        clean_name = name.strip()
        errors = []
        if not clean_name:
            errors.append("신청자 성함을 입력해 주세요.")
        if blank_option in [rank1, rank2, rank3]:
            errors.append("1순위부터 3순위까지 모두 선택해 주세요.")
        if errors:
            for e in errors: st.error(e)
        else:
            label_to_row = {r["option_label"]: r.to_dict() for _, r in published_df.iterrows()}
            selected_rows = [
                {"priority":"1순위", **label_to_row[rank1]},
                {"priority":"2순위", **label_to_row[rank2]},
                {"priority":"3순위", **label_to_row[rank3]},
            ]
            delete_existing_submission(clean_name, current_month)
            save_submission(clean_name, current_month, selected_rows)
            st.success(f"🎊 **{clean_name}**님, 신청이 완료되었습니다. 결과를 기다려 주세요!")
            st.balloons()


# ═══════════════════════════════════════════
# 7. 관리자 모드
# ═══════════════════════════════════════════
with st.expander("🔐 관리자 시스템"):

    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        pw = st.text_input("Access Password", type="password", key="admin_pw")
        if st.button("로그인", use_container_width=True, key="admin_login"):
            if pw == ADMIN_PASSWORD:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("비밀번호가 일치하지 않습니다.")
    else:
        hc1, hc2 = st.columns([5, 1])
        with hc2:
            if st.button("로그아웃", key="admin_logout"):
                st.session_state.admin_auth = False
                st.rerun()

        tab_status, tab_sched, tab_deadline, tab_reset = st.tabs([
            "📋 접수 현황", "🗂️ 스케줄 관리", "⏰ 마감 조정", "🗑️ 데이터 초기화"
        ])

        # ── 탭 1: 접수 현황 ──
        with tab_status:
            subs = load_submissions()
            if subs.empty:
                st.info("접수된 신청이 없습니다.")
            else:
                sub_tab1, sub_tab2 = st.tabs(["전체 제출 내역", "일정별 신청 현황"])
                with sub_tab1:
                    expected   = ["submitted_at","month","name","priority","date","time","golf_club","course"]
                    cols_exist = [c for c in expected if c in subs.columns]
                    disp = subs[cols_exist].copy()
                    if len(cols_exist) == 8:
                        disp.columns = ["제출시각","월","이름","순위","날짜","시간","골프장","코스"]
                    st.dataframe(disp, use_container_width=True, hide_index=True)
                    st.download_button(
                        "📥 엑셀 다운로드",
                        data=df_to_excel_bytes(disp),
                        file_name=f"submissions_{datetime.now().strftime('%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                    )
                with sub_tab2:
                    grouped = subs.groupby(["date","time","golf_club","course"], sort=False)
                    priority_order = {"1순위":1,"2순위":2,"3순위":3}
                    for (d, t, gc, co), grp in grouped:
                        st.markdown(f"**📍 {d} | {t} | {gc} | {co}**")
                        p1 = (grp["priority"]=="1순위").sum()
                        p2 = (grp["priority"]=="2순위").sum()
                        p3 = (grp["priority"]=="3순위").sum()
                        st.caption(f"총 {len(grp)}명  ·  1순위 {p1} / 2순위 {p2} / 3순위 {p3}")
                        vd = grp[["name","priority"]].copy()
                        vd.columns = ["이름","순위"]
                        vd["_ord"] = vd["순위"].map(priority_order)
                        vd = vd.sort_values(["_ord","이름"]).drop(columns="_ord")
                        st.dataframe(vd, use_container_width=True, hide_index=True)
                        st.divider()

        # ── 탭 2: 스케줄 관리 ──
        with tab_sched:
            schedule_manage_df = load_schedule().drop(columns=["option_label"], errors="ignore")

            st.markdown("**현재 등록된 스케줄**")
            if schedule_manage_df.empty:
                st.info("등록된 스케줄이 없습니다.")
            else:
                ed_df = schedule_manage_df.copy()
                ed_df["게시"] = ed_df["status"].apply(lambda x: str(x).strip() == "published")
                editor_input = ed_df[["month","date","time","golf_club","course","게시"]].copy()
                editor_input.columns = ["월","날짜","시간","골프장","코스","게시"]
                edited = st.data_editor(
                    editor_input, use_container_width=True, hide_index=False,
                    column_config={
                        "월":     st.column_config.TextColumn("월",     disabled=True),
                        "날짜":   st.column_config.TextColumn("날짜",   disabled=True),
                        "시간":   st.column_config.TextColumn("시간",   disabled=True),
                        "골프장": st.column_config.TextColumn("골프장", disabled=True),
                        "코스":   st.column_config.TextColumn("코스",   disabled=True),
                        "게시":   st.column_config.CheckboxColumn("게시", help="ON=게시 / OFF=보류"),
                    },
                    key="schedule_editor"
                )
                if st.button("게시 상태 저장", use_container_width=True, key="save_status"):
                    changed = False
                    for i in range(len(edited)):
                        new_status = "published" if bool(edited.loc[i,"게시"]) else "draft"
                        orig_status = str(schedule_manage_df.iloc[i]["status"]).strip()
                        if orig_status != new_status:
                            row_id = int(schedule_manage_df.iloc[i]["id"])
                            update_schedule_row(row_id, {"status": new_status})
                            changed = True
                    if changed:
                        st.success("게시 상태가 업데이트되었습니다.")
                        st.rerun()
                    else:
                        st.info("변경된 항목이 없습니다.")

            st.divider()

            s_add, s_edit, s_del = st.tabs(["➕ 스케줄 추가", "✏️ 스케줄 수정", "🗑️ 스케줄 삭제"])

            with s_add:
                c1, c2 = st.columns(2)
                add_date_obj = c1.date_input("일자", key="add_date")
                add_time_str = c2.text_input("티오프 시간", placeholder="예: 07:12", key="add_time")
                c3, c4 = st.columns(2)
                add_golf   = c3.selectbox("골프장", GOLF_LIST, key="add_golf")
                add_course = c4.selectbox("코스", COURSE_MAP[add_golf], key="add_course")
                if st.button("스케줄 저장 (보류 상태)", use_container_width=True, key="btn_add"):
                    if not add_time_str.strip():
                        st.warning("시간을 입력해 주세요.")
                    else:
                        wday = weekday_kr(add_date_obj)
                        save_schedule_row({
                            "month":     f"{add_date_obj.month}월",
                            "date":      f"{add_date_obj.month}/{add_date_obj.day}({wday})",
                            "time":      add_time_str.strip(),
                            "golf_club": add_golf,
                            "course":    add_course,
                            "status":    "draft"
                        })
                        st.success("저장되었습니다.")
                        st.rerun()

            with s_edit:
                fresh_edit = load_schedule().drop(columns=["option_label"], errors="ignore").reset_index(drop=True)
                if fresh_edit.empty:
                    st.info("수정할 스케줄이 없습니다.")
                else:
                    edit_options = [
                        f"{i} | {r['month']} | {r['date']} | {r['time']} | {r['golf_club']} | {r['course']}"
                        for i, r in fresh_edit.iterrows()
                    ]
                    sel_edit = st.selectbox(
                        "수정할 스케줄 선택", edit_options,
                        format_func=lambda x: " | ".join(x.split(" | ")[1:]),
                        key="edit_sel"
                    )
                    edit_idx  = int(sel_edit.split(" | ")[0].strip())
                    row       = fresh_edit.loc[edit_idx]

                    st.markdown("---")
                    st.markdown("**수정할 내용을 입력하세요**")
                    ec1, ec2 = st.columns(2)
                    edit_date_obj = ec1.date_input("일자", value=parse_date_from_str(row["date"]), key="edit_date")
                    edit_time_str = ec2.text_input("티오프 시간", value=str(row["time"]).strip(), key="edit_time")
                    ec3, ec4 = st.columns(2)
                    golf_default   = GOLF_LIST.index(row["golf_club"]) if row["golf_club"] in GOLF_LIST else 0
                    edit_golf      = ec3.selectbox("골프장", GOLF_LIST, index=golf_default, key="edit_golf")
                    course_list    = COURSE_MAP[edit_golf]
                    course_default = course_list.index(row["course"]) if row["course"] in course_list else 0
                    edit_course    = ec4.selectbox("코스", course_list, index=course_default, key="edit_course")
                    status_options = ["draft", "published"]
                    status_labels  = {"draft":"보류 (draft)", "published":"게시 (published)"}
                    cur_status     = str(row.get("status","draft")).strip()
                    status_idx     = status_options.index(cur_status) if cur_status in status_options else 0
                    edit_status    = st.selectbox("게시 상태", status_options, index=status_idx,
                                                  format_func=lambda x: status_labels[x], key="edit_status")
                    if st.button("✏️ 수정 저장", use_container_width=True, key="btn_edit"):
                        if not edit_time_str.strip():
                            st.warning("시간을 입력해 주세요.")
                        else:
                            wday_e = weekday_kr(edit_date_obj)
                            update_schedule_row(int(row["id"]), {
                                "month":     f"{edit_date_obj.month}월",
                                "date":      f"{edit_date_obj.month}/{edit_date_obj.day}({wday_e})",
                                "time":      edit_time_str.strip(),
                                "golf_club": edit_golf,
                                "course":    edit_course,
                                "status":    edit_status,
                            })
                            st.success(f"수정 완료!")
                            st.rerun()

            with s_del:
                fresh_sched = load_schedule().drop(columns=["option_label"], errors="ignore").reset_index(drop=True)
                if fresh_sched.empty:
                    st.info("삭제할 스케줄이 없습니다.")
                else:
                    del_options = [
                        f"{i} | {r['month']} | {r['date']} | {r['time']} | {r['golf_club']} | {r['course']}"
                        for i, r in fresh_sched.iterrows()
                    ]
                    sel_del = st.selectbox("삭제할 스케줄 선택", del_options, key="del_sel")
                    if st.button("선택 항목 삭제", use_container_width=True, key="btn_del"):
                        del_idx = int(sel_del.split(" | ")[0].strip())
                        delete_schedule_row(int(fresh_sched.loc[del_idx, "id"]))
                        st.success("삭제되었습니다.")
                        st.rerun()

        # ── 탭 3: 마감 조정 ──
        with tab_deadline:
            st.markdown("**마감 기한 변경**")
            dl_c1, dl_c2 = st.columns(2)
            new_d = dl_c1.date_input("마감 날짜", deadline_dt.date(), key="dl_date")
            new_t = dl_c2.time_input("마감 시간", deadline_dt.time(), key="dl_time")
            if st.button("저장", use_container_width=True, key="save_deadline"):
                update_deadline(new_d, new_t)
                st.toast("마감 기한이 업데이트되었습니다.")
                st.rerun()

        # ── 탭 4: 데이터 초기화 ──
        with tab_reset:
            st.warning("⚠️ 이 작업은 되돌릴 수 없습니다. 모든 제출 데이터가 삭제됩니다.")
            confirm = st.checkbox("삭제에 동의하며, 제출 데이터를 초기화합니다.", key="reset_confirm")
            if st.button("초기화 실행", use_container_width=True, key="reset_btn", disabled=not confirm):
                get_supabase().table("submissions").delete().neq("id", 0).execute()
                st.toast("데이터가 초기화되었습니다.")
                st.rerun()
