const MarketPrice = require('../models/MarketPrice');
const Transaction = require('../models/Transaction');
const puppeteer = require('puppeteer');
const cheerio = require('cheerio');

// ─── State-wise popular crops (at least 10 per state) ────────────────
const STATE_CROPS = {
  'Andhra Pradesh':    ['Rice','Groundnut','Cotton','Chilli','Turmeric','Maize','Sugarcane','Tobacco','Mango','Banana','Onion','Tomato'],
  'Arunachal Pradesh': ['Rice','Maize','Ginger','Turmeric','Orange','Apple','Kiwi','Cardamom','Soyabean','Mustard','Millet','Potato'],
  'Assam':             ['Rice','Tea','Jute','Sugarcane','Potato','Mustard','Banana','Orange','Areca Nut','Ginger','Turmeric','Lemon'],
  'Bihar':             ['Rice','Wheat','Maize','Sugarcane','Potato','Onion','Lentil','Gram','Mustard','Banana','Litchi','Mango'],
  'Chhattisgarh':      ['Rice','Maize','Soyabean','Groundnut','Sugarcane','Wheat','Gram','Lentil','Tomato','Onion','Potato','Mustard'],
  'Goa':               ['Rice','Coconut','Cashew','Mango','Banana','Pineapple','Areca Nut','Sugarcane','Pepper','Watermelon','Cucumber','Brinjal'],
  'Gujarat':           ['Cotton','Groundnut','Wheat','Rice','Castor Seed','Cumin','Bajra','Sugarcane','Onion','Potato','Tomato','Mango'],
  'Haryana':           ['Wheat','Rice','Bajra','Cotton','Sugarcane','Mustard','Gram','Potato','Tomato','Onion','Barley','Maize'],
  'Himachal Pradesh':  ['Apple','Wheat','Maize','Rice','Barley','Potato','Ginger','Tomato','Pea','Plum','Walnut','Apricot'],
  'Jharkhand':         ['Rice','Wheat','Maize','Gram','Lentil','Potato','Tomato','Onion','Mustard','Sugarcane','Mango','Banana'],
  'Karnataka':         ['Rice','Ragi','Maize','Sugarcane','Cotton','Groundnut','Coconut','Coffee','Pepper','Cardamom','Tomato','Onion'],
  'Kerala':            ['Rice','Coconut','Pepper','Cardamom','Rubber','Ginger','Turmeric','Coffee','Tea','Banana','Cashew','Arecanut','Tapioca','Nutmeg'],
  'Madhya Pradesh':    ['Soyabean','Wheat','Rice','Gram','Maize','Cotton','Sugarcane','Lentil','Mustard','Onion','Garlic','Potato'],
  'Maharashtra':       ['Sugarcane','Cotton','Soyabean','Rice','Wheat','Onion','Gram','Groundnut','Banana','Mango','Grapes','Turmeric'],
  'Manipur':           ['Rice','Maize','Soyabean','Mustard','Potato','Ginger','Turmeric','Orange','Pineapple','Banana','Pea','Cabbage'],
  'Meghalaya':         ['Rice','Maize','Potato','Ginger','Turmeric','Orange','Pineapple','Banana','Areca Nut','Cashew','Jute','Tea'],
  'Mizoram':           ['Rice','Maize','Sugarcane','Ginger','Turmeric','Banana','Orange','Passion Fruit','Chilli','Sesame','Mustard','Potato'],
  'Nagaland':          ['Rice','Maize','Millet','Soyabean','Potato','Ginger','Turmeric','Chilli','Orange','Pineapple','Sugarcane','Mustard'],
  'Odisha':            ['Rice','Groundnut','Sugarcane','Jute','Mustard','Sesamum','Cotton','Maize','Turmeric','Onion','Potato','Mango'],
  'Punjab':            ['Wheat','Rice','Cotton','Maize','Sugarcane','Potato','Bajra','Barley','Mustard','Onion','Tomato','Pea'],
  'Rajasthan':         ['Bajra','Wheat','Barley','Maize','Gram','Mustard','Cumin','Groundnut','Cotton','Onion','Garlic','Guar'],
  'Sikkim':            ['Rice','Maize','Ginger','Turmeric','Cardamom','Orange','Potato','Buckwheat','Millet','Apple','Pea','Soyabean'],
  'Tamil Nadu':        ['Rice','Sugarcane','Coconut','Groundnut','Cotton','Banana','Mango','Turmeric','Maize','Tapioca','Onion','Chilli'],
  'Telangana':         ['Rice','Cotton','Maize','Chilli','Turmeric','Sugarcane','Soyabean','Groundnut','Mango','Orange','Onion','Tomato'],
  'Tripura':           ['Rice','Jute','Sugarcane','Potato','Mustard','Tea','Rubber','Banana','Pineapple','Orange','Ginger','Jackfruit'],
  'Uttar Pradesh':     ['Wheat','Rice','Sugarcane','Potato','Mustard','Gram','Maize','Bajra','Onion','Tomato','Mango','Banana'],
  'Uttarakhand':       ['Rice','Wheat','Sugarcane','Soyabean','Maize','Potato','Ginger','Turmeric','Apple','Walnut','Mandarin','Litchi'],
  'West Bengal':       ['Rice','Jute','Potato','Tea','Mustard','Sugarcane','Wheat','Maize','Sesame','Mango','Banana','Lentil'],
};

