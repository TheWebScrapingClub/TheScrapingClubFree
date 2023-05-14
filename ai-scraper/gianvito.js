const axios = require('axios');
const cheerio = require('cheerio');

const startUrl = 'https://www.gianvitorossi.com/it_it';

async function scrape(url) {
  try {
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);

    // Extract product categories
    const productPages = $('a[role="menuitem"]').map(function() {
      return $(this).attr('href');
    }).get();

    for (const productPage of productPages) {
      await getProducts(`https://www.gianvitorossi.com${productPage}`);
    }
  } catch (error) {
    console.error(error);
  }
}

async function getProducts(url) {
  try {
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);

    // Extract product links
    const productLinks = $('a.b-product_tile-image_link').map(function() {
      return $(this).attr('href');
    }).get();

    for (const link of productLinks) {
      await getProductDetails(`https://www.gianvitorossi.com${link}`);
    }

    // Check for more product pages
    try {
      const nextPage = $('a[data-event-click.prevent="loadMore"]').attr('href');
      await getProducts(`https://www.gianvitorossi.com${nextPage}`);
    } catch (error) {
      // No more product pages
    }
  } catch (error) {
    console.error(error);
  }
}

async function getProductDetails(url) {
  try {
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);

    // Extract JSON data
    const jsonText = $('script[type="application/ld+json"]')[0].children[0].data;
    const data = JSON.parse(jsonText);

    // Extract product details
    const productCode = data.mpn;
    const fullPrice = data.offers.price;
    const price = fullPrice;
    const productUrl = response.config.url;

    // Output data
    console.log({
      productCode: productCode,
      fullPrice: fullPrice,
      price: price,
      productUrl: productUrl
    });
  } catch (error) {
    console.error(error);
  }
}

scrape(startUrl);