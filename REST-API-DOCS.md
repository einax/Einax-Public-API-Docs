# EINAX REST API DOCS

## General Information

* The base API endpoint is https://einax.com/api/v1/
* All endpoints return JSON objects or array.
* All timestamps are given in milliseconds
* For GET endpoints, parameters must be sent as a query string.
* For POST endpoints, the parameters may be sent as request body
* Parameters may be sent in any order.
* Any endpoint can return ERROR. The error payload is as follows:
```JS
{
  "code": 121
}
```
* Specific error codes will be defined in another document

## LIMITS
* During Beta testing einax API have limits of 5 requests per second for all endpoints.
* If limits are violated a 429 error will be returned
* Repeatedly violating rate limits will result in an automated IP ban

## Endpoint security type
* Einax has two types of endpoints - public and signed.
* Public endpoints available to everyone.
* Signed endpoints require user authentication using valid API-Key and signature.
* API-keys are passed into the Rest API via the X-MBX-APIKEY header.
* API-keys and secret-keys are case sensitive.
* Signed endpoints require an additional parameters: (signature, recv_window and timestamp).
* Endpoints use HMAC SHA256 signatures. The HMAC SHA256 signature is a keyed HMAC SHA256 operation. Use your secretKey as the key and totalParams as the value for the HMAC operation.
* The signature is not case sensitive
* totalParams is defined as the request body.
* Besides trading timing precision recv_window and timestamp parameters are also provide additional layer of security meaning that request replay attack won't work unless it has been replayed within relatively small timeframe (equal to recv_window).

## Public API endpoints

### Server Time

Returns server time in milliseconds. Should be used as a test of connectivity and as a means
to account for latency between you and the server.

**Request:**
```
GET /api/v1/time
```

**Response:**

```JS
{
  1545294344155
}
```
### Currencies

Returns array of digital assets listed on the platform. Please note that this list contains
all currencies opened for deposits and withdrawals. Markets can be disabled for those currencies.
To see the list of active markets please refer to markets endpoint.

**Request:**
```
GET /api/v1/finance/currencies/
```
**Response:**

```JS
[{
	"ticker": "ETH",                  //Currency Symol
  
	"name": "Ethereum",               //Currency Full name
  
	"description": null,              //Short description of the currency or link to it's website.
  
	"parent_id": "null",              /*Ticker of the parent currency (for ETH tokens it will be ETH). 
	This is  null if the currency is it's own parent.*/
	
	"withdraw_fee": "0.0001",         /*Withdrawal fee (measured in parent currency. 
	If parent_id is null withdrawal fee will be processed in this currency) */
	
	"sort_order": 1500,               /*A number represents how high currency is displayed 
	in currencies list */	
	
	"active_withdraw": true,          /*Shows if withdrawals for this currency are enabled 
	at the time of request*/
  
	"active_deposit": true,           /*Shows if deposits for this currency are enabled 
	at the time of request*/
  
	"decimals": "1000000000000000000" /*Shows how many elementary units of currency contained in single token
	(number of Satoshis in 1 BTC or number of Weis in 1 ETH) */
  
}, {
	"ticker": "WT",
	"name": "Welcome Token",
	"description": null,
	"withdraw_fee": "0.001",
	"sort_order": 2500,
	"active_withdraw": true,
	"active_deposit": true,
	"decimals": "1000000000000000000"
}, {
	"ticker": "TOKEN",
	"name": "Token name",
	"description": "https://www.website.address/",
	"withdraw_fee": "0.001",
	"sort_order": 24500,
	"active_withdraw": true,
	"active_deposit": true,
	"decimals": "100000000"
}]
```

### Markets

Returns an array of the active markets. Please note that this endpoint will NOT return state of the markets (like last price, volume, etc) only a static market characteristics will be returned. For dynamic market stats
please refer to _/api/v1/history/quotes/_ endpoint

**Request:**
```
GET api/v1/finance/markets/
```

**Response:**