// ─── Realistic price ranges per commodity (₹ per quintal) ────────────
const PRICE_RANGES = {
  'Rice':        { min: 1800, max: 3500 },   'Wheat':       { min: 1800, max: 2800 },
  'Maize':       { min: 1500, max: 2500 },   'Sugarcane':   { min: 280, max: 400 },
  'Cotton':      { min: 5500, max: 7500 },   'Soyabean':    { min: 3500, max: 5000 },
  'Groundnut':   { min: 4500, max: 6500 },   'Mustard':     { min: 4000, max: 5500 },
  'Gram':        { min: 4000, max: 5500 },   'Lentil':      { min: 4500, max: 6000 },
  'Potato':      { min: 800, max: 2000 },    'Onion':       { min: 1000, max: 3500 },
  'Tomato':      { min: 800, max: 4000 },    'Banana':      { min: 1500, max: 3000 },
  'Mango':       { min: 2000, max: 6000 },   'Coconut':     { min: 1500, max: 3000 },
  'Pepper':      { min: 30000, max: 50000 }, 'Cardamom':    { min: 80000, max: 150000 },
  'Turmeric':    { min: 6000, max: 12000 },  'Ginger':      { min: 3000, max: 8000 },
  'Coffee':      { min: 15000, max: 30000 }, 'Tea':         { min: 15000, max: 25000 },
  'Rubber':      { min: 12000, max: 18000 }, 'Cashew':      { min: 8000, max: 14000 },
  'Jute':        { min: 3500, max: 5500 },   'Bajra':       { min: 1800, max: 2800 },
  'Barley':      { min: 1500, max: 2500 },   'Chilli':      { min: 8000, max: 18000 },
  'Cumin':       { min: 15000, max: 35000 }, 'Garlic':      { min: 5000, max: 15000 },
  'Apple':       { min: 5000, max: 12000 },  'Orange':      { min: 2000, max: 5000 },
  'Grapes':      { min: 3000, max: 8000 },   'Litchi':      { min: 3000, max: 8000 },
  'Pineapple':   { min: 1500, max: 4000 },   'Tapioca':     { min: 600, max: 1500 },
  'Areca Nut':   { min: 25000, max: 45000 }, 'Arecanut':    { min: 25000, max: 45000 },
  'Sesamum':     { min: 8000, max: 14000 },  'Sesame':      { min: 8000, max: 14000 },
  'Castor Seed': { min: 4500, max: 6500 },   'Ragi':        { min: 2500, max: 4000 },
  'Tobacco':     { min: 10000, max: 18000 }, 'Pea':         { min: 3000, max: 5000 },
  'Walnut':      { min: 20000, max: 40000 }, 'Millet':      { min: 2000, max: 3500 },
  'Guar':        { min: 4000, max: 6000 },   'Nutmeg':      { min: 40000, max: 80000 },
  'Plum':        { min: 3000, max: 7000 },   'Apricot':     { min: 5000, max: 12000 },
  'Cabbage':     { min: 500, max: 1500 },    'Brinjal':     { min: 800, max: 2500 },
  'Cucumber':    { min: 600, max: 1800 },    'Watermelon':  { min: 500, max: 1500 },
  'Kiwi':        { min: 10000, max: 25000 }, 'Jackfruit':   { min: 1000, max: 3000 },
  'Soyabean':    { min: 3500, max: 5000 },   'Buckwheat':   { min: 3000, max: 5000 },
  'Passion Fruit': { min: 5000, max: 12000 }, 'Mandarin':   { min: 2000, max: 5000 },
};

