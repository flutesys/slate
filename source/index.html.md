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

The API key must be provided in the JSON body of the request for POST requests, under the JSON key `access_token` (see examples below).

Different environments use different API keys.

An API key is NOT required for the GET /v1/email endpoint, since this endpoint can only be used to view
information about specific email ID's (which are secure UUIDs, version 4).

<br><br><br><br><br><br><br><br><br>

# POST /v1/email

`POST https://api.flutemail.com/v1/email`

Send an email.

## Example: Send a basic email

```shell

curl --request POST \
  --url https://api.flutemail.com/v1/email \
  --header 'content-type: application/json' \
  --data '{
          	"access_token": MY_ENV_ACCESS_TOKEN,
          	"environment": MY_ENV_NAME,
          	"to": [
          		{
          			"email": "you@example.com"
          		}
          	]
          	"subject": "rumi says",
          	"text": "listen to the song of the reed flute"
          }'

```

```python
import requests

headers = {
  "Authorization": MY_ENV_NAME + ":" + MY_ENV_ACCESS_TOKEN
}

payload = {
        "to": [
                {
                        "email": 'you@example.com'
                }
        ],
        "subject": "rumi says",
        "text": "listen to the song of the reed flute"
}

response = requests.request("POST", "https://api.flutemail.com/v1/email", json=payload, headers=headers)

print(response.json())
```

```javascript
var request = require("request");

var options = { method: 'POST',
  url: 'https://api.flutemail.com/v1/email',
  headers:
   { 
     'Content-Type': 'application/json'
     'Authorization': `${MY_ENV_ACCESS_TOKEN}:${MY_ENV_NAME}`
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

# GET /v1/email

Retrieve information about an email sent.

TODO