# Quotex Trading Bot 🤖

एक automated trading bot जो Quotex पर automatically trades करता है।

## Features ✨

✅ RSI और Moving Average indicators  
✅ Automated trading signals  
✅ Risk management system  
✅ Real-time logging  
✅ Error handling  
✅ Daily trade limits  
✅ Stop loss और take profit  

## Installation 📦

```bash
# Clone repository
git clone https://github.com/karan130767/quotexmybot.git
cd quotexmybot

# Install dependencies
pip install -r requirements.txt
```

## Setup 🔧

1. **Copy environment file:**
```bash
cp .env.example .env
```

2. **Edit `.env` file with your credentials:**
```
QUOTEX_EMAIL=your_email@example.com
QUOTEX_PASSWORD=your_password
```

3. **Edit `config.py` with your trading settings**

## Usage 🚀

```bash
python bot.py
```

## Configuration ⚙️

Edit `config.py` to customize:

- `TRADE_AMOUNT` - Trade amount per signal
- `TIMEFRAME` - Chart timeframe (1m, 5m, 15m, 1h)
- `ASSET` - Trading asset (EURUSD, etc)
- `RSI_PERIOD` - RSI indicator period
- `MA_FAST` - Fast moving average period
- `MA_SLOW` - Slow moving average period
- `STOP_LOSS_PERCENT` - Stop loss percentage
- `TAKE_PROFIT_PERCENT` - Take profit percentage
- `MAX_TRADES_PER_DAY` - Maximum trades per day
- `AUTO_TRADE` - Enable/disable automatic trading

## Trading Strategy 📊

Bot uses:
1. **RSI Indicator** - Identifies overbought/oversold conditions
2. **Moving Averages** - Confirms trend direction
3. **Risk Management** - Protects against excessive losses

### Buy Signal:
- RSI < 30 (Oversold) AND
- Fast MA > Slow MA (Uptrend)

### Sell Signal:
- RSI > 70 (Overbought) AND
- Fast MA < Slow MA (Downtrend)

## Logging 📝

All trades और bot activities `trading_bot.log` में save होती हैं।

## Risk Disclaimer ⚠️

```
यह bot automated trading करता है।
हमेशा demo account से शुरुआत करें।
Real money के साथ काम करने से पहले अच्छे से test करें।
Trading में हमेशा risk होता है - सावधानी से use करें।
```

## Troubleshooting 🔍

### Connection Error
- Email/password check करें
- Internet connection verify करें
- Quotex account active है या नहीं check करें

### No Signals
- Candle data check करें
- Indicators properly calculate हो रहे हैं या नहीं
- Logs देखें `trading_bot.log` में

## Contributing 🤝

Issues और improvements के लिए issues create करें।

## License 📄

MIT License

---

**Created by:** karan130767  
**Last Updated:** 2026-06-13