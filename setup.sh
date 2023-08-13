mkdir -p ~/.streamlit/
echo "[theme]
primaryColor='#13d457'
backgroundColor='#130b27'
secondaryBackgroundColor='#112233'
textColor='#dae3ea'
font = 'sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml