import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="보장 리모델링 Before & After 비교", layout="wide")
st.title("🔄 보장 리모델링 Before & After 비교")

# 보장 항목 리스트
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

# 자동 카테고리 분류 함수
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

# 사이드바 항목 선택
st.sidebar.header("📋 보장 항목 선택")
selected_items = st.sidebar.multiselect("비교할 항목을 선택하세요", guarantee_items)

if selected_items:
    st.subheader("💡 선택한 항목에 대한 보장금액 입력")

    df_input = pd.DataFrame({"보장명": selected_items})
    df_input["보장금액_기존"] = 0
    df_input["보장금액_리모델링"] = 0
    df_input["카테고리"] = df_input["보장명"].apply(classify_category)

    edited_df = st.data_editor(df_input, num_rows="dynamic", use_container_width=True)

    st.subheader("💳 월 보험료 입력")
    col1, col2 = st.columns(2)
    with col1:
        total_before = st.number_input("총 월 보험료 (기존)", min_value=0)
    with col2:
        total_after = st.number_input("총 월 보험료 (리모델링)", min_value=0)

    st.divider()
    st.subheader("📌 보장 변화 요약")
    edited_df["상태"] = edited_df.apply(
        lambda row: "🟢 강화" if row["보장금액_리모델링"] > row["보장금액_기존"] else
                    "🔴 축소" if row["보장금액_리모델링"] < row["보장금액_기존"] else "⚪ 유지",
        axis=1
    )

    # 상태 강조 테이블
    st.markdown("### 📋 항목별 변화 상태")
    styled_df = edited_df.style.applymap(
        lambda v: "background-color: #d1e7dd" if v == "🟢 강화" else
                  "background-color: #f8d7da" if v == "🔴 축소" else
                  "background-color: #fefefe", subset=["상태"]
    )
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    # 카드 형식 보험료 비교
    st.markdown("### 💳 월 보험료 카드 비교")
    card_col1, card_col2 = st.columns(2)
    with card_col1:
        st.markdown(f"""
        <div style='padding:20px; background-color:#f8f9fa; border-left:5px solid #adb5bd; border-radius:10px'>
        <h4>기존 월 보험료</h4>
        <h2 style='color:#212529'>{total_before:,.0f}원</h2>
        </div>
        """, unsafe_allow_html=True)
    with card_col2:
        st.markdown(f"""
        <div style='padding:20px; background-color:#e7f5ff; border-left:5px solid #339af0; border-radius:10px'>
        <h4>리모델링 후 월 보험료</h4>
        <h2 style='color:#1c7ed6'>{total_after:,.0f}원</h2>
        </div>
        """, unsafe_allow_html=True)

    # 절감 효과 강조
    diff = total_before - total_after
    rate = (diff / total_before * 100) if total_before else 0
    st.markdown("### 📉 절감 효과")
    if diff > 0:
        st.success(f"💸 월 보험료가 총 **{diff:,.0f}원 절감**되었습니다. (절감율: **{rate:.1f}%**) ✅")
    elif diff < 0:
        st.warning(f"📈 월 보험료가 총 **{abs(diff):,.0f}원 증가**했습니다. (증가율: **{abs(rate):.1f}%**) ⚠️")
    else:
        st.info("📌 월 보험료는 변동이 없습니다.")

    # 추천 멘트
    st.markdown("### 📝 리모델링 핵심 요약")
    if diff > 0 and rate >= 15:
        st.markdown("👍 보험료를 효과적으로 절감하면서 주요 보장 항목은 유지 또는 강화되었습니다.")
    elif diff > 0:
        st.markdown("👍 보험료가 절감되었고, 대부분의 보장이 유지되었습니다.")
    elif diff < 0 and (edited_df["상태"] == "🟢 강화").sum() > (edited_df["상태"] == "🔴 축소").sum():
        st.markdown("✅ 일부 보험료가 증가했지만, 보장 수준이 전반적으로 강화되었습니다.")
    else:
        st.markdown("📌 리모델링으로 일부 보장이 조정되었으며 보험료도 함께 변경되었습니다.")
