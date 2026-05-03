# Stress Testing Engine with Regime Change Detection

A high-performance C++ engine for stress testing options portfolio strategies with real-time 3D visualization, Hidden Markov Model regime detection, and early warning signals for optimal risk allocation vs. S&P 500 benchmark.

---

## Live 3D Regime Change Visualization

The engine computes a **P&L surface in 3 dimensions** (Spot Price x Implied Volatility x P&L) that **morphs in real-time** as market regimes shift. The surface color, shape, and orientation change as the Hidden Markov Model detects regime transitions -- from smooth green domes in bull markets to inverted red craters during crashes.

### P&L Surface Morphing Through Market Regimes

> The 3D surface rotates and deforms live as the engine cycles through: **Bull Quiet** (green) --> **Transition** (yellow/orange) --> **Bear Volatile / Crisis** (red) --> **Recovery** (blue) --> **New Bull** (green)

![3D P&L Surface - Regime Cycle Animation](docs/img/regime_cycle_3d.gif)

**What you're seeing:**
- **X-Axis**: Spot Price ($) -- the underlying S&P 500 level
- **Y-Axis**: Implied Volatility (%) -- option-implied expected volatility
- **Z-Axis**: P&L ($) -- portfolio profit/loss from Iron Condor strategy
- **Color**: Green = profit zone, Red = loss zone, shifting with regime
- **Bottom bar**: Regime timeline progressing through the full cycle
- **Header**: Current regime, trading signal, and VIX level updating live

| Phase | Surface Shape | VIX | Signal | Cash Allocation |
|-------|--------------|-----|--------|-----------------|
| Bull Quiet | Smooth elevated dome | ~12 | STRONG BUY | 15% |
| Transition | Rippling, tilting surface | ~24 | REDUCE RISK | 40% |
| Bear Volatile | Inverted crater, deep valleys | ~67 | CRISIS | 70% |
| Recovery | Reforming upward slope | ~28 | BUY | 25% |
| New Bull | Smooth dome returns | ~14 | STRONG BUY | 15% |

---

### Early Warning Dashboard

The multi-panel dashboard tracks crisis probability, VIX trajectory, portfolio allocation shifts, and cumulative returns vs. S&P 500 benchmark in real-time. Watch how the system **detects the incoming crash early** and shifts to cash before the drawdown hits.

![Early Warning Dashboard Animation](docs/img/early_warning_dashboard.gif)

**Panels:**
- **Top-Left**: Crisis probability gauge -- rises from 5% to 89% as crash approaches
- **Top-Right**: VIX trajectory -- climbing from 12 past the danger threshold to 67
- **Bottom-Left**: Portfolio allocation bars -- cash increasing, equity decreasing as risk rises
- **Bottom-Right**: Cumulative returns -- portfolio (green) avoids the crash vs. S&P 500 (red)

---

### Stress Test P&L Surface

The stress test engine sweeps across **Spot Shocks** (-50% to +20%) and **Volatility Shocks** (0% to +50%) simultaneously, computing portfolio P&L at every combination. Historical crisis scenarios (GFC 2008, COVID 2020, etc.) are marked as labeled points on the surface.

![Stress Test Surface Animation](docs/img/stress_test_surface.gif)

**Reading the surface:**
- **Green zone** (upper right): Mild shocks, portfolio holds up
- **Red zone** (lower left): Severe spot crash + vol spike = maximum loss
- **Labeled points**: Where historical crises fall on the shock spectrum
- The surface **rotates** to show the full 3D shape of portfolio risk

---

### HMM Regime Transition Matrix

The Hidden Markov Model's **5x5 transition probability matrix** shows the likelihood of moving between market regimes. The dashed cyan box tracks the current state as it moves through the cycle. Watch the probabilities shift as different regimes become more or less likely.

![Regime Transition Heatmap Animation](docs/img/regime_transition_heatmap.gif)

**Reading the matrix:**
- **Rows** = current state (From), **Columns** = next state (To)
- **Diagonal** = probability of staying in current regime (self-transition)
- **Off-diagonal** = probability of regime change
- **Hot colors** (red/orange) = high probability, **Cool colors** (blue) = low probability
- **Dashed box** = current active state moving through the cycle

---

## How the 3D Coordinate System Changes Per Regime

Watch the 3D P&L surface **morph in real-time** as the engine cycles through all 5 market regimes. The surface color, shape, and height change as the Hidden Markov Model detects regime transitions. The timeline bar at the bottom tracks the current phase.

![3D Regime Phase Comparison Animation](docs/img/regime_phases_comparison.gif)

