import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# ==========================================
# 1. 連結 Google 試算表 (直接整合金鑰，最穩定版本)
# ==========================================
@st.cache_data(ttl=60)
def fetch_data_from_sheets():
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 請將下方引號內的內容，替換成你 key.json 裡的實際數值
    creds_info = {
        "type": "service_account",
        "project_id": "project-498407",
        "private_key_id": "8a8b15d2ed4f776f851ddd6b52c7d62ae5351afe",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDax/Srft28R5dEEbmSr+mg2RlvCKyHjf67s6c7MvQ6uJ8ydoVgja50OfMd0bj6gVDuDRy08+T8uBxlHSyZw5cXGRHIIxKyg+GtHiWltZQohGeJxJdTG4stFaZQ3OzfrVC6+lTT+XkwaW68zM6Nhk+Vn1EZmpaKzDJa5JVQGQZCoumbeAAgeUF5a/nMcaQpqi1820tmS6Rt2hHwf26x1O5k614nNEUjfhOLl7QSEd4EDQTw/E5jAGxW7KnXfIo7UIEIhac70/R1FiC0voScIeJ9q7y67qL459y5UWeOjVO7ezi1O3ttkQQXaF/61hs/2pComG5c+ieYKfVakQ1t+Q4lAgMBAAECggEAAd/mo6VYffF1sgARevI8bX2NIP0uFnkPDQ/7qrKjuP2vfLjbKQOVxaOtRsMvBobfCQC+QmB4a0aIyCbRMZEYnvp+3NwZRl1obKzeZ2mjcLRvu0e4TZ5ypkrlWOCHvBC2j7kvSspJF+ZALDVFPzblJ2CzcT8SM3OPKkwdAzZvrgvGWcTOwE6RzycQMfIMlz7XOLfJD0MknYKwBFWX9a8PqTppoYakDg6v3jgnogcYlTVekTCdpSBrZILbfMuxjOrNqbA+oZF6Wsdr5YFZGzoTWeHCKnabo7bhchA2IstmWlSVu7Wyet+GzJSt5CtLZbdDzd5a+L7CJ/O8KWhrImCjEQKBgQD49lzbOnClhCk7ujYxh0oEZlR5R/B+vMthvMQ+tiQO8L+Y5ABmLWM1o5eK51yzryNN7VXK5bBG5Q8GDNYZmUGwDQhdaE9GBTjSF0DOpOk+A+WHo7YR8hmS5R3Xl4/6abBObg0IouFTejswsjakAI+axWQ19JLq5L4X24ZAEQQ69QKBgQDg9y8C7cYuFKNMk1z2FwtEhzHJUjYYJn20ow10MXmw2EWL5ST47LHX0T3i1RR8OooJXWvTaK2GVA0Y/0pO5JeLTgAeCHEi7yhJs8k+t/na2+AgEI3iI/NBfTF9CwJjOJxdDG1jMPum/dVH4RN1DeR9+b4yeyv+rGekWtTaLNnocQKBgQCc4hJti4wEoR2ip5sS5t/7mchNjMm985ZuBpfbtMdQKuFxpOujd6J24JnUTCsch5bFunM/ojHM2vb2pwwboXnFSNEmm16pDw1ZRpHuJflcvPPc34sSD+hGWNy7kIAhFBtbEaGTnMmVdD9pH7z3abUXaY+Ro5OEkduGvyb8pVjNQmafRf0amJLaEghsTUryvSX/oxkuy4TzxkVWKQKBgQDVZAK2335N9YuUtm/GisNIZIkoMxBWxiQVNVksr0WEJxGJCnmQmUx0r+jpAj+lOw32piQCa9e1hILMBFSjExhgrkNUOaO/nmJImNa9vjnVB8lC3hs8HY98zGTz5HOZOs04WCddFMQKBgHssrAF9CW5ucdutLpumrwmHOFFEcWuKgvhgQndYpEGbUCA1tfBN94rtxSwmduQOT0yJwuJ1fIycZHmK/qK+MGsYUug+MTPYuU12ZybUKLqjS8va5Dza4j1MsdB6FuqECwMC9my26AziP3qsR6LhzzYhmqoWLCjR2Ynmi3O2p23\n-----END PRIVATE KEY-----\n",
        "client_email": "mysheets@project-498407.iam.gserviceaccount.com",
        "client_id": "112780949161934201435",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "universe_domain": "googleapis.com"
    }
    
    try:
        creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open("物流查詢系統")
        worksheet = spreadsheet.get_worksheet(0)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"❌ 連結錯誤：{e}")
        return None

# ==========================================
# 2. 前端介面
# ==========================================
st.set_page_config(page_title="買家物流狀態查詢系統", page_icon="📦")
st.title("📦 買家物流狀態查詢系統")

df = fetch_data_from_sheets()

if df is not None:
    buyer_name = st.text_input("👤 請輸入您的買家姓名：").strip()
    if buyer_name:
        search_result = df[df['買家姓名'].astype(str).str.strip() == buyer_name]
        if not search_result.empty:
            for _, row in search_result.iterrows():
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                col1.metric("🛍️ 商品名稱", str(row.get('商品欄', '無')))
                col2.metric("⏳ 待運回商品", str(row.get('待運回商品', '無')))
                status = str(row.get('已交易完畢的商品', ''))
                col3.markdown("### 狀態\n" + ("✅ **已交易完畢**" if status == "是" else "🚚 **處理中**"))
        else:
            st.warning("🔍 找不到該買家資料。")
