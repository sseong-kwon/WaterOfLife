import streamlit as st

# --------------------
# 기본 페이지 설정
# --------------------
st.set_page_config(
    page_title="술 취향 설문 & 추천",
    page_icon="🍶",
    layout="centered"
)

# --------------------
# 헤더 / 설명
# --------------------
st.title("🍷 취향 기반 술 추천기")
st.markdown(
    """
    간단한 **설문조사**를 통해  
    당신의 취향에 맞는 **위스키, 사케, 전통주, 와인**을 추천해 드립니다.  
    아래 질문에 편하게 답해 주세요 😄
    """
)

# --------------------
# 상단 이미지 (플레이스홀더 이미지)
# --------------------
col_img1, col_img2 = st.columns(2)

with col_img1:
    st.image(
        "https://via.placeholder.com/400x250?text=Whisky+%F0%9F%8D%B7",
        caption="위스키 / 사케 등 증류주",
        use_column_width=True
    )

with col_img2:
    st.image(
        "https://via.placeholder.com/400x250?text=Wine+%F0%9F%8D%B7",
        caption="와인 / 전통주 등 발효주",
        use_column_width=True
    )

st.markdown("---")

# --------------------
# 설문 폼
# --------------------
st.header("1️⃣ 취향 설문")

with st.form("preference_form"):
    st.subheader("맛 / 향 취향")

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

    st.subheader("도수 / 상황")

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

    submitted = st.form_submit_button("✨ 추천 받기")


# --------------------
# 추천 로직 함수
# --------------------
def recommend_drink(flavor, body, sweetness, abv, occasion, budget, carbonation, prefer_type):
    min_abv, max_abv = abv

    # 간단한 룰 기반 추천 예시 (나중에 네가 마음대로 고도화 가능)
    candidates = []

    # 1. 위스키 추천
    if (min_abv >= 15 or max_abv >= 35) and ("탄향/스모키" in flavor or "곡물/빵향" in flavor):
        if budget in ["5~10만 원", "10만 원 이상"]:
            candidates.append({
                "type": "위스키",
                "name": "스모키 싱글 몰트 위스키",
                "desc": "탄향과 곡물향이 잘 살아있는 싱글 몰트 스타일. 스트레이트 또는 온더락으로 천천히 즐기기 좋습니다.",
                "img": "https://via.placeholder.com/400x250?text=Smoky+Whisky"
            })
        else:
            candidates.append({
                "type": "위스키",
                "name": "부드러운 블렌디드 위스키",
                "desc": "알코올 자극은 덜하고, 곡물향과 단맛이 적당해 입문용으로 좋습니다.",
                "img": "https://via.placeholder.com/400x250?text=Blended+Whisky"
            })

    # 2. 사케 추천
    if min_abv <= 20 and "쌉쌀함" in flavor or "과일향" in flavor:
        if sweetness in ["약간 단 편", "적당히 단 편", "꽤 단 편"]:
            candidates.append({
                "type": "사케",
                "name": "준마이 긴조 계열 사케",
                "desc": "은은한 과일향과 부드러운 감칠맛이 있어, 회나 가벼운 요리와 곁들이기 좋습니다.",
                "img": "https://via.placeholder.com/400x250?text=Sake"
            })
        else:
            candidates.append({
                "type": "사케",
                "name": "드라이 타입 준마이 사케",
                "desc": "단맛이 적고 깔끔하게 떨어져, 기름진 음식이나 튀김류와 잘 어울립니다.",
                "img": "https://via.placeholder.com/400x250?text=Dry+Sake"
            })

    # 3. 전통주 추천
    if "달콤함" in flavor or sweetness in ["적당히 단 편", "꽤 단 편", "아주 달게"]:
        if carbonation == "탄산 있는 게 좋다":
            candidates.append({
                "type": "전통주",
                "name": "탄산 막걸리 / 스파클링 탁주",
                "desc": "은은한 단맛과 산미, 탄산이 어우러져 가볍게 즐기기 좋은 스타일입니다.",
                "img": "https://via.placeholder.com/400x250?text=Sparkling+Makgeolli"
            })
        else:
            candidates.append({
                "type": "전통주",
                "name": "프리미엄 약주 / 청주",
                "desc": "깔끔한 곡물향과 단맛이 조화로운 고급 약주로, 선물용이나 식사와 곁들이기 좋습니다.",
                "img": "https://via.placeholder.com/400x250?text=Korean+Rice+Wine"
            })

    # 4. 와인 추천
    if "과일향" in flavor or occasion in ["데이트/분위기용", "친구들과 모임"]:
        if body == "가볍고 산뜻한 편":
            candidates.append({
                "type": "와인",
                "name": "산뜻한 화이트 와인 (소비뇽 블랑 계열)",
                "desc": "상큼한 산미와 시트러스/열대과일 향이 특징으로, 가벼운 음식과 잘 어울립니다.",
                "img": "https://via.placeholder.com/400x250?text=White+Wine"
            })
        else:
            candidates.append({
                "type": "와인",
                "name": "미디엄 바디 레드 와인",
                "desc": "과일향과 약간의 탄닌이 조화로운 스타일로, 파스타/고기 요리와 두루 잘 어울립니다.",
                "img": "https://via.placeholder.com/400x250?text=Red+Wine"
            })

    # 5. 선호 주종 필터링 (선택한 경우만)
    if prefer_type:
        filtered = [c for c in candidates if c["type"] in prefer_type]
        if filtered:
            candidates = filtered

    # 후보가 하나도 없으면 기본 추천
    if not candidates:
        candidates.append({
            "type": "라이트한 주종",
            "name": "가벼운 화이트 와인 또는 탄산 막걸리",
            "desc": "도수 부담이 적고, 다양한 음식과 무난하게 어울려 입문용으로 추천드립니다.",
            "img": "https://via.placeholder.com/400x250?text=Light+Drink"
        })

    return candidates


# --------------------
# 결과 출력
# --------------------
if submitted:
    st.header("2️⃣ 추천 결과")

    recs = recommend_drink(flavor, body, sweetness, abv, occasion, budget, carbonation, prefer_type)

    for rec in recs:
        st.subheader(f"✅ 추천 주종: {rec['type']} - {rec['name']}")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(rec["img"], use_column_width=True)
        with col2:
            st.write(rec["desc"])
            st.caption(f"상황: {occasion} · 예산: {budget} · 선호 도수: {abv[0]}~{abv[1]}%")

    st.markdown("---")
    st.info("※ 실제 제품 이름이 아니라, 스타일(타입)에 대한 추천 예시입니다. 나중에 브랜드/제품명으로 확장할 수 있어요.")
else:
    st.info("위 설문을 입력하고 **'✨ 추천 받기'** 버튼을 눌러보세요!")