**What changes per regime:**
- **Bull Quiet**: Smooth green elevated dome -- stable premium income, low vol, high Sharpe
- **Transition**: Surface starts rippling and tilting -- early warning score rising, VIX climbing
- **Bear Volatile**: Surface **inverts** into a deep red crater -- crisis mode, max cash allocation
- **Recovery**: Surface reforms upward with steep blue slopes -- re-entering at the bottom
- **New Bull**: Smooth green dome returns at higher levels -- full cycle alpha locked in

---

### Full Cycle Performance vs. S&P 500

The animated chart below shows the engine's portfolio (green) vs. the S&P 500 benchmark (red) over a full 756-day cycle. Watch how the regime detection system **avoids the crash** by shifting to cash early, then **re-enters aggressively** at the bottom during recovery.

![Performance vs S&P 500 Animation](docs/img/performance_vs_sp500.gif)

**Key observations:**
- **Day 180-240 (Transition)**: Engine detects regime shift, starts reducing equity exposure
- **Day 240-340 (Crisis)**: Portfolio holds 70% cash while S&P drops -- drawdown limited to ~8% vs ~35%
- **Day 340-460 (Recovery)**: Engine re-enters with 1.3x exposure, capturing the V-shaped recovery
- **Day 460+ (New Bull)**: Full exposure with options premium income, alpha continues to compound
- **Lower panel**: Drawdown comparison -- the engine's max drawdown is a fraction of the benchmark's

---

## Features

### Options Pricing & Greeks
- **Black-Scholes** analytical pricing with full Greeks (Delta, Gamma, Theta, Vega, Rho)
- **Monte Carlo simulation** with antithetic variates and control variates
- **Implied volatility** solver via Newton-Raphson
- **Regime-switching Monte Carlo** with stochastic volatility transitions

### 10+ Options Strategies
- Covered Call, Protective Put, Collar
- Bull Call Spread, Bear Put Spread
- Iron Condor, Iron Butterfly
- Long/Short Straddle, Long/Short Strangle
- Calendar Spread, Ratio Spread

### Hidden Markov Model Regime Detection
- 5-state market regime model: Bull Quiet, Bull Volatile, Bear Quiet, Bear Volatile, Transition
- Online Bayesian updating with Forward algorithm
- Viterbi decoding for most likely regime sequence
- Baum-Welch training for parameter optimization
- Multi-factor feature extraction: returns, volatility, credit spreads, volume

### Early Warning System
- **Crisis probability tracking** with real-time alerts
- **Multi-factor warning score**: vol acceleration, price momentum, credit spread widening, HMM transition probability
- **Trading signals**: Strong Buy, Buy, Hold, Reduce Risk, Go To Cash, Crisis
- **Dynamic allocation targets**: Cash/Equity/Options percentages per regime

### Stress Testing
- **8 historical scenarios**: Black Monday 1987, Dot-Com 2000, GFC 2008, Flash Crash 2010, Volmageddon 2018, COVID 2020, Meme Stocks 2021, Rate Hike 2022
- **Parametric grid stress tests**
- **Tail risk scenario generation**
- **Correlated multi-factor scenarios**
- **Reverse stress testing** (find scenarios causing target loss)
- **VaR and CVaR** computation

### 3D Live Visualization Dashboard
- **Real-time 3D P&L surface** (Spot x Volatility x P&L) using Three.js/WebGL
- **Regime change timeline** with color-coded history
- **Trading signal display** with allocation bars
- **Stress test results table**
- **Portfolio metrics panel**: Value, Return, Alpha, Sharpe, Max Drawdown, Greeks
- **Early warning progress bar**
- **Regime probability distribution** bars
- Auto-rotating 3D camera with orbit controls

---

## Architecture

```
src/
├── core/               # Pricing engine
│   ├── black_scholes   # Analytical options pricing & Greeks
│   ├── monte_carlo     # MC simulation with regime switching
│   ├── portfolio       # Portfolio management & P&L surfaces
│   └── market_data     # Synthetic market data generator
├── strategies/         # Options strategy library
│   ├── options_strategies  # 10+ strategy factories
│   └── strategy_manager    # Regime-based strategy selection
├── regime/             # Regime detection
│   ├── hidden_markov_model # Full HMM implementation
│   └── regime_detector     # Feature extraction & signal generation
├── stress/             # Stress testing
│   ├── stress_engine       # Main stress test runner
│   ├── scenario_generator  # Parametric & tail risk scenarios
│   └── historical_scenarios # Pre-built crisis scenarios
├── visualization/      # Live dashboard
│   ├── web_server      # Embedded HTTP + SSE server
│   └── data_broadcaster # Real-time data serialization
└── utils/              # Utilities
    ├── math_utils      # Statistical functions
    ├── json_writer     # JSON serialization
    └── csv_parser      # Data I/O
```

### Data Flow