// ─── Helper: generate realistic price with small daily fluctuation ───
function generateRealisticPrice(commodity, dayOffset = 0) {
  const range = PRICE_RANGES[commodity] || { min: 1000, max: 3000 };
  const basePrice = range.min + (range.max - range.min) * 0.5;
  const volatility = (range.max - range.min) * 0.08;
  const seed = (commodity.charCodeAt(0) * 31 + dayOffset * 7) % 100;
  const fluctuation = (seed / 100 - 0.5) * 2 * volatility;
  const modal = Math.round(basePrice + fluctuation);
  const min = Math.round(modal * (0.85 + (seed % 10) * 0.005));
  const max = Math.round(modal * (1.05 + (seed % 10) * 0.005));
  return { min_price: min, max_price: max, modal_price: modal };
}

// ─── Puppeteer Scraper: commodityonline.com ──────────────────────────
let _browser = null;
async function getBrowser() {
  if (!_browser || !_browser.isConnected()) {
    _browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
    });
  }
  return _browser;
}

async function scrapeLivePrices(commodity, state) {
  let page;
  try {
    const slug = commodity.toLowerCase().replace(/\s+/g, '-');
    const stateSlug = state.toLowerCase().replace(/\s+/g, '-');
    const url = `https://www.commodityonline.com/mandiprices/${slug}/${stateSlug}`;
    console.log(`🌐 Scraping live prices from: ${url}`);

    const browser = await getBrowser();
    page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    // Give the page time to render dynamic content
    await new Promise(r => setTimeout(r, 3000));

    const scraped = await page.evaluate(() => {
      const result = { summary: {}, markets: [] };

      // 1. Extract summary prices from the mandi_highlight section
      const highlightRows = document.querySelectorAll('.mandi_highlight .row div');
      highlightRows.forEach(div => {
        const h4 = div.querySelector('h4');
        const p = div.querySelector('p');
        if (h4 && p) {
          const label = h4.textContent.trim().toLowerCase();
          const priceText = p.textContent.trim();
          const numMatch = priceText.match(/[\d,.]+/);
          const price = numMatch ? parseFloat(numMatch[0].replace(/,/g, '')) : null;
          const unit = priceText.includes('Kg') ? 'Kg' : 'Quintal';
          if (label.includes('average')) result.summary.avg = { price, unit };
          else if (label.includes('lowest')) result.summary.min = { price, unit };
          else if (label.includes('costliest')) result.summary.max = { price, unit };
        }
      });

      // 2. Extract per-market rows from the table inside .mandi_highlight
      const tableRows = document.querySelectorAll('.mandi_highlight table tbody tr');
      tableRows.forEach(tr => {
        const cells = tr.querySelectorAll('td');
        if (cells.length >= 3) {
          const market = cells[0]?.textContent?.trim();
          const variety = cells[1]?.textContent?.trim();
          const priceText = cells[2]?.textContent?.trim() || '';
          const dateText = cells[3]?.textContent?.trim() || '';
          const numMatch = priceText.match(/[\d,.]+/);
          const price = numMatch ? parseFloat(numMatch[0].replace(/,/g, '')) : null;
          if (market && price) {
            result.markets.push({ market, variety, price, date: dateText });
          }
        }
      });

      // 3. Also try to get individual mandi price cards from the main listing
      document.querySelectorAll('.mandi_card, .mandiprices_card, [class*="mandi"][class*="card"]').forEach(card => {
        const links = card.querySelectorAll('a');
        const texts = Array.from(links).map(l => l.textContent.trim()).filter(t => t.length > 0);
        const priceEl = card.querySelector('[class*="price"], p, span');
        if (priceEl) {
          const priceText = priceEl.textContent.trim();
          const numMatch = priceText.match(/[\d,.]+/);
          if (numMatch) {
            const price = parseFloat(numMatch[0].replace(/,/g, ''));
            result.markets.push({ market: texts[texts.length - 1] || 'Unknown', variety: 'Standard', price, date: '' });
          }
        }
      });

      // 4. Fallback: extract from TR rows like "Avg Market Price: ₹980/Quintal"
      if (!result.summary.avg) {
        document.querySelectorAll('tr').forEach(tr => {
          const text = tr.textContent.trim();
          const numMatch = text.match(/₹([\d,.]+)/);
          if (numMatch) {
            const price = parseFloat(numMatch[1].replace(/,/g, ''));
            if (text.toLowerCase().includes('avg')) result.summary.avg = { price, unit: text.includes('Kg') ? 'Kg' : 'Quintal' };
            else if (text.toLowerCase().includes('min')) result.summary.min = { price, unit: text.includes('Kg') ? 'Kg' : 'Quintal' };
            else if (text.toLowerCase().includes('max')) result.summary.max = { price, unit: text.includes('Kg') ? 'Kg' : 'Quintal' };
          }
        });
      }

      return result;
    });

    await page.close();

    // Validate: we need at least the average price
    if (!scraped.summary.avg?.price) {
      console.log('⚠️ Scraper found no valid summary prices, will fallback.');
      return null;
    }

    console.log(`✅ CommodityOnline: avg=₹${scraped.summary.avg?.price}, min=₹${scraped.summary.min?.price}, max=₹${scraped.summary.max?.price}`);
    console.log(`✅ CommodityOnline: ${scraped.markets.length} individual market entries.`);
    return scraped;

  } catch (err) {
    console.error('🌐 CommodityOnline scrape error (will fallback):', err.message);
    if (page) await page.close().catch(() => {});
    return null;
  }
}

