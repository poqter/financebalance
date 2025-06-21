import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 📄 페이지 설정
st.set_page_config(page_title="보장 리모델링 Before & After 비교", layout="wide")
st.title("🔄 보장 리모델링 Before & After 비교")

# 입력 행 수
num_rows = st.slider("입력할 보장 항목 수", min_value=1, max_value=20, value=5)

# 🔍 카테고리 자동 분류 함수
def classify_category(name):
    if "진단" in name:
        return "진단비"
    elif "입원" in name:
        return "입원비"
    elif "수술" in name:
        return "수술비"
    else:
        return "기타"

# ✍️ 입력 폼
col1, col2 = st.columns(2)
with col1:
    st.subheader("✅ 기존 설계 입력")
    before_data = []
    for i in range(num_rows):
        name = st.text_input(f"보장명 (기존) - {i+1}", key=f"before_name_{i}")
        amount = st.number_input(f"보장금액 (기존) - {i+1}", min_value=0, step=10000, key=f"before_amt_{i}")
        premium = st.number_input(f"월 보험료 (기존) - {i+1}", min_value=0, step=1000, key=f"before_premium_{i}")
        before_data.append({"보장명": name, "보장금액": amount, "월보험료": premium})
    before_df = pd.DataFrame(before_data).dropna()
    before_df["카테고리"] = before_df["보장명"].apply(classify_category)

with col2:
    st.subheader("🛠️ 리모델링 설계 입력")
    after_data = []
    for i in range(num_rows):
        name = st.text_input(f"보장명 (리모델링) - {i+1}", key=f"after_name_{i}")
        amount = st.number_input(f"보장금액 (리모델링) - {i+1}", min_value=0, step=10000, key=f"after_amt_{i}")
        premium = st.number_input(f"월 보험료 (리모델링) - {i+1}", min_value=0, step=1000, key=f"after_premium_{i}")
        after_data.append({"보장명": name, "보장금액": amount, "월보험료": premium})
    after_df = pd.DataFrame(after_data).dropna()
    after_df["카테고리"] = after_df["보장명"].apply(classify_category)

# 🔄 비교 시각화
if not before_df.empty and not after_df.empty:
    total_before = before_df["월보험료"].sum()
    total_after = after_df["월보험료"].sum()
    savings = total_before - total_after
    savings_rate = (savings / total_before) * 100 if total_before else 0

    # ✨ 추천 문구 자동 생성
    if savings > 0 and savings_rate >= 20:
        reco_text = "👍 월 보험료를 크게 절감하면서도 보장을 유지했어요!"
    elif savings > 0:
        reco_text = "👍 보장은 유지하면서도 월 보험료를 줄였습니다!"
    elif savings < 0 and after_df["보장금액"].sum() > before_df["보장금액"].sum():
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
        <p>보장 항목 수: {len(before_df)}</p>
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
    before_cat = before_df.groupby("카테고리")["보장금액"].sum().reset_index()
    after_cat = after_df.groupby("카테고리")["보장금액"].sum().reset_index()
    combined = pd.merge(before_cat, after_cat, on="카테고리", how="outer", suffixes=("_기존", "_리모델링")).fillna(0)

    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(len(combined))
    width = 0.4
    ax.bar([i - width/2 for i in x], combined["보장금액_기존"], width=width, label="기존", color="#adb5bd")
    ax.bar([i + width/2 for i in x], combined["보장금액_리모델링"], width=width, label="리모델링", color="#339af0")
    ax.set_xticks(list(x))
    ax.set_xticklabels(combined["카테고리"])
    ax.set_ylabel("보장금액 (원)")
    ax.legend()
    st.pyplot(fig)
