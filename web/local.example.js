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

// LiveCoinWatch looks coins up by ticker, not by CoinGecko id. The network name from status.json, uppercased,
// is used by default ("ark" -> ARK), and bitcoin is built in. Add a ticker here for any network where that
// doesn't match, e.g. { monolythium: 'LYTH' }.
window.PRICE_SYMBOLS = {};
