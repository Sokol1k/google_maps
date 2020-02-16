const puppeteer = require("puppeteer");
const amqplib = require("amqplib/callback_api");
require("dotenv").config();

class GoogleMaps {
  constructor() {
    this.browser = null;
    this.page = null;
    this.url =
      // "https://www.google.com.ua/maps/search/restaurant/@34.031427,-118.289711,15z";
    this.url = null;
    this.sector_channel = null;
    this.items_channel = null;
    this.sector_connection = null;
    this.items_connection = null;
    this.haveUrl = false;
    // this.center_latitude = 34.031427;
    this.center_latitude = null;
    // this.center_longitude = -118.289711;
    this.center_longitude = null;
    this.item_data = {};
    this.radius = parseFloat(process.env.STEP_KM) / 2;
    this.rabbit_url = process.env.RABBIT_URL;
    this.rabbit_sector_queue = process.env.RABBIT_SECTOR_QUEUE;
    this.rabbit_sector_exchange = process.env.RABBIT_SECTOR_EXCHANGE;
    this.rabbit_sector_rounting_key = process.env.RABBIT_SECTOR_ROUNTING_KEY;
    this.rabbit_items_queue = process.env.RABBIT_ITEMS_QUEUE;
    this.rabbit_items_exchange = process.env.RABBIT_ITEMS_EXCHANGE;
    this.rabbit_items_rounting_key = process.env.RABBIT_ITEMS_ROUNTING_KEY;
  }

  connectToSectorsQueue() {
    amqplib.connect(this.rabbit_url, (error1, connection) => {
      if (error1) {
        throw error1;
      }
      this.sector_connection = connection;
      this.sector_connection.createChannel((error2, channel) => {
        if (error2) {
          throw error2;
        }

        this.sector_channel = channel;

        this.sector_channel.prefetch(1);

        this.sector_channel.assertExchange(
          this.rabbit_sector_exchange,
          "direct",
          {
            durable: false
          }
        );

        this.sector_channel.assertQueue(this.rabbit_sector_queue, {
          durable: true
        });

        this.sector_channel.bindQueue(
          this.rabbit_sector_queue,
          this.rabbit_sector_exchange,
          this.rabbit_sector_rounting_key
        );
        this.sector_channel.consume(
          this.rabbit_sector_queue,
          msg => {
            if (msg && !this.haveUrl) {
              let sector = JSON.parse(msg.content.toString());
              this.center_latitude = parseFloat(sector.center_latitude);
              this.center_longitude = parseFloat(sector.center_longitude);
              this.url =
                "https://www.google.com/maps/search/" +
                sector.keyword +
                "/@" +
                sector.center_latitude +
                "," +
                sector.center_longitude +
                ",15z";
              this.haveUrl = true;
              this.sector_channel.ack(msg);
            }
          },
          { noAck: false }
        );
      });
    });
  }

  connectToItemsQueue() {
    amqplib.connect(this.rabbit_url, (error1, connection) => {
      if (error1) {
        throw error1;
      }
      this.items_connection = connection;
      this.items_connection.createChannel((error2, channel) => {
        if (error2) {
          throw error2;
        }

        this.items_channel = channel;

        this.items_channel.assertExchange(
          this.rabbit_items_exchange,
          "direct",
          {
            durable: true
          }
        );

        this.items_channel.assertQueue(this.rabbit_items_queue, {
          durable: true
        });

        this.items_channel.bindQueue(
          this.rabbit_items_queue,
          this.rabbit_items_exchange,
          this.rabbit_items_rounting_key
        );
      });
    });
  }

  publish(queue, content) {
    try {
      this.items_channel.sendToQueue(queue, Buffer.from(content));
      console.log("Data add to queue!");
    } catch (e) {
      throw e;
    }
  }

  async createPuppetter() {
    try {
      this.browser = await puppeteer.launch({
        args: ["--proxy-server=http://192.168.11.82:9966"]
      });
      this.page = await this.browser.newPage();
      await this.page.setRequestInterception(true);
      this.page.on("request", request => {
        if (["stylesheet", "font"].indexOf(request.resourceType()) !== -1) {
          request.abort();
        } else {
          request.continue();
        }
      });
      await this.page.waitFor(2000);
      if (this.url == null) {
        throw "Error: Url cannot be null!";
      }
      await this.page.goto(this.url);
      // await this.page.waitForSelector(".widget-consent-button-later");
      // await this.page.click(".widget-consent-button-later");
    } catch (e) {
      throw e;
    }
  }

  async isLastPage() {
    try {
      return await this.page.evaluate(() => {
        let nextButton = document.getElementById(
          "n7lv7yjyC35__section-pagination-button-next"
        );
        if (nextButton != null) {
          return nextButton.getAttribute("disabled") == null ? true : false;
        }
        return false;
      });
    } catch (e) {
      throw e;
    }
  }

  async countItems() {
    try {
      return await this.page.evaluate(() => {
        let items = document.querySelectorAll('[role="listitem"]');
        return items.length;
      });
    } catch (e) {
      throw e;
    }
  }

