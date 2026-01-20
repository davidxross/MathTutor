import { useState, useEffect, useRef } from 'react';
import { useStock } from '../context/StockContext';
import { searchSymbols, getQuote } from '../services/finnhub';

export default function SearchBar() {
  const { addStock, watchlist } = useStock();
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const inputRef = useRef(null);
  const suggestionsRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target) &&
        !inputRef.current.contains(event.target)
      ) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const timeoutId = setTimeout(async () => {
      if (query.length >= 1) {
        setLoading(true);
        try {
          const results = await searchSymbols(query);
          setSuggestions(results);
          setShowSuggestions(true);
        } catch (err) {
          console.error('Search error:', err);
        } finally {
          setLoading(false);
        }
      } else {
        setSuggestions([]);
        setShowSuggestions(false);
      }
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [query]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const symbol = query.trim().toUpperCase();

    if (watchlist.includes(symbol)) {
      setError('Stock already in watchlist');
      setTimeout(() => setError(''), 3000);
      return;
    }

    setLoading(true);
    setError('');

    try {
      await getQuote(symbol);
      addStock(symbol);
      setQuery('');
      setShowSuggestions(false);
    } catch (err) {
      setError('Invalid stock symbol');
      setTimeout(() => setError(''), 3000);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (symbol) => {
    if (watchlist.includes(symbol)) {
      setError('Stock already in watchlist');
      setTimeout(() => setError(''), 3000);
      setQuery('');
      setShowSuggestions(false);
      return;
    }

    addStock(symbol);
    setQuery('');
    setShowSuggestions(false);
    setError('');
  };

  return (
    <div className="relative w-full max-w-md">
      <form onSubmit={handleSubmit} className="relative">
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
          placeholder="Search stocks (e.g., AAPL, SHOP.TO)"
          className="w-full px-4 py-2 pr-10 text-slate-900 dark:text-white bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent placeholder-slate-400 dark:placeholder-slate-500"
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 disabled:opacity-50"
        >
          {loading ? (
            <svg
              className="w-5 h-5 animate-spin"
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
          ) : (
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
          )}
        </button>
      </form>

      {error && (
        <p className="absolute mt-1 text-sm text-red-500 dark:text-red-400">
          {error}
        </p>
      )}

      {showSuggestions && suggestions.length > 0 && (
        <ul
          ref={suggestionsRef}
          className="absolute z-10 w-full mt-1 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-lg shadow-lg max-h-60 overflow-auto"
        >
          {suggestions.map((item) => (
            <li key={item.symbol}>
              <button
                type="button"
                onClick={() => handleSuggestionClick(item.symbol)}
                className="w-full px-4 py-2 text-left hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
              >
                <span className="font-medium text-slate-900 dark:text-white">
                  {item.symbol}
                </span>
                {item.exchange && item.exchange !== 'US' && (
                  <span className="ml-1.5 px-1.5 py-0.5 text-xs font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 rounded">
                    {item.exchange}
                  </span>
                )}
                <span className="ml-2 text-sm text-slate-500 dark:text-slate-400">
                  {item.description}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
