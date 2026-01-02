# Authorization

Most methods require an API key, which can be obtained at https://steamcommunity.com/dev/apikey

Some APIs work with access tokens, if you have one you can provide it here, and it will be preferred over the webapi
key.

Here's how to get a store token:

1. Open https://store.steampowered.com/pointssummary/ajaxgetasyncconfig
2. Copy the value of webapi_token or simply paste the full JSON in

Here's how to get a community token:

1. Open https://steamcommunity.com/my/edit/info
2. Run the following script:

```js
JSON.parse(application_config.dataset.loyalty_webapi_token) (or manually copy data-loyalty_webapi_token from application_config element)
```