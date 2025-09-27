# John-Kurisko-s-Three-Scalping-Setups
John Kurisko's Three Scalping Setup and Trading Business Plan
Below The source provides excerpts from a video featuring professional scalper John Kurisko, who discusses his disciplined approach to trading and three specific setups he uses to generate income. Kurisko stresses that successful trading is a business that requires discipline, patience, and a well-defined business plan, asserting that most traders fail due to lack of these qualities. He details his proprietary system, which combines stochastic oscillator divergences with a "quad rotation" indicator—four different stochastic bands—to identify high-probability trades, such as the "Holy Grail setup," which combines a quad rotation with a divergence. Kurisko also describes two other setups, the "20/20 bull flag" and a "bear flag," which use stochastic rotation and embedded stochastic levels for trade entries and exits, highlighting the importance of having a robust exit strategy to avoid gambling.


This workflow details the algorithmic implementation of the trading setups taught by John Kurisko (DayTraderRockStar), focusing on precise entry, exit, and risk management criteria derived from his described 'Business Plan for Traders'.
For a code generation model, each step is broken down into verifiable conditions, calculations, or defined actions.

--------------------------------------------------------------------------------
ALGO TRADING WORKFLOW: JOHN KURISKO SETUPS


# README.md: Algorithmic Trading Blueprint (John Kurisko Setups)

## PROJECT: Algorithmic Implementation of DayTraderRockStar Strategies

This document provides a precise, step-by-step workflow for the proprietary trading methodologies developed by John Kurisko (DayTraderRockStar). These strategies are derived from his "Business Plan for Traders" and focus on discipline, patience, and waiting for high-probability setups.

The goal is to generate complete, ready-to-deploy algorithmic trading code based exclusively on the established rules for Order Entry Criteria, Profit Exit Criteria, and Automatic Stop Criteria.

---

## 1. INSTRUCTION FOR CODE GENERATION BOT (JOULE)

JOULE is instructed to create executable trading strategies for the three primary setups detailed below. The code must strictly enforce all preconditions and use the specified indicator settings and risk management rules.

**Mandatory Requirement:** All entries must be defined based on the signals generated on the **1-Minute (1M) or 5-Minute (5M) timeframes**.

---

## 2. SYSTEM CONFIGURATION AND INDICATORS

The system relies heavily on the interaction of multiple Exponential Moving Averages (EMAs) and a proprietary four-band setup of the Stochastic Oscillator, known as the Quad Rotation.

| Component | Indicator | Settings | Role/Notes | Source |
| :--- | :--- | :--- | :--- | :--- |
| **Timeframes** | Execution | 1 Minute (1M) and 5 Minute (5M) | Used for scalping executions. | |
| **Moving Averages** | EMA | 20, 50, 200 Periods | Trend context and entry/hold reference. | |
| **Stochastics (Quad Rotation)** | Fast Stoch | (9, 3) | Primary trigger/Momentum indicator. | |
| | Medium Stoch 1 | (14, 3) | Second component of Quad Rotation. | |
| | Medium Stoch 2 | (40, 4) | Third component of Quad Rotation. | |
| | Slow/Embedded Stoch | (60, 10, 10) | Represents the 5-Minute timeframe internal momentum; defines embedded trend strength. | |
| **Stochastic Levels** | Boundary Lines | 20 (Oversold), 80 (Overbought) | Used for divergence and flag rotation confirmation. | |
| **Volume Indicator** | VWAP | Default Settings | Secondary tool for playbook. | |
| **Stoch Line Used** | D-Line | The Signal Line (Percentage D-line) | Used for all stochastic readings. | |

---

## 3. STRATEGY 1: SUPER SIGNAL / QUAD DIVERGENCE (HOLY GRAIL BUY SETUP)

This setup is deemed the "Holy Grail" due to its high probability (up to 95%) and is a merger of the Quad Rotation and a Stochastic Price Divergence (Buy Side Divergence Lower Low Entry).

### Step-by-Step Instructions for JOULE (Long Entry)

#### A. Pre-Entry Setup Environment
1.  **Trend Context:** Identify if price action is in an identifiable upward trend or a defined channel.
2.  **Channel Confirmation:** (Optional but Recommended) The divergence signal is strongest when aligned with lower channel lines (trend line). Identify a downward channel pullback using the 1-2-3 Pattern (requires three pivots).

