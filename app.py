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
        "private_key_id": "3df6618313bf47f80604ea348da1aec3bb1e5dd0",
        # 使用 r''' ''' 包住金鑰，這樣裡面的所有換行符號都會被保留，不會出錯
        "private_key": r'''-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQColLMbFBCcoKne\niV29onwkfFwID+aMo+yug0Rs477okWKdHGeeDFZ19Wza59CEyher5RVzBgap+OOx\naOtMw1De6OUTCvVJL0Z3Wm5uR1lLsVVjMumqjNhYDfoinVCEW7Uc3KDK4xmd0Usy\ndLrPyii+0cweAVb4Q0BI1heNAydjhIFroNibNzjSlR8ZfEqb4J6K6zLWishoeRps\nEfV2QsyYXR0INi3wDgiQccPQBjkXsjs9/uHcBpmY5lEWsJkWqzKfvFtlAhPSY/sc\nMoiKaYvdtGEhOILES465YNPYdDaGqut0MQGSQgQB3qTS1jGA6eP3oyMwFB5XlTvK\nLR9RLDNvAgMBAAECggEARpYkvHTVU8/N8LkRwCJ12o0bt+B4h3Dn3FZoYzOlLxoY\n8XIATOQbm76MusgPvlokOTxtk8D1L1xgcltdEsJBbWSU7jlLZT5fQgBidth3IkN5\nXlTmFBxvRcdscevu18zSc+hJh0o54qPM2a6YvgKGtwd/cRzcfo0iMJ08NTYZ2wfl\ndIe+OCljsoj5GMEoDj3pcjwU9gUBmY5TG5uZQGuvSr0r1BkJWTa1Frq7oEm24GBx\n1oYIQYyadGEVN0THMKW6YHqL9IoesniTyalpfH9/MlvZIPlYPDGtlFsZ8zbyGzpv\nmRvszXK6GHc84RoNk7EBPdFb/1JCV7Ja9G8ajxHjqQKBgQDQAgHb3FMA2nayQuVv\nYTvLlyjauNl8upn58uaLSFcJo8i65aTJvRaJuGE+gZPU4yiK5mBXaUvykVRuxx/U\nPmlEB7RDpFQXeeVmCWgUo/uXOcsXxI6++q8W9gyEku/gOfnNsKH+TkagPCLMlLxk\nqmWhPY4MdaBb1IMW7SxcoFb9UwKBgQDPee+Qqzq4K6WF+5Oq5o00pSzX7H28uVs+\nkdRDeQVV1pUMu9/YU1HRK1Z58+U2aGU1xHaTtN+wYKOfV9vwRvBW5C+Ry5NImwlS\nhtMLIDIMBTajk3n/cTDUqXQQJdrcj/yqPIr+I/De6jBVgrnv77pQahIDDAE9JLze\nsRS79BnR9QKBgHoTE4Ay18vCarLHq9soF22uct2aaplW8hLMyRypAdu4cY+uQn3b\nKST+PqPubBIelqad+aCTPW1IeWLiHf3z+tdgJh0kje2RLl4p2xlx+6+OzXBPfO78\nNFGnaUVM7taLb92VchzLV4umf03NZJs3nZl5hKovRkNefuivnL9nomXdAoGAZQRk\nnRaRt3wg0nRkOJCabeiCRftyWQISqAtOwy9YZqvc1F9hJK2kp2gnaadTkcMQjDZE\n2bP2OaVD5WBcyMdxW40skBsDchVyW4kjlkYtt+aN7OTwQGw3L0P2K6qSvlMo3SYv\nMoADVjXGJMxKhcU9/Ms4S917eO67Ot4TT1QRgkUCgYBci98QdkWQ6gdzKqruBDuS\nPdXeapIoa5/GdJ0A+1AsUMbkxysRN1wt0dZMyl5VMX90j04mBQ0GyDShBYhUH/ut\nR3MUDv8Nbv2NijffvMKh9uRqooiCZxdlmo7jPe08xlE3rMxYfQnhUWTpKZKwS9S3\neY8HjVGmgB3Qeo3dclDVcw==
-----END PRIVATE KEY-----''',
        "client_email": "mysheets@project-498407.iam.gserviceaccount.com",
        "client_id": "112780949161934201435",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mysheets%40project-498407.iam.gserviceaccount.com",
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
