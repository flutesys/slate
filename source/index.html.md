---
title: Flute | Mail - Docs & API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - shell

toc_footers:
  - <a href='https://dashboard.flutemail.com/signup'>Sign Up</a>
  - <a href='https://dashboard.flutemail.com/login'>Login</a>


search: true
---

# What is Flute Mail?

Flute Mail is a better email API that improves the delivery and reliability of your API-based email.

It allows you to
configure and use multiple email APIs such as
SendGrid, Postmark, SparkPost, or any SMTP server,
while maintaining your own logs and stats.

We also invented **Smart Failover**.
That means if we detect provider-caused spam bounces (such as
[this](https://mailchannels.zendesk.com/hc/en-us/articles/202191674-Fixing-the-550-5-7-1-RBL-Sender-blocked-IP-or-domain-error)),
we will automatically send through other configured providers, ensuring much
better IP reliability than any single email provider can ever give you. Also, if a provider ever goes down or
experiences delays (it happens surprisingly often) we automatically route your requests to another
provider that you've configured.

For more info about how Flute Mail can improve your deliverability, reliability and email ROI, read our
[technical whitepaper](https://medium.com/@absolutelydo/problems-with-email-apis-especially-sendgrid-244d3311e4ba).

<br><br><br><br><br><br>

## What is a Virtual Flute?

A Virtual Flute is a unique email account. Each Virtual Flute comes with its own API credentials and logs.
You might have seperate flutes for different types of transactional
emails that you regularly send, such as reminders, receipts, developer notifications, etc. This makes it easier
to search, route, analyze, and improve the deliverability of your email.

A Virtual Flute has 3 key components:

*   `username`: A name used to identify and authenticate this flute
*   `providers`: A set of different providers such as AWS, SendGrid, etc., used to send email
*   `sentbox`: A searchable log of all the emails sent through this flute

Note the "From" address of the email sent is determined by the attached `providers`, not by the
flute itself. So multiple emails sent from the same flute may appear to come from different
"From" addresses. This is an intentional feature, which gives you powerful delivery-optimization
features you wouldn't be able to get with a hard-coded "From".

### Example

A small company might have 4 virtual flutes:

*   A "transactional" flute, which appears from support@yourcompany.com, used to send important
    transactional emails like reminders and password resets.
*   A "marketing" flute, which appears from noreply@mail.yourcompany.com, sent through Mailgun, and if it detects a spam bounce,
    resends the email through SparkPost. This ensures high reliability and deliverability, while also keeping
    your marketing email on a different domain,
    [protecting the sending reputation of your transactional email](https://postmarkapp.com/blog/separate-your-promotional-and-transactional-email-sending).
*   A "personal" flute, which appears from ceo@yourcompany.com, used to send a low-volume of highly critical
    messages through GMail's SMTP servers to get the benefit of GMail's high reliability and reputation.
*   A "dev" flute for testing messages and developer notifications.

### Best practices

### Guideline 1: High granularity

Generally speaking, the more flutes you have for different kinds of transactional email, the better.
There is virtually no limit to
how many flutes you can create. Sending different types of email through different flutes makes it
easier to isolate issues and follow-up on logs later. It also makes it easier to unsubscribe
users from certain types of emails, without blocking critical ones.

The most important question to ask: is this email "critical" (such as a password reset or a monthly report) or of a
"promotional" nature (like engagement notifications). These types of emails should be in seperate flutes
so that you can control the deliverability/reputation of each seperately.

### Guideline 2: Have a redundant Smart Failover provider

Always configure your flute to have a redundant "smart failover" provider, so that if emails
fail through the primary provider (for whatever reason), your emails still gets delivered.

### Guideline 3: Consider having your Smart Failover provider on a different domain

Having your redundant provider on a different domain helps to protect against random domain
reputation issues. For example you might send from yourcompany.com and yourcompanymail.com. Most
businesses have multiple domains for different purposes (testing, etc.).

### Have an expert take a look.

We're happy to assist users in designing and implementing a solid flute-y email strategy. [Contact us](https://www.flutemail.com/support) for
more info.

<br><br><br><br><br><br><br><br><br>

# Authentication

Your API endpoint is `https://$SUBDOMAIN.api.flutemail.com/v1/`. Note the subdomain is unique to each customer.

Every API request must be authenticated with a username and password. The username is your Virtual Flute
`username` and the password is an API key for that flute. These keys can be generated
from your Flute Mail dashboard.

Different flutes must use different API keys. A key may only be viewed once, so save your keys in a credentials config file, and design your code so
that it can use different username/key pairs for different types of email.

### Web API Authentication

```shell
$ curl -v -u user:password my_subdomain.api.flutemail.com
...
> Authorization: Basic dXNlcjpwYXNzd29yZA==
...
```

*   Every request must have an HTTP `Authorization` [Basic](https://majgis.github.io/2017/09/13/Create-Authorization-Basic-Header/) header, composed of the Virtual Flute `username` and API `key` password.

### SMTP API Authentication

You may also use our SMTP relay to send email through a Virtual Flute. However please note that the
web API is preferred whenever possible, as SMTP is a significantly slower protocol.

*   **Server:** smtp.flutemail.com
*   **Port:** 587 (TLS required, STARTTLS)
*   **Username:** Your Virtual Flute `username`.
*   **Password:** Any API token key for this flute.

<br><br><br><br><br><br><br><br><br>

# POST /email

`POST https://$SUBDOMAIN.api.flutemail.com/v1/email`

Send an email.

## Example: Send a basic email

```shell
export SUBDOMAIN="my_subdomain";
export VFLUTE_USERNAME="my_virtual_flute_username";
export VFLUTE_PASS="my_virtual_flute_API_key";
export EMAIL_DEST="you@example.com";

curl -X POST \
  https://$SUBDOMAIN.api.flutemail.com/v1/email \
  --user $VFLUTE_USERNAME:$VFLUTE_PASS \
  --header 'Content-Type: application/json' \
  --data '{
	"to": [{"email": "'$EMAIL_DEST'"}],
	"subject": "rumi says",
	"text": "listen to the song of the reed flute"
}'
```

> You should get a JSON response that looks like this:

```json
{
    "status": "success",
    "data": {
        "id": "email-xxxxxxxxxxxxx"
    }
}
```

Let's send a very simple plaintext email.

Variables:

*   `SUBDOMAIN`: Your subdomain
*   `VFLUTE_USERNAME`: The username of your Virtual Flute
*   `VFLUTE_PASS`: An API key for the same flute
*   `EMAIL_DEST`: Where you want to send this test email

You don't need to specify a FROM address because this is defined by your Virtual Flute's `providers`.

## Headers

*   Only an HTTP `Content-Type: application/json` will be accepted and returned by the API.
*   See `Authorization` headers above.

## Body Parameters

| Parameter   | Default  | Description                                                                                                                                                                                |
| ----------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| subject     | required | A non-empty string for the email's subject.                                                                                                                                                |
| to          | required | An array of objects of `{"name": "", "email": ""}`. At least one must be provided.                                                                                                         |
| text        | `''`     | A string for the text content of the email.                                                                                                                                                |
| html        | `''`     | A string for the HTML content of the email.                                                                                                                                                |
| cc          | `[]`     | An array of objects of `{"name": "", "email": ""}`, same as the `to` parameter. Emails will be sent to these addresses, and they will be listed under the CC header.                       |
| bcc         | `[]`     | An array of objects of `{"name": "", "email": ""}`, same as the `to` parameter. Emails will be sent to these addresses, but their email addresses will not be visible to other recipients. |
| attachments | `[]`     | An array of objects of `{name, type, data}`. See below for specification.                                                                                                                  |
| images      | `[]`     | An array of objects of `{name, type, data}`. This is for inline images. See below for specification.                                                                                       |
| reply_to    | `''`     | A valid email address for the `Reply-To` header.                                                                                                                                           |
| headers     | `{}`     | Key-value pairing for any other SMTP headers. Headers such as `Subject`, `From`, `To`, `CC` and `Reply-To` will be overwritten and will not be allowed here.                               |

## API Limitations

*   All JSON string payloads should be UTF-8 encoded.
*   Each individual recipient in the `to`, `cc` and `bcc` fields cannot exceed 1024 bytes (characters) in name and email.
*   At least one provider must be configured for the Virtual Flute. Otherwise, the API call will fail.
*   The entire payload size (all body parameters stringified, including attachments) cannot exceed 6 MB. (We do this to ensure high performance).
*   All emails have open tracking enabled, and are therefore converted from plaintext to HTML. [We have reasons for doing this.](https://lwn.net/Articles/735973/)

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

| Status  | Description                                                                                                         |
| ------- | ------------------------------------------------------------------------------------------------------------------- |
| success | The email was successfully queued and logged. The ID of the email is in `data/id`.                                  |
| fail    | One or more inputs was invalid. The status code is between 400 and 499, and the error message is in `data/message`. |
| error   | Internal server error. The status code is 500 or greater, and the error message is in `message`.                    |

Status codes can be one of the following:

| Code | Description                                                                             |
| ---- | --------------------------------------------------------------------------------------- |
| 200  | Successfully queued the email.                                                          |
| 400  | One or more inputs are badly formed.                                                    |
| 401  | Virtual Flute not found, does not have providers configured or access token is invalid. |
| 403  | Access token was not specified.                                                         |
| 413  | Payload is too large (exceeds 6 MB)                                                     |
| 415  | Input is not in JSON format.                                                            |
| 422  | One or more quotas exceeded                                                             |
| 500  | Could not queue the email.                                                              |

## Email Attachments

Email attachments are simply JSON objects that look like this `{"name": "filename.pdf", "type": "application/pdf", "data": "base64 encoded string"}`

| Field | Type             | Description                                                                                                                                                                                               |
| ----- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name  | string, required | The filename of the attachment, including extension. Maximum length is 255 bytes. For inline images, this must be unique, and it can be referred to in your HTML content using `<img src="cid:'name'"/>`. |
| type  | string, required | The MIME type of the attachment; e.g., `text/plain`, `image/jpeg`, `application/pdf`, etc.                                                                                                                |
| data  | string, required | The content of the attachment as a Base64 encoded string. The string should not contain line breaks.                                                                                                      |

<br><br><br>

# GET /email

## Example: Retrieve an email

```shell
export SUBDOMAIN="my_subdomain";
export VFLUTE_USERNAME="my_virtual_flute_username";
export VFLUTE_PASS="my_virtual_flute_API_key";
export EMAIL_ID="email-xxxxxxxxxxxx";

curl -X GET \
  https://$SUBDOMAIN.api.flutemail.com/v1/email/$EMAIL_ID \
  --user $VFLUTE_USERNAME:$VFLUTE_PASS \
  --header 'Content-Type: application/json' \
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
        "emailObject": {}
    }
}
```

Let's retrieve an email we sent earlier.

Variables:

*   `SUBDOMAIN`: Your subdomain
*   `VFLUTE_USERNAME`: The username of your Virtual Flute
*   `VFLUTE_PASS`: An API key for the same flute
*   `EMAIL_ID`: The ID of the email you wish to retrieve (provided at the time of sending)

## Query Parameters

| Parameter         | Default | Description                                                     |
| ----------------- | ------- | --------------------------------------------------------------- |
| includeBody       | false   | If true, then `emailObject` will be added in the response body. |
| includeRecipients | false   | If true, then `recipients` will be added in the response body.  |

See [Entity Types](#entity-types) for a description of the `emailObject` and `recipients` data.

## Status fields

| Status  | Description                           |
| ------- | ------------------------------------- |
| success | The email was successfully retrieved. |
| fail    | The email was not found.              |
| error   | Internal server error.                |

## Response Fields

| Field              | Description                                                                                                                                                     |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id                 | Same as the parameter that was given.                                                                                                                           |
| providersAttempted | An array of provider objects. These are all of the providers that were attempted when trying to send the email.                                                 |
| subject            | Email subject.                                                                                                                                                  |
| from               | Email "from" string (comma-delimited with emails).                                                                                                              |
| requestStatus      | Either one of `SUCCESS`, `FAIL`, `PENDING`. `SUCCESS` means that the email was successfully sent through a provider. `FAIL` means all providers were attempted. |
| createdAt          | The timestamp of when the request to send the email was received by our servers.                                                                                |
| updatedAt          | The last timestamp of when the email was modified in any way.                                                                                                   |
| errors             | An array of strings. If this is non-empty, the requestStatus should be `FAIL`.                                                                                  |
| recipients         | An array of recipient objects. This is only provided if `includeRecipients` is true.                                                                            |
| emailObject        | The email object. This is only provided if `includeBody` is true.                                                                                               |

# Entity Types

## Recipients

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

*   `id` is a concatenation of the index of the recipient, two underscores and the email ID.
*   `to` is the recipient's email address (or, if the recipient's name was provided, it is in `"Name" <email>` format)
*   `requestStatus` is either `SUCCESS`, `FAIL` or `UNKNOWN` (for this recipient only)
*   `openStatus` is either `UNKNOWN` or `OPENED` (if the recipient's read was tracked)
*   `providerType` is the successful (or last, if `requestStatus` is `FAIL`) provider that reached the recipient.
*   `providerId` is the ID of the provider that reached the recipient.
*   `providerMessageId` is the ID returned by the provider that reached the recipient.

## Emails

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