#### B. Divergence Setup (Stochastic Stages)
| Step | Code Logic / Condition | Source |
| :--- | :--- | :--- |
| **1. Quad Rotation Trigger (L1)** | **IF** all four stochastic bands (9/3, 14/3, 40/4, 60/10/10) drop simultaneously **under the 20 line** (oversold). **THEN** record the low price of the current candle as **Low 1 (L1)**. | |
| **2. Initial Bounce** | **IF** L1 is followed by a bounce in price and the Fast Stochastic (9/3) moves back **above the 20 line**. | |
| **3. Price Retest (L2)** | **IF** Price subsequently drops again, forming a new low, **Low 2 (L2)**, which is either **lower than L1 or a double bottom** to L1. | |
| **4. Divergence Confirmation** | **CRITICAL IF:** At the formation of L2, the Fast Stochastic (9/3) must put in a **higher low** compared to the stochastic reading during L1 AND subsequently **turn up above the 20 line**. | |
| **5. Entry Signal** | **ACTION:** Execute a **Long Trade** immediately upon the **visual confirmation** (turn back up) of the Fast Stochastic (9/3), activating the divergence signal. | |

#### C. Risk Management (Stop Loss)
1.  **Stop Placement:** Automatically place the stop loss **one to two ticks under the pattern low candle (L2)**. This automatically defines the risk.
2.  **Position Sizing:** Since this is a Super Signal/Holy Grail setup, a larger position size is warranted. (Refer to Business Plan Rule 5 for increasing position size).

---

## 4. STRATEGY 2: BULL FLAG BUY SETUP (20-20 FLAG)

This is a continuation pattern utilized when the larger trend is strong. The setup is confirmed by the "embedded" stochastic (60/10).

### Step-by-Step Instructions for JOULE (Long Entry)

#### A. Pre-Entry Trend Confirmation
1.  **Flagpole:** Price must have moved aggressively up off the 20 EMA, indicating a steep move (flagpole).
2.  **Embedded Stochastic Check:** **IF** the Slow Stochastic (60/10/10), representing the 5M timeframe, is **holding above 80**. **Note:** Preferably, this stochastic should be near 85 or 90 to indicate a stronger trend.

#### B. Entry Criteria (20-20 Condition)
| Step | Code Logic / Condition | Source |
| :--- | :--- | :--- |
| **1. Price Pullback** | **IF** Price pulls back and successfully holds **on or above the 20 EMA**. | |
| **2. Stochastic Rotation** | **IF** the Fast Stochastic (9/3) rotates quickly back down and approaches or **touches the 20 line** (oversold). | |
| **3. Entry Signal** | **ACTION:** Execute a **Long Trade** when the Fast Stochastic (9/3) gets close to or **touches the 20 line**. | |

#### C. Risk Management and Exit Strategy
1.  **Partial Profit Exit:** **ACTION:** Take partial profits as the Fast Stochastic (9/3) **crosses back above 80**.
2.  **Stop Management:** **ACTION:** Move the stop loss to **break even** on any additional shares remaining after partial profit taking.

---

## 5. STRATEGY 3: BEAR FLAG SHORT SETUP

This is the inverse continuation pattern, utilized in a strong downtrend.

### Step-by-Step Instructions for JOULE (Short Entry)

#### A. Pre-Entry Trend Confirmation
1.  **Embedded Stochastic Check:** **IF** the Slow Stochastic (60/10/10) is **holding under 20** (e.g., stuck around the bottom/below 25-30). This confirms the larger trend is down.

#### B. Entry Criteria (80-20 Condition)
| Step | Code Logic / Condition | Source |
| :--- | :--- | :--- |
| **1. Price Rally/Pullback** | **IF** Price pulls back (rallies) and successfully holds **on or below the 20 EMA**. | |
| **2. Stochastic Rotation** | **IF** the Fast Stochastic (9/3) rotates quickly back up and approaches or **touches the 80 line** (overbought). | |
| **3. Entry Signal** | **ACTION:** Execute a **Short Trade** as the Fast Stochastic (9/3) gets close to or **touches the 80 line**. | |

#### C. Risk Management and Exit Strategy
1.  **Partial Profit Exit:** **ACTION:** Take partial profits as the Fast Stochastic (9/3) **crosses back below 20**.
2.  **Stop Management:** **ACTION:** Move the stop loss to **break even** on any additional shares remaining after partial profit taking.

---

## 6. SECONDARY RISK MANAGEMENT: COUNTER-TREND EXIT RULE

This rule must be applied to any counter-trend trade (e.g., buying in a confirmed downtrend) to protect the position from continued strong trend movement.

| Step | Code Logic / Condition | Source |
| :--- | :--- | :--- |
| **1. Confirmation of Downtrend** | **IF** The main trend is down (e.g., price is underneath the 200 EMA) AND the Slow Stochastic (60/10) is **stuck under 20** (embedded). | |
| **2. Counter-Trend Entry** | **IF** A counter-trend BUY signal (such as a Quad Rotation) is taken. | |
| **3. Immediate Exit Signal** | **ACTION (Exit Signal):** If the 60/10 Stochastic remains embedded under 20, the algorithm must **sell/exit the long trade** immediately when the Fast Stochastic (9/3) rotates back up to and crosses **above 80**. | |
| **Reason:** | This signal (9/3 hitting 80 while 60/10 is embedded under 20) confirms the Bear Flag setup, indicating the bounce is finished and the dominant trend is resuming. | |