  async openItem(index) {
    try {
      await this.page.waitForSelector(`[data-result-index='${index}']`);
      await this.page.click(`[data-result-index='${index}']`);
    } catch (e) {
      throw e;
    }
  }

  async goBack() {
    try {
      await this.page.waitForSelector(".section-back-to-list-button");
      await this.page.click(".section-back-to-list-button");
    } catch (e) {
      throw e;
    }
  }

  async checkGeolocation() {
    let url = String(this.page.url()).split("!");
    this.item_data["url"] = this.page.url();
    this.item_data["latitude"] = parseFloat(url[url.length - 2].split("d")[1]);
    this.item_data["longitude"] = parseFloat(url[url.length - 1].split("d")[1]);

    let result =
      Math.pow(this.center_latitude - this.item_data["latitude"], 2) +
        Math.pow(this.center_longitude - this.item_data["longitude"], 2) <=
      Math.pow(this.radius, 2);

    if (result) {
      await this.parseData();
      return true;
    } else {
      return false;
    }
  }

  async parseData() {
    let result = await this.page.evaluate(() => {
      let name = document.querySelector("h1").innerText;

      let temp = document.querySelector('div[data-section-id*="ad"]');

      if (temp != null) {
        try {
          var full_address = temp.querySelector("span.widget-pane-link")
            .innerText;
        } catch (e) {
          throw "Error: item 'full_address' not found";
        }
        temp = full_address.split(", ");
        var address = temp[0];
        var city = temp[1];
        var zipcode = temp[2];
        var country = temp[3];
      } else {
        var full_address = null;
        var address = null;
        var city = null;
        var zipcode = null;
        var country = null;
      }

      temp = document.querySelector('button[jsaction*="pane.rating.category"]');

      if (temp != null) {
        try {
          var category = temp.innerText;
        } catch (e) {
          throw "Error: item 'category' not found";
        }
      } else {
        var category = null;
      }

      temp = document.querySelector('div[data-section-id*="pn0"]');

      if (temp != null) {
        try {
          var phone = temp.querySelector('span[class*="widget-pane-link"]')
            .innerText;
        } catch (e) {
          throw "Error: item 'phone' not found";
        }
      } else {
        var phone = null;
      }

      temp = document.querySelector('div[data-section-id*="ap"]');

      if (temp != null) {
        try {
          var website = temp.querySelector('span[class*="widget-pane-link"]')
            .innerText;
        } catch (e) {
          throw "Error: item 'website' not found";
        }
      } else {
        var website = null;
      }

      temp = document.querySelector('div[data-section-id*="mcta"]');

      if (temp) {
        claimed_business = true;
      } else {
        claimed_business = false;
      }

      temp = document.querySelector('span[class*="section-star-display"]');

      if (temp != null) {
        try {
          temp = temp.innerText.split(",");
        } catch (e) {
          throw "Error: item 'rating' not found";
        }

        var rating = parseFloat(temp[0] + "." + temp[1]);
      } else {
        var rating = null;
      }

      temp = document.querySelector(
        'button[jsaction*="pane.rating.moreReviews"]'
      );

      if (temp != null) {
        try {
          var reviews = parseInt(temp.innerText.slice(1, -1));
        } catch (e) {
          throw "Error: item 'reviews' not found";
        }
      } else {
        var reviews = null;
      }

      temp = document.querySelector(
        'button[jsaction*="pane.heroHeaderImage.click"]'
      );

      if (temp != null) {
        var image = temp.querySelector("img");
        image = btoa(image.getAttribute("src"));
      } else {
        var image = null;
      }

      return {
        name,
        full_address,
        address,
        city,
        zipcode,
        country,
        category,
        phone,
        website,
        claimed_business,
        rating,
        reviews,
        image
      };
    });
    this.item_data = Object.assign(this.item_data, result);
  }

  async startParse() {
    try {
      while (await this.isLastPage()) {
        let countItems = await this.countItems();
        if (!countItems) {
          break;
        }
        for (let index = 1; index <= countItems; index++) {
          await this.openItem(index);
          await this.page.waitFor(3000);
          let result = await this.checkGeolocation();
          if (result) {
            console.log(this.item_data);
            this.publish(
              this.rabbit_items_queue,
              JSON.stringify(this.item_data)
            );
          }
          await this.goBack();
          await this.page.waitFor(2000);
        }
        await this.page.waitForSelector(
          '[id="n7lv7yjyC35__section-pagination-button-next"]'
        );
        await this.page.click(
          '[id="n7lv7yjyC35__section-pagination-button-next"]'
        );
        await this.page.waitFor(2000);
      }
    } catch (e) {
      throw e;
    }
  }

  async close() {
    await this.browser.close();
    this.sector_connection.close();
    this.items_connection.close();
  }

  async parse() {
    try {
      this.connectToSectorsQueue();
      this.connectToItemsQueue();
      await this.createPuppetter();
      await this.page.waitFor(2000);
      await this.startParse();
    } catch (e) {
      console.log(e);
    }
    await this.close();
  }
}

let maps = new GoogleMaps();
maps.parse();