// ─── KisanDeals Scraper (lightweight fetch + cheerio) ────────────────
async function scrapeKisanDeals(commodity, state) {
  try {
    const slug = commodity.toUpperCase().replace(/\s+/g, '-');
    const stateSlug = state.toUpperCase().replace(/\s+/g, '-');
    const url = `https://www.kisandeals.com/mandiprices/${slug}/${stateSlug}/ALL`;
    console.log(`🌐 Scraping KisanDeals: ${url}`);

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000);

    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml',
      },
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      console.log(`⚠️ KisanDeals returned ${response.status}`);
      return null;
    }

    const html = await response.text();
    const $ = cheerio.load(html);
    const bodyText = $('body').text();

    let avg = null, min = null, max = null;

    // Flexible regex: handles multi-word crop names like "Areca Nut", "Green Chilli"
    const maxMatch = bodyText.match(/maximum\s+price[^₹]*₹\s*([\d,]+)/i);
    if (maxMatch) max = parseFloat(maxMatch[1].replace(/,/g, ''));

    const minMatch = bodyText.match(/minimum\s+(?:rate|price)[^₹]*₹\s*([\d,]+)/i);
    if (minMatch) min = parseFloat(minMatch[1].replace(/,/g, ''));

    const avgMatch = bodyText.match(/average\s+price[^₹]*₹\s*([\d,]+)/i);
    if (avgMatch) avg = parseFloat(avgMatch[1].replace(/,/g, ''));

    // Fallback: try to extract any ₹ amounts from the summary paragraph
    if (!avg && !min && !max) {
      const allPrices = [...bodyText.matchAll(/₹\s*([\d,]+)\s*(?:per\s+)?(?:Quintal|quintal|QTL)/gi)]
        .map(m => parseFloat(m[1].replace(/,/g, '')))
        .filter(p => p > 50); // filter out tiny values
      if (allPrices.length > 0) {
        min = Math.min(...allPrices);
        max = Math.max(...allPrices);
        avg = Math.round(allPrices.reduce((a, b) => a + b, 0) / allPrices.length);
      }
    }

    if (avg || min || max) {
      const result = {
        avg: avg || min || max,
        min: min || avg || max,
        max: max || avg || min
      };
      console.log(`✅ KisanDeals: avg=₹${result.avg}, min=₹${result.min}, max=₹${result.max}`);
      return result;
    }

    console.log('⚠️ KisanDeals: could not extract prices from page text.');
    return null;
  } catch (err) {
    console.error('🌐 KisanDeals scrape error:', err.message);
    return null;
  }
}

