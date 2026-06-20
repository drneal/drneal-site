---
title: "Inside the Algorithmic Trading Backtester: ML Signal Generation, Synthetic Data, and the Three Classifiers Under the Hood"
date: 2026-06-20
category: Algorithmic Trading
tags: algorithmic trading, machine learning, backtesting, scikit-learn, pandas, Python, quantitative finance, neural nets
level: Intermediate
read_time: 16 min
summary: A deep dive into the Algorithmic Trading Backtester live demo — how the synthetic price series is generated, what the three ML classifiers are actually doing, where to find the code in the GitHub repo, and which algorithms are next in line.
featured: false
---

*The live demo is available at [/backtester](/backtester). Everything described here runs in your browser — no data download, no local Python environment required.*

---

The [Algorithmic Trading Backtester](/backtester) is a live Flask application hosted on this site. You pick a machine learning model and a set of technical features, hit Run, and within a few seconds you get a full equity curve benchmarked against buy-and-hold, a drawdown chart, and eight risk/performance metrics including annualised Sharpe ratio, maximum drawdown, signal accuracy, and alpha versus the passive baseline.

This post explains exactly how it works, what it demonstrates about my broader quant finance practice, and where every piece of the code lives.

## What Skills This Is Demonstrating

Before getting into the mechanics, it is worth being explicit about what the demo is designed to show:

**End-to-end ML pipeline design.** The demo covers the full supervised learning workflow: data generation, feature engineering, train/test splitting, feature scaling, model fitting, out-of-sample signal generation, and portfolio simulation. Each stage is deliberate and auditable.

**Quantitative feature construction.** The six feature families — SMA crossover, EMA crossover, RSI, momentum, rolling volatility, and MACD histogram — are the same building blocks used in production systematic strategies. Implementing them correctly from raw price data (rather than pulling them from a library) is a meaningful competency test.

**Proper out-of-sample discipline.** The model is trained on the first 70% of the data and then signals are generated on the held-out 30% it has never seen. The StandardScaler is fit on the training set and *applied* to the test set — the correct way to avoid data leakage.

**Risk-aware performance attribution.** Reporting only total return is how people lose money. The demo computes Sharpe ratio, maximum drawdown, win rate, and alpha versus the buy-and-hold baseline — the metrics that actually matter for evaluating whether a strategy earns its risk.

**Production-grade Flask API design.** The backtester runs as a JSON API endpoint (`POST /backtester/run`) that the frontend hits via `fetch()`. The separation between the Python engine and the Chart.js frontend is the same architecture I use when building trading dashboards for real deployments.

---

## How the Data Is Generated

The demo uses a **synthetic geometric random walk** — the same statistical foundation that underlies the Black-Scholes option pricing model and the majority of quantitative finance theory.

