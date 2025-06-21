import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="보장 리모델링 Before & After 비교", layout="wide")
st.title("🔄 보장 리모델링 Before & After 비교")

# 보장 항목 리스트
(중략... 기존 코드 유지)

    # 추천 멘트
    st.markdown("### 📝 리모델링 핵심 요약")
    if diff > 0 and rate >= 15:
        st.markdown("👍 보험료를 효과적으로 절감하면서 주요 보장 항목은 유지 또는 강화되었습니다.")
    elif diff > 0:
        st.markdown("👍 보험료가 절감되었고, 대부분의 보장이 유지되었습니다.")
    elif diff < 0 and (edited_df["상태"] == "🟢 강화").sum() > (edited_df["상태"] == "🔴 축소").sum():
        st.markdown("🔎 보험료는 소폭 상승했지만, 주요 위험에 대한 보장이 한층 강화되어 예기치 못한 상황에 더 잘 대비할 수 있는 설계가 되었습니다.")
    else:
        st.markdown("📌 리모델링으로 일부 보장이 조정되었으며 보험료도 함께 변경되었습니다.")

    # 시나리오형 보험금 수령 시뮬레이션
    st.markdown("---")
    st.markdown("### 🧾 보험금 수령 시뮬레이션")

    scenario = st.selectbox("📍 가상 시나리오 선택", ["암 진단", "교통사고 입원"])
    expected_cost = 0

    if scenario == "암 진단":
        expected_cost = 30000000  # 가정: 암 치료 총비용 3천만 원
        match_keywords = ["암"]
    elif scenario == "교통사고 입원":
        expected_cost = 10000000  # 가정: 입원+휴업 손실 비용 1천만 원
        match_keywords = ["입원", "상해", "교통사고"]

    matched_df = edited_df[edited_df["보장명"].str.contains('|'.join(match_keywords), case=False, na=False)]
    total_payout = matched_df["보장금액_리모델링"].sum()

    st.markdown(f"**🩺 예상 치료/손실 비용:** {expected_cost:,.0f} 원")
    st.markdown(f"**📦 현재 예상 수령 보험금:** {total_payout:,.0f} 원")

    gap = expected_cost - total_payout

    if gap > 0:
        st.error(f"❗부족 예상 금액: {gap:,.0f} 원 → 이대로 괜찮으신가요?")
        st.markdown("🧭 필요 보장 보완에 대해 함께 고민해보는 것이 좋겠습니다.")
    else:
        st.success("✅ 현재 보장으로 충분히 대비되어 있습니다.")