```
 Market Data (Synthetic S&P 500)
           |
           v
+------------------------+
|   Feature Extraction   |  Returns, Vol, Spreads, Volume
+------------------------+
           |
     +-----+-----+
     |           |
     v           v
+-----------+  +------------------+
| HMM Regime|  | Early Warning    |
| Detector  |->| System           |
+-----------+  +------------------+
     |           |
     v           v
+-----------+  +------------------+
| Strategy  |  | Trading Signal   |
| Manager   |  | BUY/HOLD/CRISIS  |
+-----------+  +------------------+
     |           |
     +-----+-----+
           |
           v
+------------------------+
|   Portfolio Engine     |
|   (P&L, Greeks, VaR)  |
+------------------------+
           |
     +-----+-----+
     |           |
     v           v
+-----------+  +------------------+
| Stress    |  | 3D Visualization |
| Testing   |  | WebGL + SSE      |
+-----------+  +------------------+
                       |
                       v
              localhost:8080
```

## Build & Run

### Requirements
- C++20 compiler (GCC 10+, Clang 12+)
- CMake 3.16+
- POSIX threads
- Python 3.8+ with matplotlib, numpy, Pillow (for visualization generation only)

### Build
```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

### Run Tests
```bash
./build/run_tests
```

### Run Engine
```bash
# Full simulation with live 3D dashboard
./build/stress_engine

# Then open http://localhost:8080 in your browser

# Custom options
./build/stress_engine --port 3000 --days 1000 --speed 50 --price 5000

# Headless mode (terminal only)
./build/stress_engine --headless --days 500 --speed 0
```

### Regenerate Visualization GIFs
```bash
pip install matplotlib numpy Pillow
python3 scripts/generate_visualizations.py
python3 scripts/gen_regime_3d.py
```

### CLI Options
| Option | Default | Description |
|--------|---------|-------------|
| `--port` | 8080 | Web dashboard port |
| `--days` | 756 | Simulation trading days (756 = 3 years) |
| `--speed` | 100 | Milliseconds between frames |
| `--price` | 4500 | Initial S&P 500 price |
| `--headless` | false | Run without web server |

---

## Regime-Strategy Mapping

| Regime | Surface Shape | Recommended Strategies | Cash Target | Signal |
|--------|---------------|----------------------|-------------|--------|
| Bull Quiet | Smooth green dome | Covered Call, Iron Condor, Bull Call Spread | 15% | Strong Buy |
| Bull Volatile | Steep green peaks | Collar, Straddle, Covered Call | 25% | Buy |
| Bear Quiet | Flat yellow surface | Bear Put Spread, Collar, Protective Put | 40% | Reduce Risk |
| Bear Volatile | **Inverted red crater** | **Protective Put, Collar (CRISIS)** | **60-70%** | **CRISIS** |
| Transition | Rippled mixed surface | Straddle, Strangle, Collar | 35% | Hold |

---

## Stress Test Scenarios

```
  Portfolio Impact by Historical Scenario (unhedged):

  GFC 2008           |██████████████████████████████████████████████████| -55.0%  VIX +50
  Dot-Com 2000       |███████████████████████████████████████████████| -45.0%  VIX +20
  COVID Crash 2020   |██████████████████████████████████| -34.0%  VIX +55
  Rate Hike 2022     |█████████████████████████| -25.0%  VIX +15
  Black Monday 1987  |████████████████████████████████████████| -22.6%  VIX +40
  Volmageddon 2018   |██████████| -10.0%  VIX +35
  Flash Crash 2010   |█████████| -9.0%  VIX +25

  WITH Engine Hedging Active:
  GFC 2008           |████████████| -12.0%  (43% loss avoided)
  COVID 2020         |████████| -8.0%   (26% loss avoided)
  Black Monday       |██████| -6.0%   (16.6% loss avoided)