```JS
[{
	"first_currency": "ZRX",                    //a currency traded on this market.
  
	"second_currency": "ETH",                   //a base currency of the market (liquidity currency).
  
	"description": "",                          //additional information about market.
  
	"active": true,                             //False if trading is disabled. True otherwise
  
	"maker_fee": "0.001",                       /*If order is executed as a maker order, 
	an amount to be received will be multiplied by this number and subtracted as a fee. 
	Read 0.001 as "0.1% maker fee".*/
  
	"taker_fee": "0.001",                       /*If order is executed as a taker order, 
	an amount to be received will be multiplied by this number and subtracted as a fee. 
	Read 0.001 as "0.1% taker fee".*/
  
	"minimum_allowed_price": "0.00000001",      //A minimum price this asset can be sold or bought for. 
    
	"step": "0.00000001",                       //A minimum price increment.
  
	"min_volume_limit": "0.00001",              /*A minimum amount of liquidity that have to be used 
	to create limit order (i.e. you can't create buy order that buys an amount of tokens less then 
	0.00001 worth of ETH, and you can't sell an amount that will total in 0.00001 ETH after being sold)*/
  
	"min_volume_market": "0.00001"              /*A minimum amount of liquidity that have to be used 
	to create market order (i.e. you can't create buy order that buys an amount of tokens less then 
	0.00001 worth of ETH, and you can't sell an amount that will total in 0.00001 ETH after being sold)*/
  
}, {
	"first_currency": "CETH",
	"second_currency": "ETH",
	"description": "",
	"active": true,
	"maker_fee": "0.001",
	"taker_fee": "0.001",
	"minimum_allowed_price": "0.00000001",
	"step": "0.00000001",
	"min_volume_limit": "0.00001",
	"min_volume_market": "0.00001"
}, {
	"first_currency": "GMC",
	"second_currency": "ETH",
	"description": "",
	"active": true,
	"maker_fee": "0.001",
	"taker_fee": "0.001",
	"minimum_allowed_price": "0.00000001",
	"step": "0.00000001",
	"min_volume_limit": "0.00001",
	"min_volume_market": "0.00001"
}, {
	"first_currency": "ZDX",
	"second_currency": "ETH",
	"description": "",
	"active": true,
	"maker_fee": "0.001",
	"taker_fee": "0.001",
	"minimum_allowed_price": "0.00000001",
	"step": "0.00000001",
	"min_volume_limit": "0.00001",
	"min_volume_market": "0.00001"
}, {
	"first_currency": "TICO",
	"second_currency": "ETH",
	"description": "",
	"active": true,
	"maker_fee": "0.001",
	"taker_fee": "0.001",
	"minimum_allowed_price": "0.00000001",
	"step": "0.00000001",
	"min_volume_limit": "0.00001",
	"min_volume_market": "0.00001"
}]
```

### Ticker

Returns an array of objects with data that each describe current state of the active markets. Can be used to fetch latest market data or get list of market symbols. This information being updated
every minute. For more recent market information please refer to specific market or WebSockets API.

**Request:**
```
GET /api/v1/ticker/24h/
```

**Response:**

```JS
[  
   {  
      "s":"CETH:ETH",    //Market symbol (trading pair)
      "h":"0.00002000",  //Highest price accounted during past 24 hours
      "l":"0.000000100", //Lowest price accounted during past 24 hours
      "o":"0.00001500",  //Price accounted 24 hours ago
      "c":"0.00002000"   //Last price
      "v":"0.1"          //Trade volume measured in liquidity (ETH)
   }
]
```
### Trades

Returns last trades that have been executed on specific market.

```
POST /api/v1/history/trades/
```
**Parameters:**

|Name           |Type           |Mandatory |Description|Example|
| ------------- |:-------------:|:--------:|-----------|:-----:|
|   market      |STRING         |YES       |Market name consists of two assets symbols, separated by ":" (first is the symbol of asset traded and the second is liquidity asset symbol).|CETH:ETH
|limit          |INT            |YES       |Number of trades to be fetched. 3 will fetch 3 most recent trades. You can set this number to get maximum of 500 most recent trades.|3|

