import streamlit as st
import pandas as pd
import requests

# Streamlit 应用标题和介绍
st.set_page_config(page_title="滑坡风险判别系统", page_icon="🌍", layout="wide")
st.title("💬 滑坡风险判别系统")
st.markdown("""
    ### 基于 Claude 3.5 200k 微调模型的滑坡风险判别  
    请选择您想要使用的方式：手动调整滑坡因素，或上传包含地形、降雨等数据的文件，应用将自动判别滑坡风险。  
    如果使用 Claude 3.5 模型进行进一步的分析，请输入 API 密钥。
""")

# 设置侧边栏，让用户输入自己的 Claude API 密钥
st.sidebar.title("🛠 API 设置")
API_KEY = st.sidebar.text_input("请输入您的 Claude API 密钥", type="password")

# 如果 API 密钥没有输入，提示用户输入
if not API_KEY:
    st.sidebar.warning("请在此输入 Claude API 密钥后，方可使用 Claude 模型进行进一步分析。")

# 创建从 Claude 获取响应的函数
CLAUDE_API_ENDPOINT = "https://api.example.com/claude"  # 替换为真实的终端地址

def get_claude_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 200000  # 假设你使用200k的微调模型
    }
    response = requests.post(CLAUDE_API_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        return "Error: Unable to fetch response from Claude API."


# 选项：手动调整滑坡因素还是上传文件
option = st.radio(
    "请选择操作方式：",
    ("手动调整滑坡相关因素", "上传文件进行自动判别")
)

if option == "手动调整滑坡相关因素":
    st.sidebar.title("🌍 滑坡易发性因素")
    st.sidebar.write("调整以下滑坡相关因素：")

    # 模拟滑坡易发性因素的滑动条
    precipitation = st.sidebar.slider("降雨量 (mm)", 0, 500, 100)
    soil_type = st.sidebar.selectbox("土壤类型", ["粘土", "砂土", "壤土", "砾土"])
    slope_angle = st.sidebar.slider("坡度角 (度)", 0, 90, 30)
    vegetation_cover = st.sidebar.slider("植被覆盖率 (%)", 0, 100, 50)

    # 显示滑坡易发性相关信息
    st.write("### 🌍 滑坡易发性因素分析")
    st.write(f"**降雨量**: {precipitation} mm")
    st.write(f"**土壤类型**: {soil_type}")
    st.write(f"**坡度角**: {slope_angle} 度")
    st.write(f"**植被覆盖率**: {vegetation_cover} %")

    # 结合滑坡相关因素生成的解释
    st.write("### 📊 基于滑坡因素的解释")
    explanation = (
        f"在降雨量为 {precipitation} 毫米、坡度为 {slope_angle} 度、"
        f"{soil_type} 土壤和 {vegetation_cover}% 的植被覆盖率下，"
        f"滑坡易发性可能较高。增加降雨量或减少植被覆盖率可能会进一步提高滑坡风险。"
    )
    st.write(explanation)

elif option == "上传文件进行自动判别":
    st.write("### 📂 上传包含地形、降雨等数据的文件")
    uploaded_file = st.file_uploader("选择 CSV 或 TXT 文件", type=["csv", "txt"])

    if uploaded_file is not None:
        try:
            # 尝试读取CSV或TXT文件
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.txt'):
                data = pd.read_csv(uploaded_file, delimiter='\t')

            st.write("### 文件内容")
            st.write(data)

            # 假设文件包含以下列：'降雨量', '土壤类型', '坡度角', '植被覆盖率'
            if all(col in data.columns for col in ['降雨量', '土壤类型', '坡度角', '植被覆盖率']):
                # 计算滑坡风险
                avg_precipitation = data['降雨量'].mean()
                max_slope_angle = data['坡度角'].max()
                avg_vegetation_cover = data['植被覆盖率'].mean()

                st.write("### 自动判别结果")
                st.write(f"**平均降雨量**: {avg_precipitation} mm")
                st.write(f"**最大坡度角**: {max_slope_angle} 度")
                st.write(f"**平均植被覆盖率**: {avg_vegetation_cover} %")

                # 自动生成解释
                st.write("### 📊 自动生成的滑坡风险解释")
                explanation = (
                    f"根据上传的数据，平均降雨量为 {avg_precipitation} 毫米，最大坡度角为 {max_slope_angle} 度，"
                    f"平均植被覆盖率为 {avg_vegetation_cover}%。这些因素表明滑坡风险较高。"
                )
                st.write(explanation)
            
            else:
                st.error("文件中缺少必要的列：'降雨量', '土壤类型', '坡度角', '植被覆盖率'。请检查文件格式。")

        except Exception as e:
            st.error(f"文件处理出错：{e}")

# 聊天框让用户输入问题
st.write("### 🤖 输入与滑坡相关的问题：")
user_input = st.text_input("请输入您的问题")

# 当用户输入问题时，调用 Claude API 并显示响应
if user_input and API_KEY:
    st.write("##### Claude 的回复：")
    response = get_claude_response(user_input)
    st.write(response)
