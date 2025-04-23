
import streamlit as st
import pandas as pd
import uuid
from sklearn.metrics.pairwise import cosine_similarity

# --- 假資料區 ---
# 原料功能布林向量
ingredient_vectors = pd.DataFrame({
    "起泡": [1, 0, 1, 0],
    "保濕": [1, 1, 1, 0],
    "蛋白質來源": [1, 0, 1, 0],
    "甜味": [0, 0, 0, 1],
    "焦糖化": [0, 0, 0, 1],
    "油脂感": [0, 1, 0, 0],
}, index=["液蛋白", "液蛋黃", "乳清蛋白", "砂糖"])

# 記錄歷史配方
if "formulas" not in st.session_state:
    st.session_state.formulas = {}

# --- 介面區 ---
st.title("AI 食品研發跨部門模擬平台")
st.sidebar.header("📦 配方輸入")

# 配方輸入
selected_ingredients = st.sidebar.multiselect("選擇原料：", ingredient_vectors.index.tolist())

if selected_ingredients:
    st.subheader("🔬 功能分析與替代建議")
    selected_vector = ingredient_vectors.loc[selected_ingredients].sum().clip(upper=1)
    st.write("📊 功能分佈：")
    st.dataframe(selected_vector.to_frame(name="啟用功能"))

    # 相似原料推薦
    st.write("🧠 替代建議：")
    sim_scores = cosine_similarity([selected_vector], ingredient_vectors)[0]
    similar_df = pd.DataFrame({
        "原料": ingredient_vectors.index,
        "相似度": sim_scores
    }).sort_values(by="相似度", ascending=False)
    st.dataframe(similar_df[~similar_df["原料"].isin(selected_ingredients)].head(3))

    # 儲存配方
    name = st.text_input("為此配方命名：")
    if st.button("💾 儲存配方"):
        key = str(uuid.uuid4())
        st.session_state.formulas[key] = {
            "name": name or f"未命名配方_{len(st.session_state.formulas)+1}",
            "ingredients": selected_ingredients,
            "vector": selected_vector
        }
        st.success("配方已儲存！")

# 配方歷史區
st.sidebar.header("📚 歷史配方")
if st.session_state.formulas:
    for fid, record in st.session_state.formulas.items():
        with st.sidebar.expander(record["name"]):
            st.write(", ".join(record["ingredients"]))
else:
    st.sidebar.info("尚無儲存配方")