The generation code is at lines 238–241 of [`app.py`](https://github.com/drneal/drneal-site/blob/main/app.py):

```python
rng = np.random.default_rng(seed)
daily_ret = rng.normal(0.0005, 0.015, n_days)
closes = pd.Series(100.0 * np.cumprod(1 + daily_ret))
```

Each daily return is drawn independently from a Normal distribution with mean μ = 0.0005 (roughly +12.5% annualised drift) and standard deviation σ = 0.015 (roughly 24% annualised volatility). These parameters are realistic for a liquid equity instrument. The closing price series is then the cumulative product of `(1 + r_t)` starting at 100, which ensures prices stay positive — the geometric rather than arithmetic formulation.

### A Sample of the Generated Feature Matrix

After price generation, the feature engineering pipeline produces a matrix like this (first 8 usable rows after the 30-day warm-up period, seed = 42):

| day | close  | daily_ret | sma_ratio | rsi   | mom_5  | mom_20 | target |
|-----|--------|-----------|-----------|-------|--------|--------|--------|
| 29  | 102.08 | +0.70%    | +0.0106   | 63.18 | +2.35% | +6.92% | 1      |
| 30  | 105.41 | +3.26%    | +0.0147   | 70.79 | +6.20% | +8.92% | 0      |
| 31  | 104.82 | −0.56%    | +0.0189   | 75.33 | +4.71% | +7.01% | 0      |
| 32  | 104.07 | −0.72%    | +0.0212   | 67.73 | +3.34% | +6.08% | 0      |
| 33  | 102.85 | −1.17%    | +0.0233   | 61.52 | +1.45% | +3.04% | 1      |
| 34  | 103.85 | +0.97%    | +0.0256   | 65.33 | +1.73% | +3.27% | 1      |
| 35  | 105.66 | +1.74%    | +0.0290   | 73.93 | +0.24% | +6.39% | 0      |
| 36  | 105.53 | −0.12%    | +0.0315   | 69.45 | +0.68% | +5.62% | 0      |

The `target` column is the label the model is trained to predict: `1` if tomorrow's close is higher than today's, `0` otherwise. This is a binary classification problem on a highly noisy signal — which is exactly what makes it a useful test of a classifier's ability to extract genuine predictive content from technical features.

The `sma_ratio` column measures how far the 10-day SMA is above or below the 30-day SMA, expressed as a fraction of the slower average. When this is positive and rising, the short-term trend is stronger than the medium-term — a conventional bullish signal. RSI is the standard Wilder momentum oscillator; values above 70 indicate overbought conditions, below 30 oversold.

---

## The Three Classifiers

### Logistic Regression

[Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression) is the simplest of the three. It learns a linear decision boundary in feature space: a weighted sum of the input features is passed through a sigmoid function to produce a probability between 0 and 1, which is then thresholded at 0.5 to generate a buy/sell signal.

Despite its simplicity, it serves a critical purpose here: it is the **baseline**. If a more complex model cannot beat Logistic Regression on this task, the additional complexity is unjustified. In quantitative finance, simpler models generalise better out-of-sample because they are less prone to fitting noise in the training data — a phenomenon that kills more live strategies than any other.

In the codebase ([`app.py`, line 302](https://github.com/drneal/drneal-site/blob/main/app.py#L302)):

```python
model = LogisticRegression(max_iter=1000)
```

The `max_iter=1000` is set because the solver (by default `lbfgs`) occasionally needs more iterations to converge when features are highly correlated — which they frequently are in technical analysis.

### Random Forest

[Random Forest](https://en.wikipedia.org/wiki/Random_forest) is an ensemble of decision trees, each trained on a bootstrap sample of the training data and a random subset of features. The final prediction is the majority vote across all trees. This "bagging" approach reduces variance considerably compared to a single deep tree.

For trading signal generation, Random Forest has two significant advantages. First, it handles non-linear interactions between features naturally — something Logistic Regression cannot do without manual feature crosses. Second, `feature_importances_` gives you a ranked list of which signals are actually driving predictions, which is invaluable for understanding and debugging a strategy.

In the codebase ([`app.py`, line 298](https://github.com/drneal/drneal-site/blob/main/app.py#L298)):

```python
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=seed)
```

`max_depth=5` is a deliberate regularisation choice. Unconstrained trees in a financial time-series context will overfit the training set to an extent that makes the out-of-sample equity curve meaningfully worse. Shallow trees generalise better even if their in-sample accuracy is lower.

### Gradient Boosting

[Gradient Boosting](https://en.wikipedia.org/wiki/Gradient_boosting) builds trees sequentially rather than in parallel. Each new tree is trained to predict the *residual errors* of the current ensemble — it literally learns what the previous trees got wrong. The result is a model with very high expressive power that, when properly regularised, generalises well.

In practice, Gradient Boosting tends to outperform Random Forest on structured tabular data — which is why XGBoost and LightGBM (both gradient boosted tree implementations) dominate Kaggle competitions and are widely used in systematic trading.

In the codebase ([`app.py`, line 300](https://github.com/drneal/drneal-site/blob/main/app.py#L300)):

```python
model = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=seed)
```

`max_depth=3` is shallower than the Random Forest trees — gradient boosting is more prone to overfitting because each tree corrects the previous one's errors, which can cause the ensemble to memorise training-set noise if individual trees are too expressive.

---

## Other Algorithms That Could Be Added

The current three classifiers cover the core of classical ML. The following are natural extensions, each adding a different capability:

**[Support Vector Machine (SVM)](https://en.wikipedia.org/wiki/Support_vector_machine)** — finds the maximum-margin hyperplane separating the two classes. With a radial basis function kernel it can model non-linear boundaries and is often competitive with tree ensembles on smaller datasets. `sklearn.svm.SVC`. [scikit-learn docs](https://scikit-learn.org/stable/modules/svm.html).

**[XGBoost](https://en.wikipedia.org/wiki/XGBoost)** — the production-grade gradient boosting implementation by Chen and Guestrin. Faster than scikit-learn's GradientBoostingClassifier, supports GPU training, and includes built-in regularisation (L1 + L2). The de facto standard for tabular ML competitions. [Official documentation](https://xgboost.readthedocs.io/en/stable/).

**[LightGBM](https://en.wikipedia.org/wiki/LightGBM)** — Microsoft's gradient boosting framework. Uses histogram-based tree building which is substantially faster than XGBoost on large datasets, and handles high-cardinality categorical features natively. [Official documentation](https://lightgbm.readthedocs.io/en/stable/).

**[LSTM (Long Short-Term Memory)](https://en.wikipedia.org/wiki/Long_short-term_memory)** — a recurrent neural network architecture designed to capture temporal dependencies in sequential data. The natural choice when the *sequence* of feature values matters, not just their current levels. [Colah's definitive explainer](https://colah.github.io/posts/2015-08-Understanding-LSTMs/). Would require PyTorch or Keras rather than scikit-learn.

**[AdaBoost](https://en.wikipedia.org/wiki/AdaBoost)** — the original boosting algorithm. Reweights training examples after each round, putting more emphasis on examples the current model misclassifies. Simpler than Gradient Boosting and faster to train; useful as an intermediate complexity option between Logistic Regression and a full GBM. `sklearn.ensemble.AdaBoostClassifier`. [scikit-learn docs](https://scikit-learn.org/stable/modules/ensemble.html#adaboost).

**[k-Nearest Neighbours (k-NN)](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)** — classifies a new data point by majority vote among its k nearest training examples in feature space. No training phase; all computation happens at inference time. Useful for detecting regime similarity — "the current feature vector looks like days in the training set that preceded a rise". `sklearn.neighbors.KNeighborsClassifier`. [scikit-learn docs](https://scikit-learn.org/stable/modules/neighbors.html).

**[Gaussian Naive Bayes](https://en.wikipedia.org/wiki/Naive_Bayes_classifier)** — applies Bayes' theorem with the (naive) assumption that features are conditionally independent given the class. Extremely fast, interpretable, and often surprisingly competitive when features genuinely carry independent information. `sklearn.naive_bayes.GaussianNB`. [scikit-learn docs](https://scikit-learn.org/stable/modules/naive_bayes.html).

---

## Where This Fits in My Real Finance Work

The backtester on this site is a **demonstration harness** — a clean, browser-deployable version of the infrastructure I use day-to-day in live trading.

The production system is more involved: it operates on real tick data from MetaTrader 5 via the [MQL5 API](https://www.mql5.com/en/docs), runs rolling walk-forward optimisation rather than a single train/test split, incorporates transaction costs and slippage models, and feeds signals into live execution logic in MQL5. The feature set is substantially larger and includes order-book microstructure features not available from daily OHLCV.

The demo deliberately removes all of that complexity. The goal is to make the signal generation and model evaluation loop accessible and transparent — to show that the underlying statistical machinery is sound — without exposing production-level intellectual property or requiring a brokerage account to interact with.

If you have a specific strategy hypothesis and want to discuss whether it holds up under rigorous backtesting methodology, [get in touch](/about#contact).

---

## Where to Find the Code

Everything runs from a single file in the repository.

The complete backtesting engine is the `_run_backtest()` function in [`app.py`](https://github.com/drneal/drneal-site/blob/main/app.py), starting at **line 223**. It is a self-contained pure-Python function that takes a configuration dictionary and returns a results dictionary — no global state, no database calls, straightforward to unit test.

The Flask routes are at the bottom of the same file:
- `GET /backtester` (line ~356) — renders the HTML page
- `POST /backtester/run` (line ~361) — runs `_run_backtest()` and returns JSON

The frontend — the Chart.js charts, the configuration panel, the `fetch()` call to the API — lives entirely in [`templates/backtester.html`](https://github.com/drneal/drneal-site/blob/main/templates/backtester.html). The JavaScript is inline at the bottom of that file in a `{% block extra_scripts %}` block, so the template is self-contained and easy to audit.

The three Python dependencies that are not part of the base Flask install — `numpy`, `pandas`, and `scikit-learn` — were added to [`requirements.txt`](https://github.com/drneal/drneal-site/blob/main/requirements.txt) and Render installs them automatically on each deploy.

---

*The backtester is live at [/backtester](/backtester). Change the random seed to explore different price realisations, or experiment with switching off individual features to see which ones are actually contributing signal — the accuracy and Sharpe metrics update immediately.*
