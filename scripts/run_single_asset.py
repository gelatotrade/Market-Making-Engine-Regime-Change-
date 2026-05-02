#!/usr/bin/env python3
"""
Run the market-maker regime backtest for a SINGLE asset and persist
its per-asset result (CSV + equity curve .npz) under results/per_asset/.

This lets us run each ticker independently in small steps so that a
crash on one asset does not lose results from the others.

Usage:
    python3 scripts/run_single_asset.py SPY
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

from rolling_backtest import (  # noqa: E402
    walk_forward, sharpe_ttest, block_bootstrap, perm_test, deflated_sr,
    PARAM_GRID, MIN_TRAIN_BARS, MIN_TEST_BARS,
)
from itertools import product as _prod

try:
    import yfinance as yf
except ImportError:
    sys.exit('pip install yfinance')

OUT_DIR = ROOT / 'results' / 'per_asset'


def run_one(ticker: str):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f'[{ticker}] downloading ...', flush=True)
    df = yf.download(ticker, period='max', interval='1d', progress=False)
    if len(df) < MIN_TRAIN_BARS + MIN_TEST_BARS:
        sys.exit(f'[{ticker}] too few bars ({len(df)})')
    o = df['Open'].values.flatten()
    h = df['High'].values.flatten()
    l = df['Low'].values.flatten()
    c = df['Close'].values.flatten()
    m = ~(np.isnan(o) | np.isnan(h) | np.isnan(l) | np.isnan(c))
    o, h, l, c = o[m], h[m], l[m], c[m]
    print(f'[{ticker}] {len(c)} bars ({len(c)/252:.1f}y), walk-forward ...',
          flush=True)

    wf = walk_forward(o, h, l, c)
    if wf is None:
        sys.exit(f'[{ticker}] walk_forward returned None')

    sr = wf.pop('strat_returns')
    br = wf.pop('bench_returns')
    nc = len(list(_prod(*PARAM_GRID.values())))

    st1 = sharpe_ttest(sr)
    st2 = block_bootstrap(sr)
    st3 = perm_test(sr, br)
    st4 = deflated_sr(wf['sharpe'], nc, wf['test_bars'])

    row = {'asset': ticker, **wf}
    row['sr_pval'] = st1['p_value']; row['sr_sig'] = st1['significant']
    row['boot_ci_lo'] = st2['ci_lo']; row['boot_ci_hi'] = st2['ci_hi']
    row['boot_pval'] = st2['p_value']; row['boot_sig'] = st2['significant']
    row['perm_pval'] = st3['p_value']; row['perm_sig'] = st3['significant']
    row['dsr'] = st4['dsr']; row['dsr_sig'] = st4['significant']

    csv = OUT_DIR / f'{ticker}.csv'
    pd.DataFrame([row]).to_csv(csv, index=False, float_format='%.6f')
    np.savez_compressed(OUT_DIR / f'{ticker}_curve.npz',
                        strat=sr.astype(np.float32),
                        bench=br.astype(np.float32))

    pv = (f'p=[{st1["p_value"]:.4f} {st2["p_value"]:.4f} '
          f'{st3["p_value"]:.4f} {st4["dsr"]:.4f}]')
    print(f'[{ticker}] Alpha={wf["alpha"]*100:+.2f}%  '
          f'Sharpe={wf["sharpe"]:.3f}  Calmar={wf["calmar"]:.3f}  '
          f'Fill/d={wf["fills_per_day"]:.0f}  '
          f'Spread={wf["spread_ann"]*100:.2f}%  '
          f'DD={wf["max_dd"]*100:.1f}%  {pv}')
    print(f'[{ticker}] saved -> {csv}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: run_single_asset.py TICKER')
    run_one(sys.argv[1].upper())
