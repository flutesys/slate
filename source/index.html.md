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

```javascript
const request = require('request-promise');

request({
        method: 'POST',
        uri: 'https://api.flutemail.com/v1/email',
        headers: {},
        body: {
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
        },
        json: true,
      })
```

> The above command returns the JSON:

```json
{
  "status": "success",
  "data": {
    "id": "xxxx-xxxx-xxxx"
  }
}
```

## POST /v1/email

Send an email using the specified environment.

### HTTP Request

`POST https://api.flutemail.com/v1/email`

### Body Parameters

Parameter | Default | Description
--------- | ------- | -----------
access_token | required | The environment's access token from the Flute Mail API Tokens dashboard.
environment | required | The environment's name from the Flute Mail API Tokens dashboard. Must match the environment in `access_token`.
subject | required | A non-empty string for the email's subject.
from | required | An object `{name, email}`, where `name` is optional and `email` is required. 
to | required | An array of objects of `{name, email}`, same as the `from` parameter. At least one must be provided.
text | `''` | A string for the text content of the email.
html | `''` | A string for the HTML content of the email.
cc | `[]` | An array of objects of `{name, email}`, same as the `to` parameter. Emails will be sent to these addresses, and they will be listed under the CC header.
bcc | `[]` | An array of objects of `{name, email}`, same as the `to` parameter. Emails will be sent to these addresses, but their email addresses will not be visible to recipients.
attachments | `[]` | An array of objects of `{name, type, data}`. See below for specification.
images | `[]` | An array of objects of `{name, type, data}`. This is for inline images. See below for specification.
reply_to | `''` | A string for the `Reply-To` header.
headers | `{}` | Key-value pairing for any other headers. Headers such as `Subject`, `From`, `To`, `CC` and `Reply-To` will be overwritten and will not be allowed here.

### API Limitations

- All strings should be in the UTF-8 charset.
- All emails have open tracking enabled.
- The `from` email's domain must match the environment's sending domain configured in the Flute Mail dashboard. Otherwise, the API call will fail (see below).
- At least one provider must be configured under the environment. Otherwise, the API call will fail (see below).
- The entire payload (all body parameters stringified) cannot exceed 20 MB (i.e. 20971520 bytes). Otherwise, the API call will fail (see below).
- Each individual recipient in the `to`, `cc` and `bcc` fields cannot exceed 1024 characters in name and email. Otherwise, the API call will fail (see below).

### Response

The response will be one of the following:

Status | Description
--------- | -----------
success | The email was successfully queued and logged. The ID of the email is in `data/id`.
fail | One or more inputs was invalid. The status code is between 400 and 499, and the error message is in `data/message`.
error | Internal server error. The status code is 500 or greater, and the error message is in `message`.

Status codes can be one of the following:

Code | Description
--------- | -----------
200 | Successfully queued the email.
400 | One or more inputs are badly formed.
401 | Environment not found, does not have providers configured or access token is invalid.
403 | Access token was not specified.
413 | Payload is too large (exceeds 20 MB)
415 | Input is not in JSON format.
422 | One or more quotas exceeded
500 | Could not queue the email.

### Email Attachments

Field | Type | Description
--------- | --------- | -----------
name | string, required | The filename of the attachment, including extension. Maximum length is 255 bytes. For inline images, this must be unique, and it can be referred to in your HTML content using `<img src="cid:'name'"/>`.
type | string, required | The MIME type of the attachment; e.g., `text/plain`, `image/jpeg`, `application/pdf`, etc.
data | string, required | The content of the attachment as a Base64 encoded string. The string should not contain line breaks.

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
