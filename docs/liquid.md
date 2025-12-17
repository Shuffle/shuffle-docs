# Liquid 
Documentation for using [Liquid formatting](https://shopify.github.io/liquid/) inside Shuffle, including examples and most-used parts.

You can learn more about liquid formatting in this Youtube video:
[![Liquid formatting video](https://img.youtube.com/vi/DA11pREbuyo/maxresdefault.jpg)](https://www.youtube.com/watch?v=DA11pREbuyo)


## Table of contents
* [Introduction](#introduction)
* [Usage in Shuffle](#usage_and_issues)
* [Most used use-cases](#most_used)
* [All available filters](#list_of_available_filters)
* [Example usage in Shuffle](#example_use_of_liquid_in_a_shuffle_workflow)

## Introduction
With the introduction of version 0.9.0 of Shuffle, we [Liquid formatting](https://shopify.github.io/liquid/) was implemented. Liquid is a templating language, allowing you to perform a lot of useful formatting operations. Common usecases involve directly writing python code or using their Liquids filters to do commong things like Regex Replace and check size. 

Shuffle uses the Python library [Liquidpy](https://github.com/pwwang/liquidpy). If you find something that should work in Liquid, but doesn't work in Shuffle, [please make an issue](https://github.com/pwwang/liquidpy/issues/new). 

## Availability
Liquid parsing is available in any field **used for execution** in Workflows, except for directly in Execution Arguments. See below.

**Works** non-exhaustive:
- App Parameters
- Conditions
- Workflow Variables
- Execution Variables

Does **NOT** work:
- Node name
- Triggers

## Usage and Issues
Liquid is available to anyone using Shuffle, with any app, in any [action parameter](/docs/workflows#passing_values) field belonging to that action. If it fails to parse, you will get a result back. 

## Shuffle's Implementation of Liquid
The main use of Liquid within Shuffle to format text. We recommend using the "Repeat back to me" action in our "Shuffle Tools" app to test, before moving it into the field of choice once you know your formatting works.

Generally in Liquid you output content using two curly braces e.g. {{ variable }} and perform logic statements by surrounding them in a curly brace percentage sign e.g. {% if statement %}. 

It is further possible to write pure python with data from Shuffle. In the case you want anything to come back to you as a result, you can print it, as seen below. 
```
{% python %}
list = ["tag1", "tag2", "tag3"]
print(",".join(list))
{% endpython %}
```

## Most used
### Get the date for tomorrow 
By adding 86400 seconds to the string "now", before adding a date format, we get the timestamp for tomorrow at this time. date: "%s" returns seconds since January 1st, 1970 (unix timestamp)

**Expression:**
```
{{ "now" | date: "%s" | plus: 86400 | date: "%Y-%m-%dT%H:%M:%S"}}
```

**Result:**
```
2024-03-08T19:59:58
```
### Create an epoch Unix timestamp 
By using the string "now", and changing the date format to seconds, it will give you the epoch timestamp.


**Expression:**
```
{{ "now" | date: "%s" }}
```

**Result:**
``` 
1643912690 
``` 

Example 2: Calculate a Time Range Using Epoch Timestamps:
You can use epoch timestamps to calculate a time range. For instance, you can use mathematical operations like subtraction or addition to find timestamps for a specific range (e.g., 10 days).
```
TimeFrom={{ "now" | date: "%s" | minus: 864000 }}&TimeTo={{ "now" | date: "%s" }}
```
**Result:**
If the current timestamp is 1643912690, the generated values would be:
```
TimeFrom=1643048690&TimeTo=1643912690
```

### Get size of an array

**Input:**
```
{{ ["this", "is", "an", "array"] | size }}
```

**Output:**
```
4
```

### Add 10 to each number in a list
First, make another node in Shuffle (e.g. Shuffle Tools 1) with the following data:
```
[{"number": 1}, {"number": 2}, {"number": 3}]
``` 

In our second node (e.g. Shuffle Tools 2), we're building out a JSON object, and want to add 1 to each item of this list, setting them to the key "new_number".
```
{"new_number": {{ $shuffle_tools_5.#.number | plus:  1 }} }
```

Want to merge the data in both of these lists? Use the "Merge lists" action, and add both lists to the 

### Dot notation
In [certain cases](https://github.com/Shuffle/Shuffle/issues/848), you may get JSON that has invalid keys. In these cases, we have workarounds using python to get the information. Here's an example based on an older issue someone had:

**PS: Dot notation no longer requires Liquid formatting and can be used the same as any other variable (January 2024)**

A node with the name "nodename" has the following value:
```
{"body": {"_source": {"kibana.alert.rule.name": "Agent Spoofing - Multiple Hosts Using Same Agent", "siem.thresholdRule", "kibana.alert.rule.uuid": "abcde12345"}}}
```

How would you get the field "._source.agent.alert.rule.name" within Shuffle? The answer is a workaround that utilizes Python, where you can work around dot notations with Python's bracket syntax.
```
{% python %}import json; print(json.loads('''$nodename.body''')["_source"]["kibana.alert.rule.name"]){% endpython %}
```

Keep in mind this is not optimal nor an intended solution in many other scenarios. Just when keys are not represented in a useful way.

### Data cleaning - newlines and quotes
As quotes can't be part of text in JSON, you may need to clean up data a whole lot before sending it on to it's destination. To do this, we use filters to remove bad data. First, make another node in Shuffle (e.g. Shuffle_Tools_1 with the following data repeated in the "Repeat back to me" action:
```
`Investigation

• Headline- Multiple inbound requests from foreign Ips related to IOCs log4shell

• Summary of Findings: Defense has observed 123 logs from the past 30 days with 25 potential malicious IP addresses linked to the Log4J exploit. Those malicious IP’s were generated from inbound requests to trusted host "123.222.154.200". Defense also noticed internal to potentially malicious external IP traffic over port 443 from IP addresses 10.20.30.40. Attached is a Excel document with the list of the raw data, source IP’s, Destination IP’s and Malicious IP’s .
```

Now make a second node (also repeat back to me), which 
```
{
"fields": {
       "project":
       {
          "key": "TTPJ"
       },
       "summary": "test",
       "description": "description": "{{ '$shuffle_tools_1' | newline_to_br | replace: '"', '' | replace: "<br />", "\\n" }}",
       "issuetype": {
          "name": "Task"
       }
   }
}
```

The JSON should now be valid, even with newlines. You can use replace and other newline replacements in the same way.


### Check if time now is between 4:30 PM and 8 AM EST
A script that returns False if the time now is NOT between the times assigned, and True if it IS between those times. 

Prints are sent to the Shuffle frontend. Needs to start with {% python %} and end with {% endpython %}

```
{% python %}
import datetime

initial_timestamp = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=5)
timedata = {
    "now": initial_timestamp.strftime("%s"),
    "comparison": "",
    "run_alert": False,
}
midnight = datetime.datetime.combine(
    datetime.date.today(),
    datetime.time(0, 0)
)
if initial_timestamp.hour < 8 and initial_timestamp.hour >= 0:
    tomorrowtime = (midnight + datetime.timedelta(hours=8)).strftime("%s")
    timedata["comparison"] = tomorrowtime
    if timedata["now"] < tomorrowtime:
        timedata["run_alert"] = True
elif initial_timestamp.hour >= 16 and initial_timestamp.hour <= 23:
    todaytime = (midnight + datetime.timedelta(hours=16, minutes=30)).strftime("%s")
    timedata["comparison"] = todaytime
    if timedata["now"] > todaytime:
        timedata["run_alert"] = True

print(timedata["run_alert"])
{% endpython %}
```


### List of available filters
* abs: Returns the absolute value of a number.

https://user-images.githubusercontent.com/31187099/152917948-865d7873-f406-45c7-98ae-37e992b3479d.mp4

https://user-images.githubusercontent.com/31187099/152917975-b78f5df6-7bc8-428d-bb40-5284c0488281.mp4

* append: Concatenates two strings and returns the concatenated value.

* as_object: Cast data as an object instead of a string. Useful with other Liquid operations and for sending/receiving data.
* at_least: Limits a number to a minimum value.

https://user-images.githubusercontent.com/31187099/152918016-1bc0c002-a10f-4129-b886-9d1c8dcb51dd.mp4

* at_most:Limits a number to a maximum value.

https://user-images.githubusercontent.com/31187099/152918035-cc6ab9bf-07b5-4d15-9adc-074148b402c9.mp4

* base64_encode: Encode a string using the Base64 encoding algorithm.
* base64_decode: Decode a Base64 encoded string.
* capitalize: Makes the first character of a string capitalized.

https://user-images.githubusercontent.com/31187099/152918039-6edd7a58-8579-4025-9f18-3f6c85443fbf.mp4

* ceil: Rounds the input up to the nearest whole number. Liquid tries to convert the input to a number before the filter is applied.

https://user-images.githubusercontent.com/31187099/152918095-8ed602a6-aa81-4b61-836d-1ff44a32c310.mp4

* compact: Removes any nil values from an array.

https://user-images.githubusercontent.com/31187099/152918109-b29bcc67-ff10-4139-8ab2-72089558ca59.mp4

https://user-images.githubusercontent.com/31187099/152918123-238cc520-90dc-4c44-bb85-795f52522cd7.mp4

* concat: Concatenates (joins together) multiple arrays. The resulting array contains all the elements from the input arrays.

https://user-images.githubusercontent.com/31187099/152918139-72a03d69-0a49-4551-b885-d1cb9cf8c99c.mp4

* csv_parse: Parses CSV-formatted information into a list. Returns with parsed objects in JSON

```
{{ "name,time\n me,now" | csv_parse }}
```

* date: Converts a timestamp into another date format. The format for this syntax is the same as strftime.
* default: Allows you to specify a fallback in case a value doesn’t exist. default will show its value if the left side is nil, false, or empty.
* divided_by: Divides a number by the specified number.
* downcase: Makes each character in a string lowercase. It has no effect on strings which are already all lowercase.
* eml_parse: Takes a string containing EML content (i.e.: RFC822) and parses out information such as to, from, subject, attachments, etc. Use with e.g.: {{ .raw_eml_string | eml_parse }}
* escape: Escapes a string by replacing characters with escape sequences (so that the string can be used in a URL, for example). It doesn’t change strings that don’t have anything to escape.
* escape_once: Escapes a string without changing existing escaped entities. It doesn’t change strings that don’t have anything to escape.
* first: Returns the first element of an array.
* floor: Rounds a number down to the nearest whole number. Liquid tries to convert the input to a number before the filter is applied.
* get: Get the value at the supplied path. e.g.: {{ .my_object | get: "my.path" }}
* hmac_sha1: Converts a string into a SHA-1 hash using a hash message authentication code (HMAC). Pass the secret key for the message as a parameter to the filter.
* hmac_sha256: Converts a string into a SHA-256 hash using a hash message authentication code (HMAC). Pass the secret key for the message as a parameter to the filter.
* hmac_sha256_base64: Converts text into a SHA-256 hash using a hash message authentication code (HMAC) and returns the data in base64. Pass the secret key for the message as a parameter to the filter.
* html_encode: Escapes HTML syntax characters in a string, e.g. "<élan>" becomes "&lt;élan&gt;".
* html_decode: Converts escaped characters in a string to HTML syntax characters, e.g. "&lt;élan&gt;" becomes "<élan>".
* in_cidr: Checks if an IP address is in a given CIDR block, e.g.: {{ .ip_address | in_cidr: '10.0.0.0/8' }}
* [join](#join): Combines the elements in an array into a single string using the argument as a separator.
* json_parse: Parse an escaped JSON string. e.g.: {{ .escaped_json_string | json_parse }}
* jsonpath: Evaluate complex JSONPaths. Includes support for wildcards and filters, e.g.: {{ .receive_event | jsonpath: '$.phoneNumbers[*].type' }}
* jwt_sign: Create a JSON Web Token from the input claim set using either RS256 (default) or HS256, e.g.: {{ .claim_set | jwt_sign: .CREDENTIAL.jwt_rsa_private_key }}, {{ .claim_set | jwt_sign: .CREDENTIAL.jwt_hmac_key, 'HS256', .extra_headers }}
* last: Returns the last element of an array.
* lstrip: Removes all whitespace (tabs, spaces, and newlines) from the beginning of a string. The filter does not affect spaces between words.
* map: Creates an array of values by extracting the values of a named property from another object.
* md5: Calculates the hex encoded md5 hash of a string.
* md5_base64: Calculates the base64 encoded md5 hash of a string.
* minus: Subtracts a number from another number.
* modulo: Returns the remainder of a division operation.
* neat_json: Format and "pretty print" an object in JSON.
* newline_to_br: Replaces every newline (\n) with an HTML line break (\<br>).
* pluralize: Output the singular or plural version of a string based on the value of a number, e.g.: {{ counter | pluralize 'item' }} outputs item or items, depending on the value of counter. For custom pluralization, you can pass a second argument, e.g. {{ 5 | pluralize 'bonus' 'bonuses'}} outputs bonuses.
* plus: Adds a number to another number.
* prepend: Adds the specified string to the beginning of another string.
* random_element: Select a random element from an array.
* regex_replace: Replaces every occurrence of a regex match in a string with the second argument, e.g. {{ "hello hello!" | regex_replace: "h\w+", "goodbye" }} outputs goodbye goodbye!.
* remove: Removes every occurrence of the specified substring from a string. Removes the elements from an array if the expression is terminated, e.g. {{ .array | remove: '<element>' }}.
* remove_first: Removes only the first occurrence of the specified substring from a string. Removes the element from an array if the expression is terminated, e.g. {{ .array | remove_first: '<element>' }}.
* replace: Replaces every occurrence of an argument in a string with the second argument.
* replace_first: Replaces only the first occurrence of the first argument in a string with the second argument.
* reverse: Reverses the order of the elements in an array. reverse cannot reverse a string.
* round: Rounds an input number to the nearest integer or, if a number is specified as an argument, to that number of decimal places.
* rstrip: Removes all whitespace (tabs, spaces, and newlines) from the right side of a string.
* sha1: Calculates the sha1 hash of a String.
* sha256: Calculates the sha256 hash of a String.
* sha512: Calculates the sha512 hash of a String.
* size: Returns the number of characters in a string or the number of elements in an array.
* slice: Returns a substring of 1 character beginning at the index specified by the argument passed in. An optional second argument specifies the length of the substring to be returned.
* sort: Sorts elements in an array by a property of an element in the array. The order of the sorted array is case-sensitive.
* sort_natural: Sorts elements in an array by a property of an element in the array.
* split: Divides an input string into an array using the argument as a separator. Example: {{ "email@domain.com" | split: '@' }}
       
```
 {{ "email@domain.com" | split: '@' }}
```
* strip: Removes all whitespace (tabs, spaces, and newlines) from both the left and right side of a string. It does not affect spaces between words.
* strip_html: Removes any HTML tags from a string.
* strip_newlines: Removes any newline characters (line breaks) from a string.
* times: Multiplies a number by another number.
* to_csv: Format an array into a CSV-formatted string.
* to_json: Format an object as JSON.
* to_snake_case: Turn input string into snake case.
* transliterate: Replaces non-ASCII characters with an ASCII approximation, or if none exists, a replacement character: “?”.
* truncate: truncate shortens a string down to the number of characters passed as a parameter. If the number of characters specified is less than the length of the string, an ellipsis (…) is appended to the string and is included in the character count.
* truncatewords: Shortens a string down to the number of words passed as the argument. If the specified number of words is less than the number of words in the string, an ellipsis (…) is appended to the string.
* type: Outputs the class of a specified object, e.g.: String or Array.
* uniq: Removes any duplicate elements in an array.
* upcase: Makes each character in a string uppercase. It has no effect on strings which are already all uppercase.
* url_decode: Decodes a string that has been encoded as a URL or by url_encode.
* url_encode: Converts any URL-unsafe characters in a string into percent-encoded characters.
* where: Selects all the elements in an array where the key has the given value. {{ .get_all_alarms.body.alarms | where:"classification","malware" }}
* zip: Creates a ZIP archive containing a given file. If the optional password parameter is present then the archive will be password protected. {{ .stream_to_zip | zip: 'optional_filename', 'optional_password' }}

## Filter Usage
Below is a list of example usage in Shuffle.

### Join
Join takes a list, and outputs the list, joined by the string specified.

Input:
```
{{ ["tag1", "tag2", "tag3"] | join: ", " }}
```

Output:
```
tag1, tag2, tag3
```

### Example use of Liquid in a Shuffle workflow 

1. Loading up a list of IP's stored in a file uploaded to Shuffle.

![Overview of the workflow](https://user-images.githubusercontent.com/31187099/147345617-d9877652-161e-48f2-94d4-97c4e92e073a.png "Overview of the workflow")

2. The list is loaded up but the whitespace starting up the list will cause parsing problems while trying to use the list.

![Image showing a list of IPs](https://user-images.githubusercontent.com/31187099/147345630-ccd6dfcc-61a0-4c48-9fb5-f14293347fe3.png "List of IPs")

3. So we employ the use of liquid formatting to clean up the list and then use it in our workflow, in our case its just a basic strip and everything is ready for use

![App actions window with applied liquid formatting in the "Items" field of the parse list function in the Shuffle Tools app](https://user-images.githubusercontent.com/31187099/147345651-608e7020-6407-40c5-b959-68583d894b67.png "App actions view")

4. We then continue an error free session with a clean list, utilizing it in our workflow

![Successfully parsed list of IP adresses](https://user-images.githubusercontent.com/31187099/147345723-05731f54-1d1a-43b8-bfe9-79ee1a7c9c3c.png "Parsed IPs")

### Example use of Liquid in a Shuffle workflow

* When trying to reverse a JSON list using using Liquid formatting we get an error due to problems with the Liquid library in use. Take this JSON as an example,

[
    {
        "Key": "2",
        "A": "B"
    },
    {
        "Key": "1",
        "A": "B"
    }
]
* If we try to reverse this array via the normal reverse function in Liquid we get the error shown below.
[{{ $shuffle_tools_1 | reverse}}] 

Error gotten: 
[<list_reverseiterator object at 0x3eb14f722f70>]

![13 01 2022_06 07 42_REC](https://user-images.githubusercontent.com/31187099/149260812-6c1a6f09-5324-4081-86d7-44d77e05da8c.png)


* Getting creative we find a work around for this by incorporating the join function in Liquid, so your call would ideally look like this. [{{ $shuffle_tools_1 | reverse | join: ',' }}]. As you can see from the below screenshot this works perfectly getting a work around for using Liquid's reverse function.

![13 01 2022_06 18 16_REC](https://user-images.githubusercontent.com/31187099/149260752-e7f37489-9095-4080-a0b7-2b04c53405a4.png)

## App Auth

You can use liquid python to define app auth parameters dynamically. For example, you can create a JWT token for authentication using the `jwt` library in python.

```
{% python %}
import jwt
def generate_token():
    key = {"customerName":"","accessID":"","description":"","accessKey":"","adminRestApiUrl":""}
    exp = time.time() + 60 * 60 
    jwt_claims = {
        "iat": time.time(), # Set issued at time to the current time.
        "exp": exp, # Set expiration time
        "aud": key["adminRestApiUrl"],  # Audience of the claim.
        "sub": key["accessID"], # Access ID from the Admin API Key.
    }

    # Use the accessKey from the Admin API key file and the RS256 algorithm to generate the JWT
    return jwt.encode(jwt_claims, key["accessKey"], algorithm="RS256")
    
print(generate_token())
{% endpython %}
```

Provide this python script in the app auth token field to generate a new JWT token for each execution. The code get executed when the app is used in a workflow. You can modify the code to fit your app auth requirements.
