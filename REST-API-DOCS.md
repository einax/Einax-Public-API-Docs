# EINAX REST API DOCS

## General Information

* The base API endpoint is https://einax.com/api/v1/
* All endpoints return JSON objects or array.
* All timestamps sent to einax must be in milliseconds. 
* Timestamps returned by server can sometimes be in seconds (This will be changed in future update in favor of unification. Until then refer to this docs for defenitive clarification)
* For GET endpoints, parameters must be sent as a query string.
* For POST endpoints, the parameters must be sent as request body.
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
Example:

Using API Secret key ```ffbdab35db1d39e3b92190bfc9754034347c4b57```

on following query string:
```
timestamp=1548399459020&recv_window=5000&market=TICO%3AETH&side=sell&type=limit&quantity=0.1&price=0.1
```

should return signature:
```
98617f2c60b54c42b01b01fa0c5f48da97d879985079cca5ed6156a31c0e02d1
```
resulting request that should be sent to server will be:

```JS
{
  'timestamp': '1548399459020',
  'recv_window': 5000,
  'market': 'TICO:ETH',
  'side': 'sell',
  'type': 'limit',
  'quantity': '0.1',
  'price': '0.1',
  'signature': '98617f2c60b54c42b01b01fa0c5f48da97d879985079cca5ed6156a31c0e02d1'
}
```
Don't forget to attach request header with your X-MBX-APIKEY:
```
{'X-MBX-APIKEY': '3e2cc318b90b99be9efe903a5f18dee4162109bf'}
```
Server will respond with
```{"message":["239"]}```


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
      "t":1545256499,               //server timestamp of the trade (in seconds)
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
      "t":1545306480,               //Timestamp (in seconds)
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
		  []                            //Ignore
	],
		["0.00000001000000000000",     
		 "1000.00000000000000000000",
		 []
		]
	],

	"asks": [                         //An array of sell orders
		["0.00020000000000000000",      //Ask Price
		 "18.29930000000000000000",     //Amount of assets to be sold at that price
		 []                             //Ignore
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

## Signed API endpoints

### Create order

Creates new order

```
POST /api/v1/bots/order/create/
```

**Parameters:**

__For limit orders:__

|Name           |Type      |Mandatory |Description|Example|
| ------------- |:--------:|:--------:|-----------|:-----:|
|market         |STRING    |YES       | Market name consists of two assets symbols, separated by ":" (first is the symbol of asset traded and the second is liquidity asset symbol).  | CETH:ETH |
|side           |ENUM      |YES       |"buy" for buy orders or "sell" for sell orders| sell   |
|type           |ENUM      |YES       |"limit"- for limit orders, "market" - for market orders (future types and additional order flags will be added in later updates)|limit   |
|quantity       |FLOAT     |YES       |Amount of tokens to be bought or sold           |1.322   |
|price          |FLOAT     |YES       |Price per token           |0.00237   |
|recv_window    |INT       |NO        | Specifies that the request must be processed within a certain number of milliseconds or be rejected by the server. Default value is 5000. If between timestamp and server time is more than this value, order will not be processed.|5000   |
|timestamp      |TIMESTAMP |YES       |Your local timestamp that will be used in recv_window checks.           | 1545306615  |
|signature      |STRING    |YES   |result of ```HMAC SHA256``` where ```secretKey``` used as key and request body as value of HMAC operation   |3e2cc318b90b99be9efe903a5f18dee4162109bf   |

Please note that Limit orders by default have following properties:
* Good till canceled
* Allow taker

 This means that:
 * If valid limit order can be placed to order book it will be placed to the order book and remain in it until canceled by user or due to exchange maintenance/market closure (correlates with GDC order standard).
 * If valid limit order CAN be executed with another order it will be immediately executed as taker order.

Future updates will add more flexibility to enable/disable those options.



__For market orders:__

|Name           |Type      |Mandatory |Description|Example|
| ------------- |:--------:|:--------:|-----------|:-----:|
|market         |STRING    |YES       |Market name consists of two assets symbols, separated by ":" (first is the symbol of asset traded and the second is liquidity asset symbol).           |ZRX:ETH   |
|side           |ENUM      |YES       |"buy" for buy orders or "sell" for sell orders           | buy  |
|type           |ENUM      |YES       |"limit"- for limit orders, "market" - for market orders (future types and additional order flags will be added in later updates)           |market   |
|quantity       |FLOAT     |NO        |Amount of tokens to be bought or sold. Either quantity or limit have to be set. If quantity is set, limit must be omitted (this is subject to change in future versions)            | 1.648  |
|limit★  |FLOAT |NO        |Amount of liquidity that will be used to buy tokens (for buy orders) or liquidity threshold upon which tokens will be sold (for sell orders) |1.648*   |
|recv_window    |INT       |NO        |Specifies that the request must be processed within a certain number of milliseconds or be rejected by the server. Default value is 5000. If between timestamp and server time is more than this value, order will not be processed.          |5000   |
|timestamp      |TIMESTAMP |YES       | Your local timestamp that will be used in recv_window checks.            |1545306615   |
|signature      |STRING    |YES   |result of ```HMAC SHA256``` where ```secretKey``` used as key and request body as value of HMAC operation   |3e2cc318b90b99be9efe903a5f18dee4162109bf   |

★ limit - parameter specific to market orders. It limits order execution by the amount of liquidity used to execute given order. To better understand how to use this parameter read following examples:

```
Assuming that we are on the market ZRX:ETH and placing market buy order with limit = 1
This market order will continue buying ZRX token from orders in order book until 1 ETH worth of tokens is bought or order book become empty
```

```
Assuming that we are on the market ZRX:ETH and placing market sell order with limit = 1
This market order will continue selling ZRX to the orders in order book until total of 1 ETH is received or order book become empty
```

Note that in current version of the API, either limit or quantity shall be present to
create valid market order. If both parameters are present order will be rejected. This
logic may be changed in future updates.

**ENUM definition:**

```
side
```
A string value describing if new order will be buying or selling an asset. Side
values allowed are:
* buy
* sell

```
type
```
A string describing the type of the order. Currently two types are supported (limit and market). And
the third type - Stop will become available at a later date. Currently supported values are:
* limit
* market

limit orders MUST contain argument price and quantity. Market orders MUST omit price and have either quantity
or limit set (the other one must be omitted)

**Response:**

After sending a request to post order, response with message code will be generated.

```JS
{
"message":["239"]
}
```

Please note that Order ID is NOT returned in the response because even valid requests can sometimes be rejected at the order processing stage.
Receiving ```239``` does not mean that your order was placed in the order book or executed. In order to make sure your order is present
on the market please refer to /api/v1/bots/orders/ endpoint or connect to websocket to receive real time updates.

### Get all open orders

```
POST /api/v1/bots/orders/
```


**Parameters:**
|Name           |Type           |Mandatory |Description|Example|
| ------------- |:-------------:|:--------:|-----------|:-----:|
|recv_window    |     INT       |NO        |Specifies that the request must be processed within a certain number of milliseconds or be rejected by the server. Default value is 5000. If between timestamp and server time is more than this value, order will not be processed.|   5000    |
|timestamp      |TIMESTAMP      |YES       | Your local timestamp that will be used in recv_window checks.          | 1545306615        |
|signature      |STRING         |YES       |result of ```HMAC SHA256``` where ```secretKey``` used as key and request body as value of HMAC operation   |2c13e77bcd1ba34794a1b0bfd0955574a429bf6e0d240c0d966d5547ae181032|

### Get last transaction history
```
POST /api/v1/bots/transactions/
```

**Parameters:**
|Name           |Type           |Mandatory |Description|Example|
| ------------- |:-------------:|:--------:|-----------|:-----:|
|recv_window    |     INT       |NO        |Specifies that the request must be processed within a certain number of milliseconds or be rejected by the server. Default value is 5000. If between timestamp and server time is more than this value, order will not be processed.|   5000    |
|timestamp      |TIMESTAMP      |YES       | Your local timestamp that will be used in recv_window checks.          | 1545306615        |
|signature      |STRING         |YES       |result of ```HMAC SHA256``` where ```secretKey``` used as key and request body as value of HMAC operation   |2c13e77bcd1ba34794a1b0bfd0955574a429bf6e0d240c0d966d5547ae181032|



### Cancel order

Cancels active order or orders. Returns array of orders that was canceled.

```
POST /api/v1/bots/order/cancel/
```

**Parameters:**
|Name           |Type           |Mandatory |Description|Example|
| ------------- |:-------------:|:--------:|-----------|:-----:|
| orders_id     |ARRAY          |YES       |Array of order identifiers | ["218950689200489268249418721092036647865"]  |
||recv_window    |     INT       |NO        |Specifies that the request must be processed within a certain number of milliseconds or be rejected by the server. Default value is 5000. If between timestamp and server time is more than this value, order will not be processed.|   5000    |
|timestamp      |TIMESTAMP      |YES       | Your local timestamp that will be used in recv_window checks.          | 1545306615        |
|signature      |STRING         |YES       |result of ```HMAC SHA256``` where ```secretKey``` used as key and request body as value of HMAC operation   |2c13e77bcd1ba34794a1b0bfd0955574a429bf6e0d240c0d966d5547ae181032|   

**Response:**

```JS
[{
	"286282882923389836404110568775499338172": "Order was canceled"
}, {
	"218950689200489268249418721092036647865": "Order was canceled"
}]
```

### Account information

Returns array of user account information.

```
POST /api/v1/bots/balances/
```

**Parameters:**
|Name           |Type           |Mandatory |Description|Example|
|recv_window    |     INT       |NO        |Specifies that the request must be processed within a certain number of milliseconds or be rejected by the server. Default value is 5000. If between timestamp and server time is more than this value, order will not be processed.|   5000    |
|timestamp      |TIMESTAMP      |YES       | Your local timestamp that will be used in recv_window checks.          | 1545306615        |
|signature      |STRING         |YES       |result of ```HMAC SHA256``` where ```secretKey``` used as key and request body as value of HMAC operation   |2c13e77bcd1ba34794a1b0bfd0955574a429bf6e0d240c0d966d5547ae181032|
**Response:**
```JS
[{
	"spendable": "4.417571700000000e-5",                          //Available balance
	"locked": "5.66831000000000000e-3",                           //Locked balance
	"ticker": "ETH",                                              //Currency symbol
	"sort_order": 1500,                                           //Ignore
	"active_withdraw": true,                                      //Indicates that withdrawals are enabled for this currency
	"active_deposit": true,                                       //Indicates that deposits are enabled for this currency
	"parent__ticker": null,                                       //Indicates symbol of parent currency
	"wallets__addr": "0x382d35c3498a8429e788c4379545efd6ba657f88" //Your deposit address
}, {
	"spendable": "78.91020000000000000000",
	"locked": "11.09700000000000000000",
	"ticker": "WT",
	"sort_order": 2500,
	"active_withdraw": true,
	"active_deposit": true,
	"parent__ticker": "ETH",
	"wallets__addr": null
},  {
	"spendable": "0.49950000000000000000",
	"locked": "0.99929989000000000000",
	"ticker": "TICO",
	"sort_order": 24500,
	"active_withdraw": true,
	"active_deposit": true,
	"parent__ticker": "ETH",
	"wallets__addr": null
}]
```
