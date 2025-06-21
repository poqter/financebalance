import streamlit as st
import pandas as pd

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
    df_input["보장금액_기존"] = ""
    df_input["보장금액_리모델링"] = ""
    df_input["카테고리"] = df_input["보장명"].apply(classify_category)

    edited_df = st.data_editor(df_input, num_rows="dynamic", use_container_width=True)

    st.subheader("💳 월 보험료 입력")
    col1, col2 = st.columns(2)
    with col1:
        total_before = st.text_input("총 월 보험료 (기존)")
    with col2:
        total_after = st.text_input("총 월 보험료 (리모델링)")

    st.divider()
    st.subheader("📌 입력 요약")
    st.write(edited_df)
    st.write(f"총 월 보험료 (기존): {total_before} 원")
    st.write(f"총 월 보험료 (리모델링): {total_after} 원")
