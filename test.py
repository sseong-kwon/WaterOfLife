import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =========================
# 설정
# =========================
st.set_page_config(
    page_title="술 취향 설문 & 추천",
    page_icon="🍶",
    layout="centered"
)

DATA_PATH = "survey_data.csv"

st.title("🍷 실시간 술 취향 설문 & 추천")
st.markdown(
    """
    발표 시간 동안만 운영되는 **실시간 설문 페이지**입니다.  
    아래 설문에 답하면, 나중에 모두 함께 **취향 통계와 추천 주종 분포**를 그래프로 확인합니다.
    """
)

st.markdown("---")

# =========================
# 1. 설문 폼
# =========================
st.header("1️⃣ 취향 설문")

with st.form("preference_form"):
    nickname = st.text_input("닉네임 또는 이니셜 (선택)", "")

    flavor = st.multiselect(
        "좋아하는 맛/향을 골라보세요. (복수 선택 가능)",
        ["과일향", "꽃향", "탄향/스모키", "곡물/빵향", "쌉쌀함", "고소함", "달콤함"],
        default=["과일향"]
    )

    body = st.selectbox(
        "술의 무게감(바디감)은 어떤 걸 좋아하나요?",
        ["가볍고 산뜻한 편", "중간 정도", "무겁고 진한 편"]
    )

    sweetness = st.select_slider(
        "단맛 선호도는 어느 정도인가요?",
        options=["거의 없음", "약간 단 편", "적당히 단 편", "꽤 단 편", "아주 달게"],
        value="약간 단 편"
    )

    abv = st.slider(
        "편하게 즐기기 좋은 도수 범위는?",
        min_value=5,
        max_value=50,
        value=(10, 25),
        step=1
    )

    occasion = st.selectbox(
        "주로 어떤 상황에서 마실 술인가요?",
        ["혼술용", "친구들과 모임", "식사와 곁들이기", "선물용", "데이트/분위기용"]
    )

    budget = st.select_slider(
        "1병 기준 예산은 어느 정도를 생각하시나요?",
        options=["~2만 원", "2~5만 원", "5~10만 원", "10만 원 이상"],
        value="2~5만 원"
    )

    carbonation = st.radio(
        "탄산이 있는 술을 좋아하나요?",
        ["상관없음", "탄산 있는 게 좋다", "탄산 없는 게 좋다"],
        index=0,
        horizontal=True
    )

    prefer_type = st.multiselect(
        "특히 관심 있는 주종이 있나요? (비워두면 상관없음)",
        ["위스키", "사케", "전통주", "와인"],
        default=[]
    )

    submitted = st.form_submit_button("✨ 설문 제출하기")


# =========================
# 2. 간단 추천 로직
# =========================
def recommend_type(flavor, body, sweetness, abv, occasion, budget, carbonation, prefer_type):
    min_abv, max_abv = abv
    rec = "와인"  # 기본값

    if max_abv >= 35 and ("탄향/스모키" in flavor or "곡물/빵향" in flavor):
        rec = "위스키"
    elif "달콤함" in flavor and min_abv <= 20:
        rec = "전통주"
    elif "과일향" in flavor and min_abv <= 20:
        rec = "사케"

    if prefer_type:
        rec = prefer_type[0]  # 선호 주종이 있으면 그 중 첫 번째로 덮어쓰기 (단순화)

    return rec


# =========================
# 3. 제출 시 CSV 저장
# =========================
if submitted:
    recommended = recommend_type(flavor, body, sweetness, abv, occasion, budget, carbonation, prefer_type)

    # 1) 새 레코드 생성
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nickname": nickname,
        "flavor": ";".join(flavor),
        "body": body,
        "sweetness": sweetness,
        "abv_min": abv[0],
        "abv_max": abv[1],
        "occasion": occasion,
        "budget": budget,
        "carbonation": carbonation,
        "prefer_type": ";".join(prefer_type) if prefer_type else "",
        "recommended_type": recommended,
    }

    # 2) 기존 CSV에 append
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(DATA_PATH, index=False)

    st.success(f"설문이 제출되었습니다! (예상 추천 주종: **{recommended}**)")

st.markdown("---")

# =========================
# 4. 발표용 결과 섹션
# =========================
st.header("2️⃣ 실시간 설문 결과 (발표용)")

st.caption("※ 발표자가 화면을 공유하고 이 섹션을 보여주면 됩니다. 응답이 들어올 때마다 페이지 새로고침하면 그래프가 업데이트됩니다.")

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)

    st.subheader(f"현재까지 응답 수: {len(df)}명")

    # 보기 쉽게 최근 응답 몇 개
    with st.expander("📋 최근 응답 보기 (옵션)", expanded=False):
        st.dataframe(df.tail(10))

    # 1) 추천 주종 분포
    st.subheader("🍶 추천 주종 분포")
    type_counts = df["recommended_type"].value_counts()
    st.bar_chart(type_counts)

    # 2) 단맛 선호도
    st.subheader("🍭 단맛 선호도 분포")
    sweet_counts = df["sweetness"].value_counts().sort_index()
    st.bar_chart(sweet_counts)

    # 3) 마시는 상황 분포
    st.subheader("🎯 마시는 상황(occasion) 분포")
    occ_counts = df["occasion"].value_counts()
    st.bar_chart(occ_counts)

    # 4) 예산 분포
    st.subheader("💸 예산 분포")
    budget_counts = df["budget"].value_counts().sort_index()
    st.bar_chart(budget_counts)

else:
    st.info("아직 설문 응답이 없습니다. 청중에게 설문 링크를 공유한 뒤, 응답이 들어오면 이 영역을 새로고침해서 결과를 확인하세요.")
