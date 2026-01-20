import { useStock } from '../context/StockContext';

export default function StockCard({ symbol, data }) {
  const { removeStock, selectStock, selectedStock } = useStock();
  const isSelected = selectedStock === symbol;

  if (!data || data.error) {
    return (
      <div className="p-4 bg-white dark:bg-slate-800 rounded-lg shadow border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between">
          <span className="font-bold text-slate-900 dark:text-white">{symbol}</span>
          <button
            onClick={(e) => {
              e.stopPropagation();
              removeStock(symbol);
            }}
            className="p-1 text-slate-400 hover:text-red-500 transition-colors"
            aria-label={`Remove ${symbol}`}
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <p className="text-sm text-red-500 mt-2">Error loading data</p>
      </div>
    );
  }

  const isPositive = data.change >= 0;

  return (
    <div
      onClick={() => selectStock(symbol)}
      className={`p-4 bg-white dark:bg-slate-800 rounded-lg shadow border-2 cursor-pointer transition-all duration-200 hover:shadow-md hover:-translate-y-0.5 ${
        isSelected
          ? 'border-blue-500 dark:border-blue-400'
          : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
      }`}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          {data.logo && (
            <img
              src={data.logo}
              alt={`${data.name} logo`}
              className="w-10 h-10 rounded-lg object-contain bg-white"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
          )}
          <div>
            <h3 className="font-bold text-lg text-slate-900 dark:text-white">
              {symbol}
            </h3>
            <p className="text-sm text-slate-500 dark:text-slate-400 truncate max-w-[150px]">
              {data.name}
            </p>
          </div>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            removeStock(symbol);
          }}
          className="p-1 text-slate-400 hover:text-red-500 transition-colors"
          aria-label={`Remove ${symbol}`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div className="mt-4">
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-slate-900 dark:text-white">
            ${data.price?.toFixed(2)}
          </span>
          <span
            className={`text-sm font-medium ${
              isPositive ? 'text-green-500' : 'text-red-500'
            }`}
          >
            {isPositive ? '+' : ''}
            {data.change?.toFixed(2)} ({isPositive ? '+' : ''}
            {data.changePercent?.toFixed(2)}%)
          </span>
        </div>

        <div className="mt-3 grid grid-cols-2 gap-2 text-sm">
          <div>
            <span className="text-slate-500 dark:text-slate-400">High: </span>
            <span className="text-slate-700 dark:text-slate-300">
              ${data.high?.toFixed(2)}
            </span>
          </div>
          <div>
            <span className="text-slate-500 dark:text-slate-400">Low: </span>
            <span className="text-slate-700 dark:text-slate-300">
              ${data.low?.toFixed(2)}
            </span>
          </div>
          <div>
            <span className="text-slate-500 dark:text-slate-400">Open: </span>
            <span className="text-slate-700 dark:text-slate-300">
              ${data.open?.toFixed(2)}
            </span>
          </div>
          <div>
            <span className="text-slate-500 dark:text-slate-400">Prev: </span>
            <span className="text-slate-700 dark:text-slate-300">
              ${data.prevClose?.toFixed(2)}
            </span>
          </div>
        </div>

        {data.dividend && (
          <div className="mt-3 pt-3 border-t border-slate-200 dark:border-slate-700">
            <div className="flex items-center gap-1.5 text-sm">
              <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-slate-500 dark:text-slate-400">Dividend:</span>
              <span className="text-slate-700 dark:text-slate-300">
                ${data.dividend.amount?.toFixed(2)}
              </span>
              <span className="text-slate-400 dark:text-slate-500">|</span>
              <span className="text-slate-500 dark:text-slate-400">Ex:</span>
              <span className="text-slate-700 dark:text-slate-300">
                {new Date(data.dividend.exDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
