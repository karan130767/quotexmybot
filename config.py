# Quotex Trading Bot Configuration

# Quotex API Credentials
QUOTEX_EMAIL = "your_email@example.com"
QUOTEX_PASSWORD = "your_password"

# Trading Settings
TRADE_AMOUNT = 10  # Amount per trade in USD
TIMEFRAME = "1m"   # Timeframe: 1m, 5m, 15m, 1h
ASSET = "EURUSD"   # Trading asset

# Strategy Settings
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MA_FAST = 9
MA_SLOW = 21

# Risk Management
STOP_LOSS_PERCENT = 2  # Stop loss percentage
TAKE_PROFIT_PERCENT = 3  # Take profit percentage
MAX_TRADES_PER_DAY = 10
MAX_LOSS_PER_DAY = 50  # Maximum loss in USD before stopping

# Bot Settings
BOT_ENABLED = True
LOG_LEVEL = "INFO"
AUTO_TRADE = True  # Set to False for manual approval
SLEEP_TIME = 5  # Seconds between checks