// ─── Gemini Price Estimator ──────────────────────────────────────────
async function getGeminiPriceEstimate(commodity, state) {
  try {
    const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
    if (!GEMINI_API_KEY) return null;

    const prompt = `What is the current average market price (mandi price) of ${commodity} in ${state}, India in Indian Rupees per Quintal as of today? Respond ONLY with a JSON object like this, no markdown, no explanation:
{"avg_price": 1234, "min_price": 1000, "max_price": 1500}
Use realistic, current market prices.`;

    console.log(`🤖 Asking Gemini for ${commodity} price in ${state}...`);

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { temperature: 0.3, maxOutputTokens: 256 }
        })
      }
    );

    const result = await response.json();
    const text = result?.candidates?.[0]?.content?.parts?.[0]?.text || '';

    // Try to parse as JSON first
    try {
      const jsonStr = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
      const parsed = JSON.parse(jsonStr);
      if (parsed.avg_price) {
        console.log(`✅ Gemini: avg=₹${parsed.avg_price}, min=₹${parsed.min_price}, max=₹${parsed.max_price}`);
        return { avg: parsed.avg_price, min: parsed.min_price || parsed.avg_price, max: parsed.max_price || parsed.avg_price };
      }
    } catch (_) {
      // JSON parsing failed, try regex fallback
    }

    // Regex fallback: extract prices from Gemini text responses
    const avgM = text.match(/avg(?:_price)?[":\s]+(\d+)/i);
    const minM = text.match(/min(?:_price)?[":\s]+(\d+)/i);
    const maxM = text.match(/max(?:_price)?[":\s]+(\d+)/i);
    if (avgM) {
      const av = parseInt(avgM[1]), mn = minM ? parseInt(minM[1]) : av, mx = maxM ? parseInt(maxM[1]) : av;
      console.log(`✅ Gemini (regex): avg=₹${av}, min=₹${mn}, max=₹${mx}`);
      return { avg: av, min: mn, max: mx };
    }

    // Last resort: find any ₹ amounts
    const rupeeMatches = [...text.matchAll(/₹\s*([\d,]+)/g)].map(m => parseInt(m[1].replace(/,/g, '')));
    if (rupeeMatches.length > 0) {
      const av = Math.round(rupeeMatches.reduce((a, b) => a + b, 0) / rupeeMatches.length);
      console.log(`✅ Gemini (₹ fallback): avg=₹${av}`);
      return { avg: av, min: Math.min(...rupeeMatches), max: Math.max(...rupeeMatches) };
    }

    console.log('⚠️ Gemini returned no parseable price data:', text.substring(0, 100));
    return null;
  } catch (err) {
    console.error('🤖 Gemini price estimate error:', err.message);
    return null;
  }
}

// ─── Multi-Source Price Fusion ────────────────────────────────────────
// Scrapes from CommodityOnline + KisanDeals + Gemini in parallel,
// then averages the results for accuracy.
async function getMultiSourcePrices(commodity, state) {
  console.log(`\n━━━ Multi-Source Price Fetch: ${commodity} in ${state} ━━━`);

  // Run all three sources in parallel for speed
  const [coResult, kdResult, geminiResult] = await Promise.all([
    scrapeLivePrices(commodity, state),
    scrapeKisanDeals(commodity, state),
    getGeminiPriceEstimate(commodity, state)
  ]);

  const sources = [];
  const avgPrices = [];
  const minPrices = [];
  const maxPrices = [];

  // CommodityOnline
  if (coResult?.summary?.avg?.price) {
    const co = coResult.summary;
    avgPrices.push(co.avg.price);
    minPrices.push(co.min?.price || co.avg.price);
    maxPrices.push(co.max?.price || co.avg.price);
    sources.push('CommodityOnline');
  }

  // KisanDeals
  if (kdResult?.avg) {
    avgPrices.push(kdResult.avg);
    minPrices.push(kdResult.min);
    maxPrices.push(kdResult.max);
    sources.push('KisanDeals');
  }

  // Gemini
  if (geminiResult?.avg) {
    avgPrices.push(geminiResult.avg);
    minPrices.push(geminiResult.min);
    maxPrices.push(geminiResult.max);
    sources.push('Gemini AI');
  }

  if (avgPrices.length === 0) {
    console.log('⚠️ No sources returned valid prices. Will use fallback.');
    return null;
  }

  // Average across all available sources
  const fusedAvg = Math.round(avgPrices.reduce((a, b) => a + b, 0) / avgPrices.length);
  const fusedMin = Math.round(minPrices.reduce((a, b) => a + b, 0) / minPrices.length);
  const fusedMax = Math.round(maxPrices.reduce((a, b) => a + b, 0) / maxPrices.length);

  console.log(`\n🔀 FUSED (${sources.join(' + ')}): avg=₹${fusedAvg}, min=₹${fusedMin}, max=₹${fusedMax}`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

  return {
    avg: fusedAvg,
    min: fusedMin,
    max: fusedMax,
    sources,
    markets: coResult?.markets || []
  };
}

// ─── 1) Get crops for a state ────────────────────────────────────────
exports.getCrops = async (req, res) => {
  try {
    const { state } = req.query;
    if (!state) return res.status(400).json({ success: false, message: 'State is required' });

    const crops = STATE_CROPS[state] || STATE_CROPS['Kerala'];
    res.json({ success: true, data: crops });
  } catch (error) {
    console.error('getCrops error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
};

// ─── 2) Get live prices (scrape + fallback to mock) ──────────────────
exports.getPrices = async (req, res) => {
  try {
    const { state, district, commodity } = req.query;
    if (!state || !commodity) {
      return res.status(400).json({ success: false, message: 'State and commodity are required' });
    }

    // Check cache (within last 30 minutes)
    const cacheKey = { state, commodity };
    if (district) cacheKey.district = district;

    const cached = await MarketPrice.find({
      ...cacheKey,
      fetched_at: { $gte: new Date(Date.now() - 30 * 60 * 1000) }
    }).sort({ arrival_date: -1 }).limit(1);

    if (cached.length > 0) {
      const src = cached[0].scraped ? 'scraped_live' : 'cache';
      return res.json({ success: true, data: cached, source: src });
    }

    // ─── Try multi-source live data (CommodityOnline + KisanDeals + Gemini) ───
    const fused = await getMultiSourcePrices(commodity, state);

    if (fused) {
      const now = new Date();

      // Create a single summary record with the fused price
      const record = await MarketPrice.create({
        state,
        district: district || '',
        market: `${district || state} Market`,
        commodity,
        variety: 'Standard',
        grade: 'Standard',
        min_price: fused.min,
        max_price: fused.max,
        modal_price: fused.avg,
        arrival_date: now,
        fetched_at: now,
        scraped: true
      });

      return res.json({ success: true, data: [record], source: 'scraped_live', sources: fused.sources });
    }

    // ─── Fallback: generate realistic mock prices ────────────────
    console.log('📊 Falling back to generated prices.');
    const varieties = ['FAQ', 'Standard', 'Premium'];
    const marketName = `${district || state} Market`;
    const now = new Date();
    const records = [];

    for (const variety of varieties) {
      const prices = generateRealisticPrice(commodity, variety.charCodeAt(0));
      const record = await MarketPrice.create({
        state,
        district: district || '',
        market: marketName,
        commodity,
        variety,
        grade: variety,
        ...prices,
        arrival_date: now,
        fetched_at: now
      });
      records.push(record);
    }

    res.json({ success: true, data: records, source: 'generated' });
  } catch (error) {
    console.error('getPrices error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
};

// ─── 3) Get price history (7 days, anchored on live price) ──────────
exports.getPriceHistory = async (req, res) => {
  try {
    const { state, commodity, days = 7 } = req.query;
    if (!state || !commodity) {
      return res.status(400).json({ success: false, message: 'State and commodity are required' });
    }

    const numDays = parseInt(days);
    let todayModal = null;
    let todayMin = null;
    let todayMax = null;
    let isLive = false;
    let liveSources = [];

    // ─── Try multi-source fusion for today's price ─────────────────
    const fused = await getMultiSourcePrices(commodity, state);
    if (fused) {
      todayModal = fused.avg;
      todayMin = fused.min;
      todayMax = fused.max;
      isLive = true;
      liveSources = fused.sources;
      console.log(`📈 Fused price anchor (${fused.sources.join(' + ')}): avg=₹${todayModal}, min=₹${todayMin}, max=₹${todayMax}`);
    } else {
      // Fallback to generated price for today
      const gen = generateRealisticPrice(commodity, 0);
      todayModal = gen.modal_price;
      todayMin = gen.min_price;
      todayMax = gen.max_price;
    }

    // ─── Build 7-day chart data ending with today ─────────────────
    const chartData = [];
    const today = new Date();

    for (let i = numDays - 1; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(today.getDate() - i);
      const dateStr = date.toISOString().split('T')[0];

      if (i === 0) {
        // Today → use live / current data
        chartData.push({
          date: dateStr,
          min_price: todayMin,
          max_price: todayMax,
          modal_price: todayModal,
          live: isLive,
          predicted: false
        });
      } else {
        // Past days → generate realistic fluctuations anchored on today's price
        const volatility = todayModal * 0.04;
        const seed = (commodity.charCodeAt(0) * 17 + i * 13 + commodity.length * 7) % 100;
        const direction = ((seed % 2 === 0) ? 1 : -1);
        const fluctuation = direction * (seed / 100) * volatility * (i * 0.3);
        
        const modal = Math.round(todayModal + fluctuation);
        const spread = todayModal * 0.12;
        const min = Math.round(modal - spread * (0.5 + (seed % 30) / 100));
        const max = Math.round(modal + spread * (0.5 + (seed % 20) / 100));

        chartData.push({
          date: dateStr,
          min_price: min,
          max_price: max,
          modal_price: modal,
          live: false,
          predicted: false
        });
      }
    }

    // ─── 7-Day Price Prediction (trend-based projection) ──────────
    // Calculate the trend from our historical data
    const pastModalPrices = chartData.map(d => d.modal_price);
    const firstPrice = pastModalPrices[0];
    const lastPrice = pastModalPrices[pastModalPrices.length - 1];
    const dailyTrend = (lastPrice - firstPrice) / (pastModalPrices.length - 1); // avg daily change

    for (let i = 1; i <= 7; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      const dateStr = date.toISOString().split('T')[0];

      // Apply trend + dampening (trend fades over time) + seeded volatility
      const trendComponent = dailyTrend * i * (1 - i * 0.08); // dampen trend further out
      const seed = (commodity.charCodeAt(0) * 23 + i * 31 + commodity.length * 11) % 100;
      const noise = ((seed - 50) / 50) * todayModal * 0.02 * i; // small random-seeded noise

      const predictedModal = Math.round(todayModal + trendComponent + noise);
      const predictedMin = Math.round(predictedModal * (todayMin / todayModal));
      const predictedMax = Math.round(predictedModal * (todayMax / todayModal));

      chartData.push({
        date: dateStr,
        min_price: predictedMin,
        max_price: predictedMax,
        modal_price: predictedModal,
        live: false,
        predicted: true
      });
    }

    res.json({ success: true, data: chartData, source: isLive ? 'scraped_live' : 'generated', sources: liveSources });
  } catch (error) {
    console.error('getPriceHistory error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
};

// ─── 4) Gemini-powered market insights ──────────────────────────────
exports.getInsights = async (req, res) => {
  try {
    const { commodity, state, district, modal_price, min_price, max_price } = req.body;
    if (!commodity || !state) {
      return res.status(400).json({ success: false, message: 'Commodity and state are required' });
    }

    const todayStr = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
    const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
    if (!GEMINI_API_KEY) {
      return res.json({
        success: true,
        data: {
          summary: `${commodity} is trading at ₹${modal_price || 'N/A'}/quintal in ${district || state} as of ${todayStr}. The price spread of ₹${min_price || 'N/A'} to ₹${max_price || 'N/A'} indicates moderate market activity.`,
          tips: [
            `Compare prices across nearby mandis before selling ${commodity}.`,
            `Current price spread (₹${min_price} - ₹${max_price}) suggests moderate demand.`,
            `Consider storage if you expect prices to rise in the coming weeks.`,
            `Check APMC rates and government MSP announcements regularly.`,
            `Transport costs can eat into margins — sell at the nearest high-price mandi.`,
            `Grade and sort your ${commodity} well — quality premiums can add 5-15% to the price.`
          ],
          trend: 'stable',
          recommendation: 'hold',
          forecast: `${commodity} prices are expected to remain around ₹${modal_price}/quintal over the next 2 weeks with minor fluctuations.`,
          demandSupply: `Current supply levels appear normal for ${state}. Demand is expected to remain steady through the season.`,
          seasonalNote: `This is a typical trading period for ${commodity} in ${state}. Prices may fluctuate based on arrivals and weather conditions.`,
          riskLevel: 'medium',
          bestStrategy: `Store ${commodity} if you have adequate facilities and sell when prices peak. Monitor daily mandi rates.`,
          priceRange: { current: modal_price || 0, weekLow: min_price || 0, weekHigh: max_price || 0 }
        }
      });
    }

    const prompt = `You are a seasoned Indian agricultural commodity market analyst with 20+ years of experience. Analyze the following real-time mandi data and provide comprehensive, farmer-friendly market insights.

📊 MARKET DATA:
- Crop: ${commodity}
- State: ${state}
- District: ${district || 'N/A'}
- Date: ${todayStr}
- Modal Price: ₹${modal_price || 'N/A'}/quintal
- Min Price: ₹${min_price || 'N/A'}/quintal
- Max Price: ₹${max_price || 'N/A'}/quintal

Return a JSON object with these EXACT keys (respond ONLY with valid JSON, no markdown, no explanation):
{
  "summary": "4-5 sentence detailed market analysis covering current price levels, comparison with national averages, and any notable market movements. Include specific numbers.",
  "tips": ["tip1", "tip2", "tip3", "tip4", "tip5", "tip6"],
  "trend": "rising" or "falling" or "stable",
  "recommendation": "buy" or "sell" or "hold",
  "forecast": "3-4 sentence specific price forecast for the next 1-2 weeks with expected price ranges in ₹/quintal. Be specific with numbers.",
  "demandSupply": "2-3 sentences about current demand-supply dynamics for this crop in this region. Mention factors like arrivals, stock levels, and buyer activity.",
  "seasonalNote": "1-2 sentences about seasonal factors affecting this crop right now (e.g., harvest season, sowing period, festival demand, weather impact).",
  "riskLevel": "low" or "medium" or "high",
  "bestStrategy": "2-3 sentences of specific, actionable strategy for farmers — when to sell, how to maximize returns, storage advice.",
  "priceRange": {"current": ${modal_price || 0}, "weekLow": ${min_price || 0}, "weekHigh": ${max_price || 0}}
}

IMPORTANT: Make ALL tips highly specific and actionable for ${commodity} farmers in ${state}. Include real market factors, government schemes (like PM-AASHA, MSP), and practical advice. Each tip should be 1-2 sentences. Be honest about risks.`;

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { temperature: 0.7, maxOutputTokens: 1024 }
        })
      }
    );

    const result = await response.json();
    const text = result?.candidates?.[0]?.content?.parts?.[0]?.text || '';

    // Parse JSON from Gemini response
    let insights;
    try {
      const jsonStr = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
      insights = JSON.parse(jsonStr);
    } catch {
      insights = {
        summary: text.substring(0, 500) || `${commodity} market analysis for ${state}.`,
        tips: [`Monitor ${commodity} prices in ${district || state} regularly.`],
        trend: 'stable',
        recommendation: 'hold',
        forecast: `Prices expected to remain around ₹${modal_price}/quintal.`,
        demandSupply: 'Normal supply and demand conditions.',
        seasonalNote: 'No major seasonal factors at this time.',
        riskLevel: 'medium',
        bestStrategy: `Monitor daily prices and sell at the best opportunity.`
      };
    }

    res.json({ success: true, data: insights });
  } catch (error) {
    console.error('getInsights error:', error);
    res.status(500).json({ success: false, message: 'Failed to generate insights' });
  }
};

// ─── 5) Create transaction (buy/sell) ────────────────────────────────
exports.createTransaction = async (req, res) => {
  try {
    const { farmer, type, commodity, variety, market, state, district, quantity, unit, price_per_unit, total_price, notes } = req.body;

    if (!farmer || !type || !commodity || !quantity || !price_per_unit) {
      return res.status(400).json({ success: false, message: 'Missing required fields' });
    }

    const transaction = await Transaction.create({
      farmer, type, commodity, variety, market, state, district,
      quantity, unit: unit || 'quintal',
      price_per_unit, total_price: total_price || (quantity * price_per_unit),
      notes
    });

    res.status(201).json({ success: true, data: transaction });
  } catch (error) {
    console.error('createTransaction error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
};

// ─── 6) List transactions for a farmer ───────────────────────────────
exports.listTransactions = async (req, res) => {
  try {
    const { farmer_id, type, status } = req.query;
    if (!farmer_id) return res.status(400).json({ success: false, message: 'farmer_id is required' });

    const query = { farmer: farmer_id };
    if (type) query.type = type;
    if (status) query.status = status;

    const transactions = await Transaction.find(query)
      .sort({ createdAt: -1 })
      .limit(50)
      .populate('farmer', 'name phone');

    res.json({ success: true, data: transactions });
  } catch (error) {
    console.error('listTransactions error:', error);
    res.status(500).json({ success: false, message: 'Server error' });
  }
};
