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

Welcome to the Flute Mail Web API Reference and developer docs.

<br><br><br>

## What is Flute Mail?

Flute Mail is an email **delivery optimization platform**, a cloud service that allows you to
configure and use multiple email APIs such as 
SendGrid, Postmark, SparkPost, or any SMTP server. Just sign up for a Flute Mail account, and hook
up your API keys from different providers. Then configure your multi-provider sending environments.
For example you might have a "Transactional" environment which load-balances your email through Postmark and
SparkPost and a "Marketing" environment for your bulk email.

Why? Flute Mail supports **automatic failover redundancy**. That means if we detect provider-caused spam bounces (such as
[this](https://mailchannels.zendesk.com/hc/en-us/articles/202191674-Fixing-the-550-5-7-1-RBL-Sender-blocked-IP-or-domain-error)),
we will automatically send through another provider configured in your environment, ensuring much
better IP reliability than any single email provider can ever give you. Also, if a provider ever goes down or
experiences delays (it happens surprisingly often) we automatically route your requests to another
provider that you've configured.

For more info about how Flute Mail can improve your deliverability, reliability and email ROI, read our
[technical whitepaper](https://medium.com/@absolutelydo/problems-with-email-apis-especially-sendgrid-244d3311e4ba).

<br><br><br><br><br><br>

## What is an Environment?

An environment is a virtual email account you send requests from. Create environments on your Flute Mail dashboard.

More precisely, you must configure an environment which tells us
which providers to route your email through. For example, you might have a "Marketing" email environment,
which sends mail from noreply@mail.yourcompany.com through Mailgun, and if it detects a spam bounce,
resends the email through SparkPost. This ensures high reliability and deliverability, while also keeping
your marketing email on a different domain,
[protecting the sending reputation of your transactional email](https://postmarkapp.com/blog/separate-your-promotional-and-transactional-email-sending).

Technically speaking, a Flute Mail Environment is just 2 things:

- A from address and name (e.g. Your Name, support@yourcompany.com)
- A set of primary and redundant providers (e.g. SparkPost and Postmark)

Different sending environments allow you to organize your different kinds of email,
so that your customers can unsubscribe from your marketing email without affecting their
password resets. It also makes it easier to analyze the deliverability of different types
of email.

Configure your email sending environments on your Flute Mail [dashboard](https://dashboard.flutemail.com/).

<br><br><br><br><br><br><br><br><br>

# Authentication

API requests must be secured with an Environment-specific API key. These keys can be generated
from your Flute Mail dashboard. Note that our API keys are very long strings, sometimes 600 characters
in length. We use these long JWT tokens for performance reasons, and also to encourage better key
storage practices.

Different environments use different API keys.

An API key is NOT required for the GET /v1/email endpoint, since this endpoint can only be used to view
information about specific email ID's (which are secure UUIDs, version 4).

<br><br><br><br><br><br><br><br><br>

# POST /v1/email

`POST https://api.flutemail.com/v1/email`

Send an email.

## Example: Send a basic email

```shell

curl -X POST \
  https://api.flutemail.com/v1/email \
  -u $MY_ENV_NAME:$MY_ENV_TOKEN \
  -H 'Content-Type: application/json' \
  -d '{
	"to": [{"email": "you@example.com"}],
	"subject": "rumi says",
	"text": "listen to the song of the reed flute"
}'

```

```python
import requests

payload = {
        "to": [
                {
                        "email": 'you@example.com'
                }
        ],
        "subject": "rumi says",
        "text": "listen to the song of the reed flute"
}

response = requests.request("POST", "https://api.flutemail.com/v1/email", json=payload, auth=(MY_ENV_NAME, MY_ENV_ACCESS_TOKEN))

print(response.json())
```

```javascript
var request = require("request");

var options = { method: 'POST',
  url: 'https://api.flutemail.com/v1/email',
  headers:
   { 
     'Content-Type': 'application/json',
     'Authorization': 'Basic ' + Buffer.from(`${MY_ENV_ACCESS_TOKEN}:${MY_ENV_NAME}`).toString('base64')
  },
  body:
   { 
     to: [ { email: 'you@example.com' } ],
     subject: 'rumi says',
     text: 'listen to the song of the reed flute' },
  json: true };

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

> You should get a JSON response that looks like this:

```json
{
  "status": "success",
  "data": {
    "id": "xxxx-xxxx-xxxx"
  }
}
```


Let's send a very simple plaintext email.

Prerequisites:

- `MY_ENV_NAME`: The name of your Flute Mail environment
- `MY_ENV_ACCESS_TOKEN`: An API key for the above environment
- `you@example.com`: Where you want to send this test email

<aside class="notice">
You don't need to specify a FROM email address because this is defined in your Environment.
</aside>

## Headers

- Only JSON body will be accepted and returned by the API.
- The `Authorization` header is Basic Auth, where the username is your environment name and the password is the same environment's access token key (which is already Base64-encoded). [Get your access token here.](https://dashboard.flutemail.com/developers/api/tokens)
- If you do not specify the `Authorization` header, you can specify `environment` and `access_token` as body parameters instead.

## Body Parameters

Parameter | Default | Description
--------- | ------- | -----------
subject | required | A non-empty string for the email's subject.
to | required | An array of objects of `{"name": "", "email": ""}`. At least one must be provided.
text | `''` | A string for the text content of the email.
html | `''` | A string for the HTML content of the email.
cc | `[]` | An array of objects of `{"name": "", "email": ""}`, same as the `to` parameter. Emails will be sent to these addresses, and they will be listed under the CC header.
bcc | `[]` | An array of objects of `{"name": "", "email": ""}`, same as the `to` parameter. Emails will be sent to these addresses, but their email addresses will not be visible to other recipients.
attachments | `[]` | An array of objects of `{name, type, data}`. See below for specification.
images | `[]` | An array of objects of `{name, type, data}`. This is for inline images. See below for specification.
reply_to | `''` | A valid email address for the `Reply-To` header.
headers | `{}` | Key-value pairing for any other SMTP headers. Headers such as `Subject`, `From`, `To`, `CC` and `Reply-To` will be overwritten and will not be allowed here.
environment | `''` | The environment name from the Flute Mail dashboard. Overrides `Authorization`, if specified.
access_token | `''` | This environments access token string key. Overrides `Authorization`, if specified.

## API Limitations

- All JSON string payloads should be UTF-8 encoded.
- Each individual recipient in the `to`, `cc` and `bcc` fields cannot exceed 1024 bytes (characters) in name and email.
- At least one provider must be configured under the environment. Otherwise, the API call will fail.
- The entire payload size (all body parameters stringified, including attachments) cannot exceed 6 MB. (We do this to ensure high performance).
- All emails have open tracking enabled, and are therefore converted from plaintext to HTML. [We have reasons for doing this.](https://lwn.net/Articles/735973/)


## Response

> A response looks like this:

```json
{
  "status": "success",
  "data": {
    "id": "xxxx-xxxx-xxxx"
  }
}
```

The `id` field in the response is your Flute Mail Email ID. This is a permanent reference to this request.

### Status fields

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
413 | Payload is too large (exceeds 6 MB)
415 | Input is not in JSON format.
422 | One or more quotas exceeded
500 | Could not queue the email.

## Email Attachments

Email attachments are simply JSON objects that look like this `{"name": "filename.pdf", "type": "application/pdf", "data": "base64 encoded string"}`

Field | Type | Description
--------- | --------- | -----------
name | string, required | The filename of the attachment, including extension. Maximum length is 255 bytes. For inline images, this must be unique, and it can be referred to in your HTML content using `<img src="cid:'name'"/>`.
type | string, required | The MIME type of the attachment; e.g., `text/plain`, `image/jpeg`, `application/pdf`, etc.
data | string, required | The content of the attachment as a Base64 encoded string. The string should not contain line breaks.

<br><br><br>

## Example: Send email with attachment

TODO

<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>


<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>

# GET /v1/email/:id

`POST https://api.flutemail.com/v1/email/:id`

Send an email.

## Entities

A recipient object looks like this:
```json
      {
        "id": "1__EMAIL_ID",
        "to": "to@flutemail.com",
        "providerId": "xxxx-xxxx-xxxx",
        "providerMessageId": "xxxxxxxxxxxxx",
        "providerType": "provider",
        "requestStatus": "SUCCESS",
        "openStatus": "OPENED"
      }
```

- `id` is a concatenation of the index of the recipient, two underscores and the email ID.
- `to` is the recipient's email address (or, if the recipient's name was provided, it is in `"Name" <email>` format)
- `requestStatus` is either `SUCCESS`, `FAIL` or `UNKNOWN` (for this recipient only)
- `openStatus` is either `UNKNOWN` or `OPENED` (if the recipient's read was tracked)
- `providerType` is the successful (or last, if `requestStatus` is `FAIL`) provider that reached the recipient.
- `providerId` is the ID of the provider (see provider object below) that reached the recipient.
- `providerMessageId` is the ID returned by the provider that reached the recipient.

A provider object looks like this:

```json
      {
        "id": "xxxx-xxxx-xxxx",
        "name": "provider"
      }
```

- `id` is our internal ID which you can use to query more details about the provider in other endpoints. 
- `name` is the canonical name of the provider itself.

An environment object looks like this:

```json
    {
      "id": "xxxx-xxxx-xxxx",
      "name": "ENV-NAME",
      "category": "Transactional",
      "fromName": "Testing",
      "fromEmail": "test@flutemail.com",
      "domain": "flutemail.com",
      "envMonthlyQuota": 999,
      "envDailyQuota": 999,
      "envMonthlyQuotaUsed": 3,
      "envDailyQuotaUsed": 3,
      "createdAt": "2017-12-20T21:15:12.041Z",
      "updatedAt": "2017-12-20T21:31:36.356Z"
    }
```

These fields are the same that were used to configure the environment (in the Flute Mail dashboard).

An email body object looks like this:

```json
    {
      "to": [
        {
          "name": "Name",
          "email": "email@flutemail.com"
        }
      ],
      "subject": "email subject",
      "text": "text content",
      "html": "html content",
      "attachments": [
        {
          "name": "file.jpg",
          "type": "image/jpeg",
          "data": "image data here"
        }
      ],
      "images": [
        {
          "name": "file.jpg",
          "type": "image/jpeg",
          "data": "image data here"
        }
      ],
      "cc": [
        {
          "name": "Name",
          "email": "email@flutemail.com"
        }
      ],
      "bcc": [
        {
          "name": "Name",
          "email": "email@flutemail.com"
        }
      ],
      "headers": {
        "X-Header": "header content"
      },
      "reply_to": "",
      "from": {
        "name": "Name",
        "email": "test@flutemail.com"
      }
    }
```

All of these fields are identical to the ones received when the email object was first created (by the POST /v1/email endpoint)

## Example: Retrieve an email

```shell

curl --request GET \
  --url https://api.flutemail.com/v1/email/{EMAIL_ID} \
  --header 'content-type: application/json' \

```

```python
import requests

response = requests.request("GET", "https://api.flutemail.com/v1/email/" + EMAIL_ID)

print(response.json())
```

```javascript
var request = require("request");

var options = { method: 'GET',
  url: 'https://api.flutemail.com/v1/email/' + EMAIL_ID,
  headers:
   { 
     'Content-Type': 'application/json'
  },
  qs:
   { 
     includeBody: true,
     includeRecipients: true,
     includeEnvironment: true,
    },
  json: true };

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});

```

> You should get a JSON response that looks like this:

```json
{
  "status": "success",
  "data": {
    "id": "xxxx-xxxx-xxxx",
    "subject": "email subject",
    "from": "\"From\" <from@flutemail.com>",
    "to": "to@flutemail.com",
    "requestStatus": "SUCCESS",
    "createdAt": "2017-12-21T18:26:56.452Z",
    "updatedAt": "2017-12-21T18:26:56.452Z",
    "errors": [],

    "providersAttempted": [],
    "recipients": [],
    "envObject": {},
    "emailObject": {}
  }
}
```


Let's retrieve an email.

Prerequisites:

- `EMAIL_ID`: The ID of the email you want to retrieve.

## Query Parameters

Parameter | Default | Description
--------- | ------- | -----------
includeBody | false | If true, then `emailObject` will be added in the response body. (By default, it is not included)
includeRecipients | false | If true, then `recipients` will be added in the response body. (By default, it is not included)
includeEnvironment | false | If true, then `envObject` will be added in the response body. (By default, it is not included)

## Status fields

Status | Description
--------- | -----------
success | The email was successfully retrieved.
fail | The email was not found.
error | Internal server error.

## Response Fields

Field | Description
--------- | -----------
id | Same as the parameter that was given.
providersAttempted | An array of provider objects. These are all of the providers that were attempted when trying to send the email.
subject | Email subject.
from | Email "from" string (comma-delimited with emails).
requestStatus | Either one of `SUCCESS`, `FAIL`, `PENDING`. `SUCCESS` means that the email was successfully sent through a provider. `FAIL` means all providers were attempted.
createdAt | The timestamp of when the request to send the email was received by our servers.
updatedAt | The last timestamp of when the email was modified in any way.
errors | An array of strings. If this is non-empty, the requestStatus should be `FAIL`.
recipients | An array of recipient objects. This is only provided if `includeRecipients` is true.
envObject | The environment object. This is only provided if `includeEnvironment` is true.
emailObject | The email object. This is only provided if `includeBody` is true.