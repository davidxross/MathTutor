const API_KEY = import.meta.env.VITE_FINNHUB_API_KEY;
const BASE_URL = 'https://finnhub.io/api/v1';

const cache = new Map();
const CACHE_DURATION = 15000; // 15 seconds

function getCached(key) {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    return cached.data;
  }
  return null;
}

function setCache(key, data) {
  cache.set(key, { data, timestamp: Date.now() });
}

async function fetchWithRetry(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url);
      if (response.status === 429) {
        // Rate limited, wait and retry
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        continue;
      }
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
}

export async function getQuote(symbol) {
  const cacheKey = `quote-${symbol}`;
  const cached = getCached(cacheKey);
  if (cached) return cached;

  const url = `${BASE_URL}/quote?symbol=${symbol}&token=${API_KEY}`;
  const data = await fetchWithRetry(url);

  if (data.c === 0 && data.h === 0 && data.l === 0) {
    throw new Error('Invalid symbol');
  }

  setCache(cacheKey, data);
  return data;
}

export async function getCompanyProfile(symbol) {
  const cacheKey = `profile-${symbol}`;
  const cached = getCached(cacheKey);
  if (cached) return cached;

  const url = `${BASE_URL}/stock/profile2?symbol=${symbol}&token=${API_KEY}`;
  const data = await fetchWithRetry(url);

  if (!data.name) {
    throw new Error('Company not found');
  }

  setCache(cacheKey, data);
  return data;
}

export async function getStockCandles(symbol, days = 30) {
  const cacheKey = `candles-${symbol}-${days}`;
  const cached = getCached(cacheKey);
  if (cached) return cached;

  const to = Math.floor(Date.now() / 1000);
  const from = to - (days * 24 * 60 * 60);

  const url = `${BASE_URL}/stock/candle?symbol=${symbol}&resolution=D&from=${from}&to=${to}&token=${API_KEY}`;
  const data = await fetchWithRetry(url);

  if (data.s === 'no_data') {
    return { timestamps: [], closes: [] };
  }

  const result = {
    timestamps: data.t || [],
    closes: data.c || [],
    opens: data.o || [],
    highs: data.h || [],
    lows: data.l || [],
    volumes: data.v || [],
  };

  setCache(cacheKey, result);
  return result;
}

export async function searchSymbols(query) {
  if (!query || query.length < 1) return [];

  const cacheKey = `search-${query}`;
  const cached = getCached(cacheKey);
  if (cached) return cached;

  const url = `${BASE_URL}/search?q=${query}&token=${API_KEY}`;
  const data = await fetchWithRetry(url);

  const results = (data.result || [])
    .filter(item => item.type === 'Common Stock')
    .slice(0, 10)
    .map(item => ({
      symbol: item.symbol,
      description: item.description,
    }));

  setCache(cacheKey, results);
  return results;
}

export async function getStockData(symbol) {
  const [quote, profile] = await Promise.all([
    getQuote(symbol),
    getCompanyProfile(symbol).catch(() => ({ name: symbol })),
  ]);

  return {
    symbol,
    name: profile.name || symbol,
    logo: profile.logo || null,
    price: quote.c,
    change: quote.d,
    changePercent: quote.dp,
    high: quote.h,
    low: quote.l,
    open: quote.o,
    prevClose: quote.pc,
  };
}
