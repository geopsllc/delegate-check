// Optional local settings for the dashboard.
// Copy this file to local.js (git-ignored, so git pull never touches it) and edit the copy.
//
// With nothing set, prices come from CoinGecko without a key. Set a key below to use it (CoinGecko Demo keys
// are capped at 10,000 calls a month) or to switch to LiveCoinWatch.

window.CG_API_KEY = '';   // free CoinGecko Demo key (optional)
window.LCW_API_KEY = '';  // free LiveCoinWatch key (optional): 10,000 requests a day

// Which provider to use: 'coingecko' or 'livecoinwatch'. Leave empty to pick automatically:
// a LiveCoinWatch key selects LiveCoinWatch, otherwise CoinGecko (with your key if set, keyless if not).
window.PRICE_PROVIDER = '';

// A price chip is shown for every network in status.json. Add any other coins here, in the order you want them
// (they appear before the network chips). name is the chip label, ticker the symbol LiveCoinWatch uses.
// CoinGecko looks coins up by id, which defaults to the name lowercased with dashes ("Bitcoin" -> bitcoin);
// add id when that doesn't match. Prices get about three significant digits ($97,412 / $3,105 / $0.284 / $0.0712);
// set decimals to force a fixed number for a coin.
window.PRICE_COINS = [
  // {name: 'Bitcoin',  ticker: 'BTC'},
  // {name: 'Ethereum', ticker: 'ETH', decimals: 1},
  // {name: 'Polymesh', ticker: 'POLYX'},
];

// LiveCoinWatch tickers for networks: the network name from status.json, uppercased, is used by default
// ("ark" -> ARK). Add a ticker here for any network where that doesn't match, e.g. { monolythium: 'LYTH' }.
window.PRICE_SYMBOLS = {};

// How often prices refresh, in seconds (minimum 10). Leave empty for the default: 300 (5 minutes) with CoinGecko,
// 60 with LiveCoinWatch. LiveCoinWatch allows 10,000 requests a day, so 60 seconds uses about 1,440 a day per open tab.
window.PRICE_REFRESH_SECS = '';
