# Beyondify - a simplified API for Beyond's dynamic pricing 


## Table of contents

1. [Intro](#intro)
1. [API specification](#api-specification)
1. [Project guidelines](#project-guidelines)
1. [Submitting](#submitting)
1. [Evaluation](#evaluation)


## Intro

Your mission is to build a simplified API with 3 endpoints, to power [Beyond's dynamic pricing tool](http://beyondpricing.com).

The core entity of Beyond is a `Listing` - for example, an apartment on Airbnb or HomeAway.

The `Listing` entity carries some information about the property (title, market, etc) and has a `Calendar` to carry prices and availability. 

A listing's `Calendar` is just a list of dates with added information about each date - for example each date can have a different price:
```
date=2023-01-01, price=500
date=2023-01-02, price=450
```

Additionally, in Beyond's dynamic pricing, we have the concept of a "Base Price". When we predict a price for a day, we think of it as a multiple of the base price. E.g. a price of $150 for a specific day is a 1.5x multiple on the base price of $100.

In this challenge you will work with a simplified version of the listing and the calendar.

## API specification

Endpoints to implement:

1. `POST /listings` endpoint
    - Creates a listing in the system
    - Send JSON data in the body, here's an example curl command you can use:
    
      ```
      curl --location --request POST 'http://localhost:8000/listings' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "title": "Comfortable Room In Cozy Neighborhood",
          "base_price": 867,
          "market": "lisbon",
          "host_name": "John Smith",
          "currency": "USD"
      }'
      ```

      All fields are required except for `host_name`.

   - Example response: return the listing information (including its ID) in JSON format:
      ```
      {
          "id": <listing_id>,
          "title": "Comfortable Room In Cozy Neighborhood",
          "base_price": 867,
          "market": "lisbon",
          "host_name": "John Smith",
          "currency": "USD"
      }
      ```

1. `GET /listings` endpoint
    - Retrieve all listings
    - Return: a list of all listings with their stored attributes in a JSON format
   
1. `GET /listings/:id` endpoint
    - Retrieve a listing with its calendar
    - Return:
      - the listing information (including its ID) in a JSON format

      - the listing's calendar (365 days starting from today)
  
    - It must allow to return the calendar in any currency. The default being the listing's currency. This parameter must be implemented as a query parameter:
      - `currency` - optional
         - It uses the currency codes.
         - E.g.: `?currency=usd`

   - Format for dates: `YYYY-MM-DD`

   - Calendar rules:
        - For the Paris and Lisbon markets: Saturday and Sunday => 1.5x of base price
        - For the San Francisco market: Wednesday => 0.70x of base price
        - For the rest of the markets: Friday => 1.25x of base price
   - Example response:  
   ```
    "id": <listing_id>,
    "title": "Comfortable Room In Cozy Neighborhood",
    "base_price": 867,
    "currency": "USD",
    "market": "san-francisco",
    "host_name": "John Smith"
    "calendar": [
        {
            "date": "2019-01-01",
            "price": 500,
            "currency": "USD",
        },
        {
            "date": "2019-01-02",
            "price": 550,
            "currency": "USD",
        },
        ...
    ]
   ```

## Project guidelines

- You are free to use any web/API framework as long as you use Python (3.7 or greater) for your solution.

- You can containerize/package your app somehow, but you don't have to. Just make sure to provide us the exact steps we need to take to be able to run your application from scratch, and please aim for simplicity.

- How you persist data is again, up to you. You can add a database if you use containers. If you don't, you can use SQLite or something similar.

- Your solution **must use [open exchange rates][open-exchange-rates]** to get the exchange rates. The free plan is enough to complete this task.

- We've provided two files for you containing enum classes with the markets and currencies your application must support. You can modify the files/classes, delete them if you go for another approach, or just use them as is - it should be enough for this assignment.

- We use [black][black] to format the code automatically and focus on what matters instead. We encourage you to use it as well and to run it on your entire codebase: (`black .`).

- If you're unfamiliar with python, check out these useful tools:

   * [ipython][ipython] - IPython is an interactive shell for the Python programming language that offers enhanced introspection, additional shell syntax, tab completion and rich history.
   * [requests][requests] - Requests is an elegant and simple HTTP library for Python, built for human beings.   


## Submitting

1. Make sure all your changes are committed to `git` in a new branch.
1. Open a new pull request and let us know when we can start reviewing your challenge.


## Evaluation

Your work will be evaluated based on the following criteria:

 * **Cleanliness and ease of use**: Your code is easy to read, understand, and extend. You put care into properly structuring it.
 * **Best practices**: proper use of HTTP status codes, error handling, automated tests, etc. But don't go too wild, this shouldn't take too much time from you.
 * **Correctness**: The features you implement work correctly.
   There are no errors in the console. It's not easy to make your code break.
 * **Completeness**: Every feature is implemented.

:exclamation: **Important:** Your app **MUST** start successfully.


[open-exchange-rates]: https://openexchangerates.org/
[black]: https://github.com/psf/black
[ipython]: https://pypi.org/project/ipython/
[requests]: https://requests.readthedocs.io/en/master/
