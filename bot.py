#!/usr/bin/env python3
"""
Quotex Trading Bot - Automated Trading System
"""

import time
import logging
from datetime import datetime
from typing import Dict, Optional
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from quotexapi.api import QuotexAPI
except ImportError:
    logger.error("quotexapi not installed. Install with: pip install quotexapi")
    QuotexAPI = None


class QuotexTradingBot:
    """Main Trading Bot Class"""
    
    def __init__(self, config):
        self.config = config
        self.api = None
        self.is_connected = False
        self.trades_today = 0
        self.loss_today = 0.0
        self.balance = 0
        
    def connect(self) -> bool:
        """Connect to Quotex API"""
        try:
            if QuotexAPI is None:
                logger.error("QuotexAPI not available")
                return False
                
            self.api = QuotexAPI(
                email=self.config.QUOTEX_EMAIL,
                password=self.config.QUOTEX_PASSWORD,
                headless=True
            )
            
            if self.api.connect():
                self.is_connected = True
                self.balance = self.api.get_balance()
                logger.info(f"✅ Connected to Quotex! Balance: ${self.balance}")
                return True
            else:
                logger.error("❌ Failed to connect to Quotex")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection error: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from Quotex"""
        try:
            if self.api:
                self.api.close()
                self.is_connected = False
                logger.info("Disconnected from Quotex")
        except Exception as e:
            logger.error(f"Disconnect error: {str(e)}")
    
    def get_candles(self, asset: str, period: int = 100) -> Optional[pd.DataFrame]:
        """Get historical candles"""
        try:
            if not self.is_connected:
                logger.warning("Not connected to API")
                return None
            
            logger.info(f"Fetching {period} candles for {asset}")
            
            # In real implementation, fetch from API
            # candles = self.api.get_candles(asset, period)
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching candles: {str(e)}")
            return None
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        try:
            rsi = RSIIndicator(close=df['close'], window=period)
            return rsi.rsi()
        except Exception as e:
            logger.error(f"RSI calculation error: {str(e)}")
            return None
    
    def calculate_ma(self, df: pd.DataFrame, period: int) -> pd.Series:
        """Calculate Simple Moving Average"""
        try:
            sma = SMAIndicator(close=df['close'], window=period)
            return sma.sma_indicator()
        except Exception as e:
            logger.error(f"MA calculation error: {str(e)}")
            return None
    
    def analyze_signals(self, df: pd.DataFrame) -> Dict:
        """Analyze trading signals"""
        try:
            if df is None or len(df) < self.config.MA_SLOW:
                return {'signal': 'NO_SIGNAL', 'strength': 0}
            
            # Calculate indicators
            rsi = self.calculate_rsi(df, self.config.RSI_PERIOD)
            ma_fast = self.calculate_ma(df, self.config.MA_FAST)
            ma_slow = self.calculate_ma(df, self.config.MA_SLOW)
            
            if rsi is None or ma_fast is None or ma_slow is None:
                return {'signal': 'NO_SIGNAL', 'strength': 0}
            
            current_rsi = rsi.iloc[-1]
            current_price = df['close'].iloc[-1]
            fast_ma = ma_fast.iloc[-1]
            slow_ma = ma_slow.iloc[-1]
            
            # Buy Signal
            if (current_rsi < self.config.RSI_OVERSOLD and 
                fast_ma > slow_ma):
                logger.info(f"🟢 BUY SIGNAL - RSI: {current_rsi:.2f}, Price: {current_price}")
                return {
                    'signal': 'BUY',
                    'strength': 100 - current_rsi,
                    'rsi': current_rsi,
                    'price': current_price
                }
            
            # Sell Signal
            elif (current_rsi > self.config.RSI_OVERBOUGHT and 
                  fast_ma < slow_ma):
                logger.info(f"🔴 SELL SIGNAL - RSI: {current_rsi:.2f}, Price: {current_price}")
                return {
                    'signal': 'SELL',
                    'strength': current_rsi - 50,
                    'rsi': current_rsi,
                    'price': current_price
                }
            
            else:
                return {
                    'signal': 'NO_SIGNAL',
                    'strength': 0,
                    'rsi': current_rsi
                }
                
        except Exception as e:
            logger.error(f"Signal analysis error: {str(e)}")
            return {'signal': 'NO_SIGNAL', 'strength': 0}
    
    def check_risk_limits(self) -> bool:
        """Check if risk limits are exceeded"""
        if self.trades_today >= self.config.MAX_TRADES_PER_DAY:
            logger.warning(f"⚠️  Max trades per day ({self.config.MAX_TRADES_PER_DAY}) reached")
            return False
        
        if self.loss_today >= self.config.MAX_LOSS_PER_DAY:
            logger.warning(f"⚠️  Max loss per day (${self.config.MAX_LOSS_PER_DAY}) reached")
            return False
        
        return True
    
    def execute_trade(self, signal: str, strength: float) -> bool:
        """Execute a trade"""
        try:
            if not self.is_connected or not self.config.BOT_ENABLED:
                return False
            
            if not self.check_risk_limits():
                return False
            
            if signal == 'BUY':
                logger.info(f"📈 Executing BUY trade - Amount: ${self.config.TRADE_AMOUNT}")
                # self.api.buy(self.config.ASSET, self.config.TRADE_AMOUNT, self.config.TIMEFRAME)
                self.trades_today += 1
                return True
                
            elif signal == 'SELL':
                logger.info(f"📉 Executing SELL trade - Amount: ${self.config.TRADE_AMOUNT}")
                # self.api.sell(self.config.ASSET, self.config.TRADE_AMOUNT, self.config.TIMEFRAME)
                self.trades_today += 1
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Trade execution error: {str(e)}")
            return False
    
    def run(self):
        """Main bot loop"""
        logger.info("🤖 Quotex Trading Bot Started")
        
        if not self.connect():
            logger.error("Failed to connect to Quotex")
            return
        
        try:
            iteration = 0
            while self.config.BOT_ENABLED:
                iteration += 1
                logger.info(f"\n--- Iteration {iteration} ---")
                
                # Get candles
                df = self.get_candles(self.config.ASSET)
                
                if df is not None:
                    # Analyze signals
                    analysis = self.analyze_signals(df)
                    
                    # Execute trade if signal is strong
                    if analysis['signal'] != 'NO_SIGNAL' and analysis['strength'] > 30:
                        if self.config.AUTO_TRADE:
                            self.execute_trade(analysis['signal'], analysis['strength'])
                        else:
                            logger.info(f"📊 Signal detected: {analysis['signal']} (Awaiting manual approval)")
                
                # Update balance
                if self.is_connected:
                    self.balance = self.api.get_balance()
                    logger.info(f"Current Balance: ${self.balance}")
                
                # Sleep before next check
                time.sleep(self.config.SLEEP_TIME)
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Bot error: {str(e)}")
        finally:
            self.disconnect()
            logger.info("🤖 Quotex Trading Bot Stopped")


def main():
    """Main entry point"""
    import config
    
    bot = QuotexTradingBot(config)
    bot.run()


if __name__ == "__main__":
    main()