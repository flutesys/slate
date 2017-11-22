---
title: Flute | Mail - Docs & API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - shell
  - python
  - javascript

toc_footers:
  - <a href='https://dashboard.flutemail.com/signup'>Sign Up for an API Key</a>

search: true
---

# Introduction

Welcome to the Flute Mail API Reference and developer docs. Learn how to send email with the Flute
Mail Web API.

## What is Flute Mail?

Flute Mail is an **email provider aggregator**, a powerful cloud service that allows you to 
configure and use multiple email APIs such as 
SendGrid, Postmark, SparkPost, or any SMTP server. Just sign up for a Flute Mail account, and hook
up your API keys from different providers. Then set up your sending "Environments", which allows
you to configure which providers you wish to load-balance your requests through. For example you
might have a "Transactional" environment which sends your email through Postmark, and a "Marketing"
environment for your bulk email.

Distributing your email sending across multiple providers has many benefits: for example you 
can send all of your transactional email through Postmark for maximum deliverability (they only 
allow transactional), while sending your marketing email through SparkPost for cost-effective, 
high-volume sending. It allows you to improve your deliverability, reliability, and capacity.

Flute Mail also supports **automatic failover redundancy**. That means if SparkPost ever goes down or
experiences delays (it happens surprisingly often) we automatically route your requests to another
provider that you've configured. Also if we detect provider-caused spam bounces (such as 
[this](https://mailchannels.zendesk.com/hc/en-us/articles/202191674-Fixing-the-550-5-7-1-RBL-Sender-blocked-IP-or-domain-error)),
we will automatically send through another provider configured in your environment, ensuring much
better reliability than any single email provider can ever give you.

## What is an "Environment"?

An Flute Mail environment is a set of 3 things:

- A domain (such as support.yourcompany.com)
- A set of primary and redundant providers (e.g. SparkPost and Postmark)
- Associated settings and add-ons. 

Different sending environments allow you to organize your different kinds of email,
manage your domain reputation (ensure your marketing emails don't affect your critical emails), and
take advantage of special add-ons and integrations for certain kinds of email.

Configure your email sending environments on your Flute Mail [dashboard](https://dashboard.flutemail.com/).

<aside class="notice">
Remember — all email sent through an environment must match the FROM domain. This helps to protect your deliverability and sending reputation.
</aside>

# Authentication

Most API requests must be secured with an Environment-specific API key. These keys can be generated 
from your Flute Mail dashboard.

The API key must be provided in the JSON body of the request for POST requests, under the JSON key `access_token` (see examples below).

You must use different API keys to send email from different sending environments.

An API key is NOT required for the GET /v1/email endpoint, since this endpoint can only be used to view
information about specific email ID's (which are secure UUIDs, version 4).

# POST /v1/email

## Send a basic email

```python
import requests

r = requests.post('https://api.flutemail.com/v1/email', json={
    "access_token": MY_ENVIRONMENT_NAME_ACCESS_TOKEN,
    "subject": "test email subject",
    "text": "test email content",
    "to": [
        {
            "email": "you@example.com",
        }
    ],
    "from": {
        "name": "Flute",
        "email": "flute_test_sender@flutemail.io"
    }
})
```

# GET /v1/email

Get information about an email.

# API Limitations

# Email Attachments


<!-- This example API documentation page was created with [Slate](https://github.com/tripit/slate). Feel free to edit it and use it as a base for your own API's documentation.

# Authentication

> To authorize, use this code:

```ruby
require 'kittn'

api = Kittn::APIClient.authorize!('meowmeowmeow')
```

```python
import kittn

api = kittn.authorize('meowmeowmeow')
```

```shell
# With shell, you can just pass the correct header with each request
curl "api_endpoint_here"
  -H "Authorization: meowmeowmeow"
```

```javascript
const kittn = require('kittn');

let api = kittn.authorize('meowmeowmeow');
```

> Make sure to replace `meowmeowmeow` with your API key.

Kittn uses API keys to allow access to the API. You can register a new Kittn API key at our [developer portal](http://example.com/developers).

Kittn expects for the API key to be included in all API requests to the server in a header that looks like the following:

`Authorization: meowmeowmeow`

<aside class="notice">
You must replace <code>meowmeowmeow</code> with your personal API key.
</aside>

# Kittens

## Get All Kittens

```ruby
require 'kittn'

api = Kittn::APIClient.authorize!('meowmeowmeow')
api.kittens.get
```

```python
import kittn

api = kittn.authorize('meowmeowmeow')
api.kittens.get()
```

```shell
curl "http://example.com/api/kittens"
  -H "Authorization: meowmeowmeow"
```

```javascript
const kittn = require('kittn');

let api = kittn.authorize('meowmeowmeow');
let kittens = api.kittens.get();
```

> The above command returns JSON structured like this:

```json
[
  {
    "id": 1,
    "name": "Fluffums",
    "breed": "calico",
    "fluffiness": 6,
    "cuteness": 7
  },
  {
    "id": 2,
    "name": "Max",
    "breed": "unknown",
    "fluffiness": 5,
    "cuteness": 10
  }
]
```

This endpoint retrieves all kittens.

### HTTP Request

`GET http://example.com/api/kittens`

### Query Parameters

Parameter | Default | Description
--------- | ------- | -----------
include_cats | false | If set to true, the result will also include cats.
available | true | If set to false, the result will include kittens that have already been adopted.

<aside class="success">
Remember — a happy kitten is an authenticated kitten!
</aside>

## Get a Specific Kitten

```ruby
require 'kittn'

api = Kittn::APIClient.authorize!('meowmeowmeow')
api.kittens.get(2)
```

```python
import kittn

api = kittn.authorize('meowmeowmeow')
api.kittens.get(2)
```

```shell
curl "http://example.com/api/kittens/2"
  -H "Authorization: meowmeowmeow"
```

```javascript
const kittn = require('kittn');

let api = kittn.authorize('meowmeowmeow');
let max = api.kittens.get(2);
```

> The above command returns JSON structured like this:

```json
{
  "id": 2,
  "name": "Max",
  "breed": "unknown",
  "fluffiness": 5,
  "cuteness": 10
}
```

This endpoint retrieves a specific kitten.

<aside class="warning">Inside HTML code blocks like this one, you can't use Markdown, so use <code>&lt;code&gt;</code> blocks to denote code.</aside>

### HTTP Request

`GET http://example.com/kittens/<ID>`

### URL Parameters

Parameter | Description
--------- | -----------
ID | The ID of the kitten to retrieve

## Delete a Specific Kitten

```ruby
require 'kittn'

api = Kittn::APIClient.authorize!('meowmeowmeow')
api.kittens.delete(2)
```

```python
import kittn

api = kittn.authorize('meowmeowmeow')
api.kittens.delete(2)
```

```shell
curl "http://example.com/api/kittens/2"
  -X DELETE
  -H "Authorization: meowmeowmeow"
```

```javascript
const kittn = require('kittn');

let api = kittn.authorize('meowmeowmeow');
let max = api.kittens.delete(2);
```

> The above command returns JSON structured like this:

```json
{
  "id": 2,
  "deleted" : ":("
}
```

This endpoint retrieves a specific kitten.

### HTTP Request

`DELETE http://example.com/kittens/<ID>`

### URL Parameters

Parameter | Description
--------- | -----------
ID | The ID of the kitten to delete
 -->
