import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 📄 페이지 설정
st.set_page_config(page_title="보장 리모델링 Before & After 비교", layout="wide")
st.title("🔄 보장 리모델링 Before & After 비교")

# 📌 보장 항목 목록
guarantee_items = [
    "일반사망", "질병사망", "재해(상해)사망", "질병후유장해", "재해(상해)장해",
    "일반암", "유사암", "뇌혈관", "뇌졸중", "뇌출혈", "허혈성심장질환", "급성심근경색증",
    "질병수술", "질병종수술", "상해수술", "상해종수술",
    "뇌혈관질환수술", "허혈성심장질환수술",
    "질병입원", "상해입원", "간병인",
    "교통사고처리지원금", "스쿨존사고처리지원금", "변호사선임비용",
    "운전자벌금(대인)", "운전자벌금(대물)", "자동차사고부상위로금", "일상생활배상책임",
    "치아보철치료비", "치아보존치료비", "골절진단비",
    "질병입원(실손)", "질병통원(실손)", "상해입원(실손)", "상해통원(실손)"
]

# 🔍 카테고리 자동 분류 함수
def classify_category(name):
    if "암" in name:
        return "암"
    elif "심장" in name or "허혈성" in name:
        return "심장"
    elif "뇌" in name:
        return "뇌혈관"
    elif "수술" in name:
        return "수술"
    elif "입원" in name or "실손" in name:
        return "입원"
    elif "사망" in name:
        return "사망"
    elif "장해" in name:
        return "장해"
    elif "벌금" in name or "변호사" in name or "운전자" in name or "사고" in name:
        return "운전자"
    elif "치아" in name:
        return "치아"
    elif "골절" in name:
        return "기타"
    else:
        return "기타"

# 🧭 사이드바에서 보장 항목 선택
st.sidebar.header("보장 항목 선택")
selected_items = st.sidebar.multiselect("비교할 보장 항목을 선택하세요", guarantee_items)

# ✍️ 선택 항목 입력
if selected_items:
    st.subheader("✅ 기존 설계 vs 리모델링 설계 입력")
    input_data = []
    for item in selected_items:
        with st.expander(f"📌 {item}"):
            col1, col2 = st.columns(2)
            with col1:
                before_amt = st.number_input(f"[기존] 보장금액 - {item}", min_value=0, step=10000, key=f"b_amt_{item}")
                before_prem = st.number_input(f"[기존] 월 보험료 - {item}", min_value=0, step=1000, key=f"b_prem_{item}")
            with col2:
                after_amt = st.number_input(f"[리모델링] 보장금액 - {item}", min_value=0, step=10000, key=f"a_amt_{item}")
                after_prem = st.number_input(f"[리모델링] 월 보험료 - {item}", min_value=0, step=1000, key=f"a_prem_{item}")
            input_data.append({
                "보장명": item,
                "보장금액_기존": before_amt,
                "월보험료_기존": before_prem,
                "보장금액_리모델링": after_amt,
                "월보험료_리모델링": after_prem,
                "카테고리": classify_category(item)
            })

    df = pd.DataFrame(input_data)

    if not df.empty:
        total_before = df["월보험료_기존"].sum()
        total_after = df["월보험료_리모델링"].sum()
        savings = total_before - total_after
        savings_rate = (savings / total_before) * 100 if total_before else 0

        if savings > 0 and savings_rate >= 20:
            reco_text = "👍 월 보험료를 크게 절감하면서도 보장을 유지했어요!"
        elif savings > 0:
            reco_text = "👍 보장은 유지하면서도 월 보험료를 줄였습니다!"
        elif savings < 0 and df["보장금액_리모델링"].sum() > df["보장금액_기존"].sum():
            reco_text = "👍 보험료는 소폭 상승했지만 보장이 더 강해졌어요!"
        else:
            reco_text = "📌 리모델링으로 보장이 일부 조정되었어요. 자세한 설명을 참고하세요."

        # 💳 감성 카드 UI
        st.markdown("### 💳 감성 카드 요약 비교")
        col_card1, col_card2 = st.columns(2)
        with col_card1:
            st.markdown(f"""
            <div style="background-color:#f8f9fa; padding:20px; border-radius:15px; border-left: 10px solid #adb5bd">
            <h3 style="color:#495057;">✅ 기존 설계</h3>
            <p>총 월 보험료: <strong style="font-size:22px;">{total_before:,.0f}원</strong></p>
            <p>보장 항목 수: {len(df)}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_card2:
            st.markdown(f"""
            <div style="background-color:#e6f7ff; padding:20px; border-radius:15px; border-left: 10px solid #339af0">
            <h3 style="color:#1c7ed6;">🛠️ 리모델링 설계</h3>
            <p>총 월 보험료: <strong style="font-size:22px;">{total_after:,.0f}원</strong></p>
            <p>절감액: <strong style="color:#d9480f;">{savings:,.0f}원</strong></p>
            <p>절감율: <strong style="color:#fa5252;">{savings_rate:.1f}%</strong></p>
            <p style="margin-top:10px; font-size:18px;">{reco_text}</p>
            </div>
            """, unsafe_allow_html=True)

        # 📊 카테고리별 보장금액 비교
        st.markdown("### 🔥 카테고리별 보장금액 비교")
        cat_sum = df.groupby("카테고리")[["보장금액_기존", "보장금액_리모델링"]].sum().reset_index()

        fig, ax = plt.subplots(figsize=(8, 4))
        x = range(len(cat_sum))
        width = 0.4
        ax.bar([i - width/2 for i in x], cat_sum["보장금액_기존"], width=width, label="기존", color="#adb5bd")
        ax.bar([i + width/2 for i in x], cat_sum["보장금액_리모델링"], width=width, label="리모델링", color="#339af0")
        ax.set_xticks(list(x))
        ax.set_xticklabels(cat_sum["카테고리"])
        ax.set_ylabel("보장금액 (원)")
        ax.legend()
        st.pyplot(fig)
