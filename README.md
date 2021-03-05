# hero
## Home Energy Report Online(?)

In early 2021 Duke Energy Corporation released a revamped web site for
customers to view their Home Energy Report on the web:
https://her.duke-energy.com/

Behind their web application is a powerful Apigee-powered API. With the belief
that having home energy usage data available for your own analysis can assist
with energy savings, this Python module is made available.

The hero module includes:

* hero - object constructor requiring username and password
* getDailyUsage - retrieve usage data in kilo-Watt-hours with 15 minute resolution for the provided date

## Usage

    myhero = hero("emailUsedForHERsite", "MyHERsitePassword")
    myenergy = myhero.getDailyUsage(datetime.date.today() - datetime.timedelta(days=2))

## Limitations
It can take up to 48 hours for current data to become available; hence the
example usage above pulls the data from two days ago.

## Legal
The Duke Energy names and logos and all related product and service names,
design marks and slogans are the trademarks or service marks of Duke Energy.

See LICENSE file for Copyright and usage.