```

---

## Statistical Validation — Market-Maker Regime Backtest

Rigorous out-of-sample walk-forward optimization across **20 assets** (10 ETFs + MAG7 stocks + 3 sector ETFs) over 13–45 years of daily data.

### Methodology

| Component | Detail |
|-----------|--------|
| **Strategy** | ~100% base long + multi-level limit order overlay |
| **Regime classifier** | 5-state EMA slope/vol: CRISIS, CAUTIOUS, RECOVERY, BULL, NORMAL |
| **Walk-forward** | 60% train / 40% test, no lookahead |
| **Parameter grid** | 1,296 combinations (4×3×3×3×3×2×2) |
| **Fee model** | IBKR Tiered: maker rebate $0.0020/sh, commission $0.0015/sh, SEC+FINRA |
| **Fill model** | OHLC intraday oscillation, 45% adverse selection discount |
| **Assets** | SPY, QQQ, IWM, EFA, EEM, GLD, TLT, DIA, VGK, ACWI, AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, XLK, XLF, XLV |

### Out-of-Sample Results (Walk-Forward Test Period)

| Asset | Alpha | Sharpe | Calmar | Fills/d | Spread/yr | Max DD |
|-------|------:|-------:|-------:|--------:|----------:|-------:|
| TSLA | +58.15% | 1.793 | 2.029 | 59 | 160.70% | 59.5% |
| META | +48.00% | 1.963 | 2.052 | 43 | 108.37% | 35.4% |
| NVDA | +44.36% | 2.535 | 3.203 | 50 | 129.30% | 34.6% |
| AMZN | +43.52% | 2.171 | 2.002 | 39 | 94.02% | 36.6% |
| MSFT | +42.73% | 2.301 | 2.495 | 37 | 79.63% | 25.8% |
| GOOGL | +40.87% | 2.496 | 2.774 | 36 | 89.94% | 25.2% |
| AAPL | +40.50% | 2.399 | 1.642 | 38 | 89.06% | 42.1% |
| IWM | +39.56% | 2.213 | 1.416 | 35 | 72.60% | 36.9% |
| QQQ | +38.37% | 2.559 | 2.644 | 32 | 69.09% | 22.0% |
| XLK | +37.27% | 2.564 | 2.507 | 31 | 70.99% | 23.8% |
| XLF | +34.38% | 1.890 | 1.087 | 30 | 64.58% | 43.5% |
| SPY | +34.21% | 2.672 | 1.964 | 28 | 55.36% | 25.2% |
| XLV | +33.55% | 2.529 | 2.169 | 27 | 55.49% | 19.7% |
| DIA | +31.76% | 2.456 | 1.540 | 26 | 52.80% | 28.9% |
| ACWI | +30.66% | 2.478 | 1.770 | 25 | 55.35% | 25.4% |
| VGK | +24.66% | 1.831 | 1.183 | 22 | 52.72% | 29.3% |
| TLT | +24.60% | 1.499 | 1.166 | 22 | 46.52% | 20.5% |
| EFA | +22.47% | 1.884 | 1.194 | 21 | 47.82% | 27.7% |
| EEM | +21.42% | 1.387 | 0.996 | 22 | 52.81% | 31.6% |
| GLD | +18.32% | 2.133 | 2.025 | 22 | 46.21% | 16.9% |

**Summary**: Mean alpha **+35.47%**, Sharpe **2.188**, Calmar **1.893** | ~32 fills/day, 74.67%/yr spread captured | **20/20 positive alpha**, 20/20 statistically significant

### Statistical Significance (4 independent tests, all 20 assets)

| Test | Method | All 20 p-values |
|------|--------|-----------------|
| Sharpe t-test | H₀: SR≤0 | < 0.0001 |
| Block bootstrap | 10k resamples, block=20 | < 0.0001 |
| Permutation test | 10k permutations vs. benchmark | < 0.0001 |
| Deflated Sharpe Ratio | Corrects for 1,296 combos tried | < 0.0001 |

All 20 assets pass all 4 tests at p < 0.0001. The Deflated Sharpe Ratio explicitly accounts for multiple testing (1,296 parameter combinations), confirming results are not data-mined.

### Interpretation

The strategy generates alpha primarily from market-making spread capture on top of a fully-invested base position. Higher-volatility names (TSLA, META, NVDA) produce more fills and wider spreads, resulting in larger alpha. Lower-volatility names (GLD, TLT, EFA) still produce significant alpha but with fewer fills. The regime classifier protects capital during crises by trimming the base position 10–30% in CRISIS/CAUTIOUS states, reducing drawdowns relative to buy-and-hold. All results are out-of-sample with realistic IBKR fee assumptions and conservative adverse selection modeling.

---

## Usage — Rolling Backtest Scripts

### Run All 20 Assets (Full Backtest)

```bash
pip install yfinance numpy pandas scipy
python3 scripts/rolling_backtest.py
```

This downloads OHLC data for all 20 assets, optimizes parameters via walk-forward on each, runs statistical tests, and outputs a combined results CSV.

### Run a Single Asset (Incremental)

```bash
python3 scripts/run_single_asset.py SPY
python3 scripts/run_single_asset.py TSLA
python3 scripts/run_single_asset.py NVDA
```

Each call runs one ticker independently, saving its result to `results/per_asset/<TICKER>.csv` and equity curve to `results/per_asset/<TICKER>_curve.npz`. This is useful for:
- Running assets one-by-one to avoid losing progress if one crashes
- Parallelizing across multiple machines
- Re-running a single asset after parameter changes

### Output Files

| File | Description |
|------|-------------|
| `results/rolling_backtest_results.csv` | Combined results for all 20 assets |
| `results/per_asset/<TICKER>.csv` | Individual per-asset metrics |
| `results/per_asset/<TICKER>_curve.npz` | Strategy & benchmark return arrays |

---

## License

MIT
