import streamlit as st

# 페이지 설정
st.set_page_config(page_title="보험료 적정선 분석기", layout="centered")
st.title("💸 생활지출 기반 보험료 적정선 분석기")

st.markdown("고객의 소득과 지출을 기반으로 적절한 보험료, 저축률, 투자 여력을 함께 분석합니다.")

# 사용자 입력
income = st.number_input("1️⃣ 월 소득 (원)", min_value=0, step=10000)
fixed_expense = st.number_input("2️⃣ 고정 지출 (원)", min_value=0, step=10000)
current_premium = st.number_input("3️⃣ 현재 보험료 (원)", min_value=0, step=1000)
saving = st.number_input("4️⃣ 현재 저축 금액 (원)", min_value=0, step=1000)

# 계산
available_money = income - fixed_expense if income > fixed_expense else 0
lower_bound = int(available_money * 0.10)
upper_bound = int(available_money * 0.15)
saving_rate = (saving / income * 100) if income else 0
suggested_invest = int(available_money * 0.1)

# 결과 출력
st.markdown("---")
st.subheader("📊 분석 결과 요약")

st.write(f"💰 가용 생활 자금: **{available_money:,}원**")
st.write(f"📌 적정 보험료: **{lower_bound:,}원 ~ {upper_bound:,}원**")

if current_premium:
    if upper_bound == 0:
        over_rate = 0
    else:
        over_rate = current_premium / upper_bound
    st.write(f"🔎 현재 보험료: **{current_premium:,}원**")
    if current_premium > upper_bound:
        st.error(f"❗ 현재 보험료는 적정선 대비 **{over_rate:.1f}배**입니다.")
    elif current_premium < lower_bound:
        st.success("✅ 보험료가 매우 안정적인 수준입니다.")
    else:
        st.info("💡 현재 보험료는 적정 범위 내에 있습니다.")

st.write(f"💾 현재 저축률: **{saving_rate:.1f}%**")
st.write(f"📈 추천 투자 여력 (가용금의 10%): **{suggested_invest:,}원**")

# 종합 의견
st.markdown("---")
st.subheader("💡 종합 의견")

if current_premium > upper_bound:
    st.markdown(
        f"""
        현재 보험료가 가용금액 대비 과다하여  
        저축 및 투자 여력이 줄어드는 구조입니다.  
        보험 리모델링으로 월 {current_premium - upper_bound:,}원 절감 시  
        저축 또는 투자 비중을 높일 수 있습니다.
        """
    )
else:
    st.markdown("현재 지출 구조는 비교적 안정적이며, 저축 및 투자 비중을 유지하거나 확대할 여지가 있습니다.")
