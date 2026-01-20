import { useState, useEffect, useCallback } from 'react';
import { getStockData, getStockCandles } from '../services/finnhub';

export function useStockData(symbols, refreshInterval = 30000) {
  const [stockData, setStockData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStockData = useCallback(async () => {
    if (symbols.length === 0) {
      setStockData({});
      setLoading(false);
      return;
    }

    try {
      const results = await Promise.all(
        symbols.map(symbol =>
          getStockData(symbol).catch(err => ({
            symbol,
            error: err.message,
          }))
        )
      );

      const newData = {};
      results.forEach(data => {
        newData[data.symbol] = data;
      });

      setStockData(newData);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [symbols]);

  useEffect(() => {
    fetchStockData();

    const interval = setInterval(fetchStockData, refreshInterval);
    return () => clearInterval(interval);
  }, [fetchStockData, refreshInterval]);

  return { stockData, loading, error, refetch: fetchStockData };
}

export function useStockCandles(symbol, days = 30) {
  const [candles, setCandles] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!symbol) {
      setCandles(null);
      setLoading(false);
      return;
    }

    setLoading(true);
    getStockCandles(symbol, days)
      .then(data => {
        setCandles(data);
        setError(null);
      })
      .catch(err => {
        setError(err.message);
        setCandles(null);
      })
      .finally(() => setLoading(false));
  }, [symbol, days]);

  return { candles, loading, error };
}
