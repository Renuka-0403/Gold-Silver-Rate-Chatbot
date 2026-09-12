import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    st.error("HF_TOKEN is missing. Add your Hugging Face token to the .env file.")
    st.stop()

MODEL = "openai/gpt-oss-120b"
API_URL = "https://api.oropocket.com/public/prices"
client = InferenceClient(api_key=HF_TOKEN)

st.set_page_config(page_title="AI Gold & Silver Assistant", page_icon="✦", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.stApp{background:radial-gradient(circle at 8% 8%,rgba(255,213,79,.20),transparent 25%),radial-gradient(circle at 90% 12%,rgba(109,171,255,.18),transparent 27%),linear-gradient(135deg,#f9fbff 0%,#f7f5ff 50%,#fffdf7 100%)}
.block-container{padding-top:2rem;padding-bottom:2rem;max-width:1450px}
.hero{position:relative;overflow:hidden;border-radius:28px;padding:28px 32px;margin-bottom:22px;background:linear-gradient(120deg,rgba(255,255,255,.96),rgba(255,248,225,.92),rgba(239,247,255,.96));border:1px solid rgba(255,255,255,.9);box-shadow:0 16px 45px rgba(31,41,55,.08)}
.hero:before{content:"";position:absolute;width:240px;height:240px;right:-70px;top:-100px;border-radius:50%;background:rgba(255,197,61,.18);filter:blur(8px)}
.hero-title{position:relative;font-size:42px;line-height:1.05;font-weight:800;color:#16213e;margin:0}
.gold-text{color:#d99000}.silver-text{color:#56789e}
.hero-subtitle{position:relative;margin-top:10px;color:#647089;font-size:15px}
.live-pill{position:absolute;right:30px;top:30px;padding:9px 15px;border-radius:999px;background:#e9faef;border:1px solid #c8efd6;color:#13834b;font-size:13px;font-weight:700}
.live-dot{display:inline-block;width:8px;height:8px;background:#18a957;border-radius:50%;margin-right:7px;box-shadow:0 0 0 5px rgba(24,169,87,.10)}
.metal-card{position:relative;overflow:hidden;min-height:360px;border-radius:26px;padding:28px;border:1px solid rgba(255,255,255,.9);box-shadow:0 18px 45px rgba(31,41,55,.10)}
.gold-card{background:radial-gradient(circle at 82% 45%,rgba(255,193,7,.30),transparent 28%),linear-gradient(135deg,#fff8df,#fff1b8 52%,#fffaf0)}
.silver-card{background:radial-gradient(circle at 82% 45%,rgba(113,168,226,.26),transparent 28%),linear-gradient(135deg,#f2f7ff,#e4efff 52%,#f8fbff)}
.metal-label{font-size:23px;font-weight:800;color:#17213b}
.metal-price{margin-top:16px;font-size:38px;line-height:1;font-weight:800;color:#101828}
.metal-unit{margin-top:9px;color:#68748a;font-size:13px}
.metal-sell{margin-top:20px;font-size:15px;color:#4f596b}
.metal-sell b{color:#17213b}
.change-up{margin-top:13px;color:#11945a;font-weight:700}
.change-down{margin-top:13px;color:#d13c4d;font-weight:700}
.gold-art,.silver-art{position:absolute;right:20px;bottom:18px;width:250px;height:230px}
.gold-bar{position:absolute;right:45px;top:30px;width:105px;height:62px;border-radius:10px 10px 15px 15px;transform:rotate(-13deg) skewX(-8deg);background:linear-gradient(135deg,#fff4a8 0%,#ffd447 30%,#e8a500 58%,#fff0a1 82%,#d78b00 100%);border:2px solid rgba(164,104,0,.35);box-shadow:0 17px 22px rgba(161,101,0,.25),inset 4px 4px 10px rgba(255,255,255,.65);animation:floatBar 4s ease-in-out infinite}
.gold-bar:after{content:"FINE GOLD";position:absolute;left:24px;top:24px;font-size:8px;font-weight:800;color:rgba(108,68,0,.65);letter-spacing:1px}
.gold-ring{position:absolute;right:82px;bottom:48px;width:83px;height:83px;border-radius:50%;border:17px solid #e9ad16;box-shadow:inset 3px 3px 7px rgba(255,255,255,.8),5px 9px 15px rgba(155,95,0,.25);transform:rotate(-20deg)}
.gold-ring:after{content:"";position:absolute;width:25px;height:25px;left:12px;top:-22px;transform:rotate(45deg);border-radius:5px;background:linear-gradient(135deg,#35b98c,#087d61);box-shadow:0 0 12px rgba(22,167,122,.4)}
.gold-coin{position:absolute;width:57px;height:57px;border-radius:50%;background:radial-gradient(circle at 30% 28%,#fff4a0 0 8%,transparent 9%),radial-gradient(circle,#ffd94d 0%,#f2ad00 55%,#c98200 100%);border:4px solid #d99a00;box-shadow:inset 0 0 0 4px rgba(255,241,157,.55),8px 12px 15px rgba(126,81,0,.22);animation:coinFloat 3.5s ease-in-out infinite}
.gold-coin:after{content:"◆";position:absolute;left:17px;top:13px;color:rgba(125,76,0,.48);font-size:20px}
.coin-one{right:8px;bottom:30px}.coin-two{right:138px;bottom:16px;width:47px;height:47px;animation-delay:.7s}.coin-three{right:12px;bottom:112px;width:43px;height:43px;animation-delay:1.2s}
.gold-necklace{position:absolute;left:35px;bottom:20px;width:120px;height:54px;border-bottom:8px dotted #e0a20b;border-radius:0 0 80px 80px;transform:rotate(7deg);opacity:.85}
.silver-bar{position:absolute;right:55px;top:35px;width:108px;height:65px;border-radius:10px 10px 16px 16px;transform:rotate(12deg) skewX(7deg);background:linear-gradient(135deg,#fff 0%,#cfd9e4 28%,#8d9dad 55%,#f8fbff 80%,#9ba9b8 100%);border:2px solid rgba(84,105,128,.28);box-shadow:0 17px 23px rgba(57,76,96,.22),inset 4px 4px 10px rgba(255,255,255,.8);animation:floatBar 4.5s ease-in-out infinite}
.silver-bar:after{content:"FINE SILVER";position:absolute;left:25px;top:25px;font-size:8px;font-weight:800;color:rgba(48,65,82,.65);letter-spacing:1px}
.silver-coin{position:absolute;width:55px;height:55px;border-radius:50%;background:radial-gradient(circle at 30% 25%,#fff,transparent 12%),linear-gradient(135deg,#f9fcff,#c3ceda 50%,#7c8998);border:4px solid #98a7b6;box-shadow:inset 0 0 0 4px rgba(255,255,255,.6),8px 12px 15px rgba(50,65,80,.20);animation:silverSpin 5s linear infinite}
.silver-coin:after{content:"✦";position:absolute;left:18px;top:13px;color:#6d7c8d;font-size:20px}
.silver-one{right:10px;bottom:28px}.silver-two{right:132px;bottom:16px;width:47px;height:47px;animation-delay:1s}
.silver-ring{position:absolute;left:30px;bottom:40px;width:88px;height:88px;border-radius:50%;border:16px solid #aebac7;box-shadow:inset 3px 3px 7px rgba(255,255,255,.9),5px 9px 15px rgba(56,72,90,.20);transform:rotate(16deg)}
.silver-ring:after{content:"";position:absolute;width:25px;height:25px;left:14px;top:-21px;transform:rotate(45deg);border-radius:5px;background:linear-gradient(135deg,#8dd3ff,#4676d7);box-shadow:0 0 12px rgba(74,129,218,.35)}
@keyframes coinFloat{0%,100%{transform:translateY(0) rotateY(0deg)}50%{transform:translateY(-10px) rotateY(180deg)}}
@keyframes silverSpin{0%{transform:rotateY(0deg) translateY(0)}50%{transform:rotateY(180deg) translateY(-7px)}100%{transform:rotateY(360deg) translateY(0)}}
@keyframes floatBar{0%,100%{transform:rotate(-13deg) translateY(0)}50%{transform:rotate(-9deg) translateY(-8px)}}
.section-title{font-size:24px;font-weight:800;color:#17213b;margin:26px 0 13px}
.snapshot-card{border-radius:19px;padding:19px;min-height:125px;border:1px solid rgba(255,255,255,.9);box-shadow:0 10px 28px rgba(31,41,55,.06)}
.snapshot-gold{background:linear-gradient(135deg,#fffaf0,#fff0b8)}.snapshot-silver{background:linear-gradient(135deg,#f8fbff,#e6f0ff)}.snapshot-purple{background:linear-gradient(135deg,#fbf6ff,#f0e7ff)}.snapshot-green{background:linear-gradient(135deg,#f2fff9,#e2f7ed)}
.snapshot-title{font-size:13px;color:#697386}.snapshot-value{margin-top:8px;font-size:23px;font-weight:800;color:#17213b}
.ai-bubble{margin-top:18px;padding:17px;border-radius:18px 18px 18px 5px;background:linear-gradient(135deg,#f1f5ff,#f7f2ff);border:1px solid #e0e6ff;color:#35415a;line-height:1.6}
.ai-badge{display:inline-block;margin-bottom:8px;font-weight:800;color:#4c63bd}
.footer-banner{margin-top:25px;border-radius:24px;padding:25px;text-align:center;background:radial-gradient(circle at 50% 20%,rgba(255,210,80,.22),transparent 35%),linear-gradient(135deg,#fff8e7,#f2eeff,#eef8ff);border:1px solid rgba(255,255,255,.9);box-shadow:0 12px 30px rgba(31,41,55,.06)}
.footer-title{font-size:22px;font-weight:800;color:#273253}.footer-text{color:#737d91;margin-top:5px;font-size:13px}
.stButton>button{border-radius:14px;border:1px solid #e1e6ef;background:rgba(255,255,255,.85);color:#24304a;font-weight:700;min-height:46px;transition:all .2s ease}
.stButton>button:hover{transform:translateY(-2px);border-color:#b8c7e6;box-shadow:0 7px 20px rgba(45,75,125,.12)}
[data-testid="stChatInput"]{border-radius:18px}
#MainMenu{visibility:hidden}footer{visibility:hidden}header{background:transparent!important}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=30)
def fetch_live_prices():
    response = requests.get(API_URL, timeout=8)
    if response.status_code == 429:
        raise RuntimeError("The live price API has temporarily rate-limited requests. Please wait a few seconds and try again.")
    response.raise_for_status()
    result = response.json()
    if "data" not in result:
        raise RuntimeError("Unexpected API response.")
    return result["data"]

def get_live_metal_rates(metal="both", grams=None):
    data = fetch_live_prices()
    result = {"status":"success","currency":"INR","unit":"gram","timestamp":data.get("timestamp")}
    if metal in ["gold","both"]:
        result["gold"] = data["gold"]
    if metal in ["silver","both"]:
        result["silver"] = data["silver"]
    if grams is not None:
        try:
            grams = float(grams)
            if grams <= 0:
                return {"status":"error","message":"Grams must be greater than zero."}
            result["quantity_calculation"] = {}
            if "gold" in result:
                result["quantity_calculation"]["gold"] = {"grams":grams,"buy_value":round(data["gold"]["buy"]*grams,2),"sell_value":round(data["gold"]["sell"]*grams,2)}
            if "silver" in result:
                result["quantity_calculation"]["silver"] = {"grams":grams,"buy_value":round(data["silver"]["buy"]*grams,2),"sell_value":round(data["silver"]["sell"]*grams,2)}
        except (ValueError,TypeError):
            return {"status":"error","message":"Invalid quantity."}
    return result

tools = [{
    "type":"function",
    "function":{
        "name":"get_live_metal_rates",
        "description":"Fetch the current gold and silver tradeable buy and sell quotes in Indian rupees per gram. Use this function whenever the user asks for current gold or silver prices, comparisons, 24-hour changes, or the value of a quantity.",
        "parameters":{
            "type":"object",
            "properties":{
                "metal":{"type":"string","enum":["gold","silver","both"],"description":"The metal requested by the user."},
                "grams":{"type":["number","null"],"description":"Optional quantity in grams."}
            },
            "required":["metal","grams"]
        }
    }
}]

system_message = {
    "role":"system",
    "content":"You are the AI Gold & Silver Assistant. You provide current gold and silver tradeable quotes using the live data function. Never invent current prices. Whenever the user asks for current prices, comparisons, 24-hour changes, or quantity calculations, call get_live_metal_rates. The API provides INR per gram buy and sell quotes. Explain the difference between buying and selling when useful. Do not call the data an official Chennai rate, MCX rate, LBMA benchmark, or universal spot price. Keep answers clear and useful."
}

if "messages" not in st.session_state:
    st.session_state.messages = [system_message]

try:
    prices = fetch_live_prices()
except Exception:
    prices = None

st.markdown("""
<div class="hero">
<div class="hero-title">AI <span class="gold-text">Gold</span> & <span class="silver-text">Silver</span> Assistant</div>
<div class="hero-subtitle">Live precious-metal intelligence powered by AI function calling</div>
<div class="live-pill"><span class="live-dot"></span>LIVE MARKET DATA</div>
</div>
""", unsafe_allow_html=True)

if prices is None:
    st.error("Live market data could not be loaded. Please refresh the application.")
    st.stop()

gold = prices["gold"]
silver = prices["silver"]
gold_change = float(gold["change24h"]["buy"])
silver_change = float(silver["change24h"]["buy"])
gold_change_class = "change-up" if gold_change >= 0 else "change-down"
silver_change_class = "change-up" if silver_change >= 0 else "change-down"
gold_arrow = "▲" if gold_change >= 0 else "▼"
silver_arrow = "▲" if silver_change >= 0 else "▼"

left,right = st.columns(2,gap="large")

with left:
    st.markdown(f"""
<div class="metal-card gold-card">
<div class="metal-label">Gold</div>
<div class="metal-price">₹{gold["buy"]:,.2f}</div>
<div class="metal-unit">Buy rate · per gram</div>
<div class="metal-sell">Sell: <b>₹{gold["sell"]:,.2f}</b></div>
<div class="{gold_change_class}">{gold_arrow} {abs(gold_change):.2f}% · 24h</div>
<div class="gold-art">
<div class="gold-bar"></div>
<div class="gold-ring"></div>
<div class="gold-necklace"></div>
<div class="gold-coin coin-one"></div>
<div class="gold-coin coin-two"></div>
<div class="gold-coin coin-three"></div>
</div>
</div>
""", unsafe_allow_html=True)

with right:
    st.markdown(f"""
<div class="metal-card silver-card">
<div class="metal-label">Silver</div>
<div class="metal-price">₹{silver["buy"]:,.2f}</div>
<div class="metal-unit">Buy rate · per gram</div>
<div class="metal-sell">Sell: <b>₹{silver["sell"]:,.2f}</b></div>
<div class="{silver_change_class}">{silver_arrow} {abs(silver_change):.2f}% · 24h</div>
<div class="silver-art">
<div class="silver-bar"></div>
<div class="silver-ring"></div>
<div class="silver-coin silver-one"></div>
<div class="silver-coin silver-two"></div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Market Snapshot</div>', unsafe_allow_html=True)

s1,s2,s3,s4 = st.columns(4)

with s1:
    st.markdown(f'<div class="snapshot-card snapshot-gold"><div class="snapshot-title">Gold · 10g Buy</div><div class="snapshot-value">₹{gold["buy"]*10:,.2f}</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown(f'<div class="snapshot-card snapshot-silver"><div class="snapshot-title">Silver · 10g Buy</div><div class="snapshot-value">₹{silver["buy"]*10:,.2f}</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown(f'<div class="snapshot-card snapshot-purple"><div class="snapshot-title">Gold GST · gram</div><div class="snapshot-value">₹{gold["gst"]:,.2f}</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown(f'<div class="snapshot-card snapshot-green"><div class="snapshot-title">Silver GST · gram</div><div class="snapshot-value">₹{silver["gst"]:,.2f}</div></div>', unsafe_allow_html=True)

st.caption(f"Live API timestamp: {prices['timestamp']}")

st.markdown('<div class="section-title">Quick Questions</div>', unsafe_allow_html=True)

q1,q2,q3,q4 = st.columns(4)
quick_question = None

with q1:
    if st.button("Gold rate",use_container_width=True):
        quick_question = "What is the current gold rate?"
with q2:
    if st.button("Silver rate",use_container_width=True):
        quick_question = "What is the current silver rate?"
with q3:
    if st.button("Compare",use_container_width=True):
        quick_question = "Compare the current gold and silver rates."
with q4:
    if st.button("10g value",use_container_width=True):
        quick_question = "What is the current value of 10 grams of gold?"

st.markdown('<div class="section-title">Chat with AI</div>', unsafe_allow_html=True)

if len(st.session_state.messages) == 1:
    st.markdown("""
<div class="ai-bubble">
<div class="ai-badge">✦ AI Assistant</div><br>
Ask me about current gold and silver rates, compare the two metals, or calculate the value of a specific quantity.
<br><br>
Try: <b>"I have ₹50,000. How much gold can I buy?"</b>
</div>
""", unsafe_allow_html=True)

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    elif message["role"] == "assistant" and message.get("content"):
        with st.chat_message("assistant"):
            st.write(message["content"])

user_input = st.chat_input("Ask about gold, silver, prices, comparisons or quantities...")

if quick_question:
    user_input = quick_question

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Checking live market data..."):
            try:
                response = client.chat_completion(model=MODEL,messages=st.session_state.messages,tools=tools,tool_choice="auto",max_tokens=700)
                assistant_message = response.choices[0].message
                tool_calls = assistant_message.tool_calls
                if tool_calls:
                    assistant_tool_calls = []
                    for call in tool_calls:
                        assistant_tool_calls.append({"id":call.id,"type":"function","function":{"name":call.function.name,"arguments":call.function.arguments}})
                    st.session_state.messages.append({"role":"assistant","content":assistant_message.content or "","tool_calls":assistant_tool_calls})
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)
                        if function_name == "get_live_metal_rates":
                            result = get_live_metal_rates(metal=arguments.get("metal","both"),grams=arguments.get("grams"))
                        else:
                            result = {"status":"error","message":"Unknown function."}
                        st.session_state.messages.append({"role":"tool","tool_call_id":tool_call.id,"name":function_name,"content":json.dumps(result)})
                    final_response = client.chat_completion(model=MODEL,messages=st.session_state.messages,max_tokens=700)
                    answer = final_response.choices[0].message.content
                else:
                    answer = assistant_message.content or "I could not generate a response."
                st.session_state.messages.append({"role":"assistant","content":answer})
                st.write(answer)
            except Exception as error:
                st.error(f"Something went wrong: {error}")

st.markdown("""
<div class="footer-banner">
<div class="footer-title">Precious metals today. Stronger tomorrow.</div>
<div class="footer-text">Live data · AI function calling · Gold & Silver intelligence</div>
</div>
""", unsafe_allow_html=True)