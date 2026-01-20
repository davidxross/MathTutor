import { useMemo } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { useStock } from '../context/StockContext';
import { useStockCandles } from '../hooks/useStockData';

function formatDate(timestamp) {
  const date = new Date(timestamp * 1000);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  });
}

function CustomTooltip({ active, payload, label }) {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white dark:bg-slate-800 p-3 rounded-lg shadow-lg border border-slate-200 dark:border-slate-700">
        <p className="text-sm text-slate-500 dark:text-slate-400">{label}</p>
        <p className="text-lg font-bold text-slate-900 dark:text-white">
          ${payload[0].value.toFixed(2)}
        </p>
      </div>
    );
  }
  return null;
}

export default function StockChart() {
  const { selectedStock, stockData, darkMode } = useStock();
  const { candles, loading, error } = useStockCandles(selectedStock);

  const chartData = useMemo(() => {
    if (!candles || !candles.timestamps || candles.timestamps.length === 0) {
      return [];
    }

    return candles.timestamps.map((timestamp, index) => ({
      date: formatDate(timestamp),
      price: candles.closes[index],
    }));
  }, [candles]);

  const priceChange = useMemo(() => {
    if (chartData.length < 2) return null;
    const firstPrice = chartData[0].price;
    const lastPrice = chartData[chartData.length - 1].price;
    const change = lastPrice - firstPrice;
    const changePercent = (change / firstPrice) * 100;
    return { change, changePercent, isPositive: change >= 0 };
  }, [chartData]);

  if (!selectedStock) {
    return (
      <div className="bg-white dark:bg-slate-800 rounded-lg shadow border border-slate-200 dark:border-slate-700 p-6">
        <div className="text-center py-12">
          <svg
            className="mx-auto h-12 w-12 text-slate-400 dark:text-slate-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
            />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-slate-900 dark:text-white">
            No stock selected
          </h3>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Click on a stock card to view its price history
          </p>
        </div>
      </div>
    );
  }

  const selectedStockData = stockData[selectedStock];

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg shadow border border-slate-200 dark:border-slate-700 p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            {selectedStock}
            {selectedStockData?.name && (
              <span className="ml-2 text-sm font-normal text-slate-500 dark:text-slate-400">
                {selectedStockData.name}
              </span>
            )}
          </h2>
          {priceChange && (
            <p
              className={`text-sm ${
                priceChange.isPositive ? 'text-green-500' : 'text-red-500'
              }`}
            >
              30-day change: {priceChange.isPositive ? '+' : ''}
              ${priceChange.change.toFixed(2)} ({priceChange.isPositive ? '+' : ''}
              {priceChange.changePercent.toFixed(2)}%)
            </p>
          )}
        </div>
        <span className="text-sm text-slate-500 dark:text-slate-400">
          Last 30 days
        </span>
      </div>

      {loading ? (
        <div className="h-64 flex items-center justify-center">
          <svg
            className="w-8 h-8 animate-spin text-blue-500"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        </div>
      ) : error || chartData.length === 0 ? (
        <div className="h-64 flex items-center justify-center">
          <p className="text-slate-500 dark:text-slate-400">
            {error || 'No historical data available'}
          </p>
        </div>
      ) : (
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke={darkMode ? '#334155' : '#e2e8f0'}
              />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 12, fill: darkMode ? '#94a3b8' : '#64748b' }}
                tickLine={{ stroke: darkMode ? '#475569' : '#cbd5e1' }}
                axisLine={{ stroke: darkMode ? '#475569' : '#cbd5e1' }}
              />
              <YAxis
                domain={['auto', 'auto']}
                tick={{ fontSize: 12, fill: darkMode ? '#94a3b8' : '#64748b' }}
                tickLine={{ stroke: darkMode ? '#475569' : '#cbd5e1' }}
                axisLine={{ stroke: darkMode ? '#475569' : '#cbd5e1' }}
                tickFormatter={(value) => `$${value}`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line
                type="monotone"
                dataKey="price"
                stroke={priceChange?.isPositive ? '#22c55e' : '#ef4444'}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