**Response:**

```JS
[  
   {  
      "t":1545256499,               //server timestamp of the trade
      "p":"0.00020000000000000000", //price that was used for the trade
      "a":"1.70070000000000000000", //amount of assets traded
      "b":true                      /*true if buyer was also a market maker 
      (buy order from order book was executed)*/
   },
   {  
      "t":1545154163,
      "p":"0.00020000000000000000",
      "a":"0.29930000000000000000",
      "b":false
   },
   {  
      "t":1545133399,
      "p":"0.00020000000000000000",
      "a":"0.00010000000000000000",
      "b":false
   },

]
```

### Candles (K-line)

Returns array of K-line data for current market .

```
POST /api/v1/history/trades/
```
**Parameters:**

|Name           |Type           |Mandatory |Description|Example|
| ------------- |:-------------:|:--------:|-----------|:-----:|
|market         |  STRING       |YES          |Market name consists of two assets symbols, separated by ":" (first is the symbol of asset traded and the second is liquidity asset symbol).|  CETH:ETH    |
|limit          |INT            |YES       |Number of data points (candles) to fetch. You can set this number to get maximum of 500 most recent candles.|2|
|interval   | ENUM  | YES  |  Time interval  between data points. |1m   |  
|start   |TIMESTAMP   |YES   |Timestamp of the last candle to be fetched. Example request will fetch 2 candles of which most recent will have timestamp < 1545306615   |1545306615   |


**ENUM definition:**

```
interval
```
A string value describing time interval during which a single point of K-line data being collected. Intervals are varying between 1 minute and 1 Month. Following values are allowed:
* 1m
* 3m
* 5m
* 15m
* 30m
* 1h
* 2h
* 4h
* 6h
* 8h
* 12h
* 1d
* 3d
* 1w
* 1M

**Response:**

```JS
[  
   {  
      "o":"0.00020000000000000000", //Open price
      "c":"0.00020000000000000000", //Close price (current price if the candle is not closed)
      "h":"0.00020000000000000000", //Highest price reached during interval
      "l":"0.00020000000000000000", //Lowest price reached during interval
      "t":1545306480,               //Timestamp
      "v":"0"                       //Volume of trades during interval measured in liquidity
   },
   {  
      "o":"0.00020000000000000000",
      "c":"0.00020000000000000000",
      "h":"0.00020000000000000000",
      "l":"0.00020000000000000000",
      "t":1545306420,
      "v":"0"
   }

]
```
### Depth

Returns an object describing most recent state of order book on selected market. Please note that actual state of order book may be different because trades and other depth-changing events can occur
much faster then data is updated.  

```
POST /api/v1/history/depth/
```
**Parameters:**

|Name           |Type           |Mandatory |Description|Example|
| ------------- |:-------------:|:--------:|-----------|:-----:|
|market         |  STRING       |YES          |Market name consists of two assets symbols, separated by ":" (first is the symbol of asset traded and the second is liquidity asset symbol).           |  CETH:ETH    |
|limit          |INT            |YES       |Number of active orders to be returned from each side|100|




```JS
{
	"lastUpdateId": 22,               //Order-book state identifier

	"bids": [                         //An array of buy orders
		["0.00010000000000000000",      //Bid Price
		 "1.00000000000000000000",      //Amount of assets to be bought at that price
		 []                             //Ignore
	],
		["0.00000001000000000000",     
		 "1000.00000000000000000000",
		[]
		]
	],

	"asks": [                         //An array of sell orders
		["0.00020000000000000000",      //Ask Price
		 "18.29930000000000000000",     //Amount of assets to be sold at that price
		[]                              //Ignore
		],
		["0.00050000000000000000",
		 "7.79100000000000000000",
		[]
    ],
		["1.00000000000000000000",
		 "20.00000000000000000000",
		[]
		],
		["99.99900000000000000000",
		 "5.00000000000000000000",
		[]
		]
	]
}
```
