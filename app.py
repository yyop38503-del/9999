import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import json

# ==========================================
# 1. 偵測環境與設定連結
# ==========================================
@st.cache_data(ttl=60)
def fetch_data_from_sheets():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    SPREADSHEET_NAME = "物流查詢系統"
    
    try:
        # 判斷是在「雲端」還是「本地」
        if "gcp_service_account" in st.secrets:
            # 這是雲端環境，讀取 Secrets
            creds_info = st.secrets["gcp_service_account"]
            creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
        else:
            # 這是本機環境，讀取 key.json
            creds = Credentials.from_service_account_file("key.json", scopes=SCOPES)
            
        client = gspread.authorize(creds)
        spreadsheet = client.open(SPREADSHEET_NAME)
        worksheet = spreadsheet.get_worksheet(0)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"❌ 連線錯誤：{e}")
        return None

# ==========================================
# 2. 網頁前端畫面設計 (與你原本的一樣)
# ==========================================
st.set_page_config(page_title="買家物流狀態查詢系統", page_icon="📦", layout="centered")
st.title("📦 買家物流狀態查詢系統")

df = fetch_data_from_sheets()

if df is not None:
    buyer_name = st.text_input("👤 請輸入您的買家姓名：").strip()
    if buyer_name:
        search_result = df[df['買家姓名'].astype(str).str.strip() == buyer_name]
        if not search_result.empty:
            for index, row in search_result.iterrows():
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                col1.metric("🛍️ 商品名稱", str(row.get('商品欄', '無')))
                col2.metric("⏳ 待運回商品", str(row.get('待運回商品', '無')))
                status = str(row.get('已交易完畢的商品', ''))
                col3.markdown("### 狀態" + ("\n✅ **已交易完畢**" if status == "是" else "\n🚚 **處理中**"))
        else:
            st.warning("🔍 找不到資料，請確認名字是否正確。")
