import datetime
from typing import List, Dict
from ..utils import basic_financials
from langchain_core.tools import tool

@tool(name_or_callable='basic_financials')
def basic_financials_getter(company_symbol: str) -> dict:
    """
    Get the basic financials data for the company. 

    Args:
        company_symbol(str): Symbol by which company is listed.
    
    Returns:
        Dictionary containing the financial data
    """
    return basic_financials(company_symbol=company_symbol)

@tool
def summarize_finnhub_financials(data:dict):
    """
    Summarizes Finnhub financial data into token-efficient categories.
    The financial data is organized in 9 structured categories as follows:

    1. Valuation - P/E, P/B, P/S, PEG, EV/EBITDA ratios
    2. Profitability - Margins, EPS, ROE, ROA with growth trends
    3. Liquidity - Current/quick ratios with status assessment
    4. Leverage - Debt ratios with risk assessment
    5. Efficiency - Asset turnover metrics
    6. Performance - Revenue growth and dividend yield
    7. Stock Performance - Price movements vs benchmarks
    8. Quarterly Trends - Recent quarter-over-quarter changes
    9. Highlights & Red Flags - Automatic detection of key concerns

    Args:
        data (dict): Raw Finnhub financial data with 'metric', 'series', and 'symbol' recieved by 'basic_financials' tool.

    Returns:
        dict: Structured summary organized by financial categories

    Example:
        >>> result = summarize_finnhub_financials(finnhub_data)
        >>> print(result['overall_health'])
        'Strong'
    """

    metric = data.get('metric', {})
    symbol = data.get('symbol', 'UNKNOWN')
    series = data.get('series', {})

    # Helper function to safely get metric values
    def get_metric(key, default=None):
        return metric.get(key, default)

    # Helper to format percentages
    def format_pct(value, multiplier=1):
        if value is None:
            return "N/A"
        return f"{value * multiplier:.2f}%"

    # Helper to identify trends
    def get_trend(current, growth):
        if growth is None or current is None:
            return "stable"
        if growth > 10:
            return "strong growth"
        elif growth > 5:
            return "moderate growth"
        elif growth < -10:
            return "declining"
        elif growth < 0:
            return "slight decline"
        return "stable"

    # 1. VALUATION METRICS
    valuation = {
        "pe_ttm": get_metric('peTTM'),
        "forward_pe": get_metric('forwardPE'),
        "pb_ratio": get_metric('pb'),
        "ps_ratio": get_metric('psTTM'),
        "peg_ratio": get_metric('pegTTM'),
        "ev_ebitda": get_metric('evEbitdaTTM'),
        "market_cap": get_metric('marketCapitalization'),
        "enterprise_value": get_metric('enterpriseValue')
    }

    # 2. PROFITABILITY METRICS
    profitability = {
        "eps_ttm": get_metric('epsTTM'),
        "eps_growth_ttm_yoy": format_pct(get_metric('epsGrowthTTMYoy')),
        "eps_growth_3y": format_pct(get_metric('epsGrowth3Y')),
        "net_margin_ttm": format_pct(get_metric('netProfitMarginTTM'), 100),
        "operating_margin_ttm": format_pct(get_metric('operatingMarginTTM'), 100),
        "gross_margin_ttm": format_pct(get_metric('grossMarginTTM'), 100),
        "roe_ttm": format_pct(get_metric('roeTTM'), 100),
        "roa_ttm": format_pct(get_metric('roaTTM'), 100),
        "roic_ttm": format_pct(get_metric('roiTTM'), 100),
        "trend": get_trend(get_metric('netProfitMarginTTM'), get_metric('netMarginGrowth5Y'))
    }

    # 3. LIQUIDITY METRICS
    # Extract nested conditional into a separate statement for clarity and to satisfy linters
    _wc_ratio = get_metric('currentRatioQuarterly', 0)
    if _wc_ratio > 1.5:
        _working_capital_status = "healthy"
    elif _wc_ratio > 1.0:
        _working_capital_status = "adequate"
    else:
        _working_capital_status = "tight"

    liquidity = {
        "current_ratio": get_metric('currentRatioQuarterly'),
        "quick_ratio": get_metric('quickRatioQuarterly'),
        "cash_per_share": get_metric('cashPerSharePerShareQuarterly'),
        "working_capital_status": _working_capital_status
    }

    # 4. LEVERAGE/SOLVENCY METRICS
    _debt_to_equity = get_metric('totalDebt/totalEquityQuarterly', 0)
    if _debt_to_equity > 2.0:
        _leverage_assessment = "high"
    elif _debt_to_equity > 1.0:
        _leverage_assessment = "moderate"
    else:
        _leverage_assessment = "low"

    leverage = {
        "debt_to_equity": get_metric('totalDebt/totalEquityQuarterly'),
        "long_term_debt_to_equity": get_metric('longTermDebt/equityQuarterly'),
        "debt_to_assets": get_metric('totalDebtToTotalAsset'),
        "interest_coverage": get_metric('netInterestCoverageTTM'),
        "leverage_assessment": _leverage_assessment
    }

    # 5. EFFICIENCY METRICS
    efficiency = {
        "asset_turnover_ttm": get_metric('assetTurnoverTTM'),
        "inventory_turnover_ttm": get_metric('inventoryTurnoverTTM'),
        "receivables_turnover_ttm": get_metric('receivablesTurnoverTTM'),
        "cash_flow_per_share_ttm": get_metric('cashFlowPerShareTTM')
    }

    # 6. PERFORMANCE TRENDS
    performance = {
        "revenue_growth_ttm_yoy": format_pct(get_metric('revenueGrowthTTMYoy')),
        "revenue_growth_3y": format_pct(get_metric('revenueGrowth3Y')),
        "revenue_per_share_ttm": get_metric('revenuePerShareTTM'),
        "dividend_yield": format_pct(get_metric('currentDividendYieldTTM'), 100)
    }

    # 7. STOCK PERFORMANCE
    stock_performance = {
        "52_week_high": get_metric('52WeekHigh'),
        "52_week_low": get_metric('52WeekLow'),
        "52_week_return": format_pct(get_metric('52WeekPriceReturnDaily')),
        "ytd_return": format_pct(get_metric('yearToDatePriceReturnDaily')),
        "beta": get_metric('beta'),
        "vs_sp500_52week": format_pct(get_metric('priceRelativeToS&P50052Week')),
        "vs_sp500_ytd": format_pct(get_metric('priceRelativeToS&P500Ytd'))
    }

    # 8. RED FLAGS & KEY HIGHLIGHTS
    red_flags = []
    highlights = []

    # Check for red flags
    if get_metric('currentRatioQuarterly', 2) < 1.0:
        red_flags.append("Liquidity concern: Current ratio below 1.0")

    if get_metric('totalDebt/totalEquityQuarterly', 0) > 2.0:
        red_flags.append("High leverage: Debt-to-equity above 2.0")

    if get_metric('netProfitMarginTTM', 0) < 0:
        red_flags.append("Unprofitable: Negative net margin")

    if get_metric('epsGrowthTTMYoy', 0) < -20:
        red_flags.append(f"Significant EPS decline: {format_pct(get_metric('epsGrowthTTMYoy'))}")

    if get_metric('quickRatioQuarterly', 2) < 0.5:
        red_flags.append("Very low quick ratio: May struggle with short-term obligations")

    # Check for highlights
    if get_metric('epsGrowthTTMYoy', 0) > 20:
        highlights.append(f"Strong EPS growth: {format_pct(get_metric('epsGrowthTTMYoy'))} YoY")

    if get_metric('roeTTM', 0) > 0.20:
        highlights.append(f"Excellent ROE: {format_pct(get_metric('roeTTM'), 100)}")

    if get_metric('currentRatioQuarterly', 0) > 2.0:
        highlights.append("Strong liquidity position")

    if get_metric('revenueGrowthTTMYoy', 0) > 15:
        highlights.append(f"High revenue growth: {format_pct(get_metric('revenueGrowthTTMYoy'))}")

    # 9. MOST RECENT QUARTERLY TREND (from series data)
    quarterly_trend = {}
    if 'quarterly' in series and 'eps' in series['quarterly']:
        recent_eps = series['quarterly']['eps'][:4]  # Last 4 quarters
        if len(recent_eps) >= 2:
            quarterly_trend['latest_quarter_eps'] = recent_eps[0]['v']
            quarterly_trend['prior_quarter_eps'] = recent_eps[1]['v']
            quarterly_trend['eps_qoq_change'] = format_pct(
                ((recent_eps[0]['v'] - recent_eps[1]['v']) / abs(recent_eps[1]['v']) * 100) 
                if recent_eps[1]['v'] != 0 else 0, 1
            )

    # Compile summary
    summary = {
        "company": symbol.upper(),
        "snapshot_date": "Latest Available",
        "valuation": valuation,
        "profitability": profitability,
        "liquidity": liquidity,
        "leverage": leverage,
        "efficiency": efficiency,
        "performance": performance,
        "stock_performance": stock_performance,
        "quarterly_trend": quarterly_trend,
        "highlights": highlights if highlights else ["None identified"],
        "red_flags": red_flags if red_flags else ["None identified"],
        "overall_health": _assess_overall_health(metric)
    }

    return summary


def _assess_overall_health(metric):
    """
    Provides an overall assessment based on key metrics.
    """
    score = 0

    # Profitability check
    if metric.get('netProfitMarginTTM', 0) > 0.10:
        score += 2
    elif metric.get('netProfitMarginTTM', 0) > 0:
        score += 1

    # Liquidity check
    if metric.get('currentRatioQuarterly', 0) > 1.5:
        score += 2
    elif metric.get('currentRatioQuarterly', 0) > 1.0:
        score += 1

    # Leverage check
    if metric.get('totalDebt/totalEquityQuarterly', 3) < 1.0:
        score += 2
    elif metric.get('totalDebt/totalEquityQuarterly', 3) < 2.0:
        score += 1

    # Growth check
    if metric.get('epsGrowthTTMYoy', -100) > 10:
        score += 2
    elif metric.get('epsGrowthTTMYoy', -100) > 0:
        score += 1

    # ROE check
    if metric.get('roeTTM', 0) > 0.15:
        score += 2
    elif metric.get('roeTTM', 0) > 0.10:
        score += 1

    if score >= 8:
        return "Strong"
    elif score >= 5:
        return "Good"
    elif score >= 3:
        return "Fair"
    else:
        return "Weak"