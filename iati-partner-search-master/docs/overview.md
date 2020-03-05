# IATI Tooling Overview
This document attemtps to:

* break down the broader concepts of what IATI is
* give an overview of IATI tools and the organisations that built them

The hope is that by the end of reading this, you will have a much better idea of:

* what the tool 'space' looks like for IATI
* where the gaps might exist for additional IATI tools
* what tools we can re-use in attempting to achieve our goals
* clarity on data sources, where it sits and which tools rely on which data sources
* who we could/should partner with from a technical and organisational perspective?

## So what is IATI?

At a very broad level, IATI is a standard.
A standard is an agreed upon way of communicating (For more on what a standard is, I highly recommend [this article](https://opensource.com/resources/what-are-open-standards) from [opensource.com](https://opensource.com)).
In this case, there were enough folks who agreed that they would communicate data in a particular way.
What they wanted to communicate, was aid projects - things like who was involved, what they did and how much was spent on aid.
This means that there would be a common way of communicating something like "we worked on combatting HIV AIDS in South Africa,
spending $1 million in expenses and disbursing another $1 million to X and Y organisation".

It was agreed that this data would be published as XML, but that it would also adhere to a Schema.

### Identifiers

Identifiers are a string of letters and numbers that uniquely identify something.
They are used for both activities and organisations.
Identifiers are used to link organisation within datasets and thus allow us to identify and connect disparate bits of information across documents.
Note that in some cases, identifiers might not be included in the XML data, where they are supposed to.
Publishers may instead list the organisations in the description, using only the organisations name.

There are norms that govern identifiers.
For example, if it's a UK private organisation, it will start with `GB-COH` .
Government organisations start with `GB-GOV` . DFID is `GB-GOV-1` .
Check out [companieshouse.gov.uk](https://companieshouse.gov.uk) for company references.

### What is an activity?

The [official source](http://reference.iatistandard.org/203/activity-standard/) does a great job of explaining what goes in an activity.
Some important things to note though:

* This information sits on an XML file.
* You might have a bunch of activities on a single file.
* Each activity is one and only one activity.
* There can be hierarchies between activities.
* IATI identifier would indicate relationship to other activities. E.g. Parent and child

### Versioning

There are versions of the schema or data format.
This basically means that there are certain ways that the data should be structured.
How the data should be structured over time has changed, to incorporate more fields etc.
The XML document should include what version of the schema was used, within the XML file.

Currently, the [latest data format is 2.03](http://reference.iatistandard.org/203/guidance/datastore/reference/structure-of-data/).
Note that only 5% of the data are in the version 1 format.

|     Publisher Name                                                                      |     Version 1 Activities     |
|-----------------------------------------------------------------------------------------|------------------------------|
|    Finland - Ministry of Foreign   Affairs                                              |    17067                     |
|    Switzerland - Swiss Agency for   Development and Cooperation (SDC)                   |    10382                     |
|    AidData                                                                              |    8959                      |
|    Ireland - Department of Foreign   Affairs and Trade                                  |    4266                      |
|    Japan International Cooperation   Agency (JICA)                                      |    2767                      |
|    openmindedly                                                                         |    1903                      |
|    New Zealand - Ministry of Foreign   Affairs and Trade - New Zealand Aid Programme    |    1526                      |
|    The Foundation Center                                                                |    1387                      |
|    Lithuania, Ministry of Foreign   Affairs                                             |    1077                      |
|    International Climate Initiative /   BMU - IKI Secretariat                           |    618                       |

However, dealing with versions is difficult, and may involve additional work.
It may be pragmatic to ignore the Version 1 data in some cases.

### Validation

When we ask the question 'is this information valid?', there are a number of levels to consider;
XML - does the document itself valid XML? There are plenty of tools that can do this.
IATI Schema - there are certain required elements and structure in the document, as well as how they should be added to the document.
Semantically Valid - something might be completely valid from a technical viewpoint, but doesn't helpfully communicate certain details about an activity.
For example, an organisation that was included in the description or

There are a number of tools, listed later, that help check for valid data.

### Datastore

The datastore refers to where the data (an enourmous number of XML files) are stored and how we retrieve that data (via a REST API).
IATI currently maintains a datastore, which is accessible via an API; `https://iatiregistry.org/api/3/` .
It is in the process of building a new datastore, with a new REST API.
This new datastore is being built by Zimmerman Zimmerman and is called IATI.cloud.
See [description of moving to new Datastore here](https://iatistandard.org/en/using-data/iati-tools-and-resources/iati-datastore/)
and the
[discussion around moving to the new Datastore](https://discuss.iatistandard.org/t/terms-of-reference-for-a-new-iati-datastore/1293)

### Some other notes

There's a difference between an organization and a publisher.
There are about 1000 publishers on IATI, but about 10000 organizations.

The partner might not be explictly added, and might be

    - Mentioned in the description
    - Disbursement is where the partner might be included. (This might give you a better idea of the people involved.)

## Organisations and their tools

We will now take a look at each organisation and what they have built.
Please note that there may be some overlap in terms of who built certain tools.
This document attempts to group tools by

* code ownership: which organisation does it belong to on Github?
* organisation domain: what URL, if any, can the tool be found at?

### IATI Technical Team

This is the team that build/maintain/host the old data store.
Much of the information about IATI and the tools that have been built haev already been documented on their website.

#### Data Store (v1)

See discussion above for details.
[Link to the code](https://github.com/IATI/IATI-Datastore)

#### [IATI Dashboard](http://dashboard.iatistandard.org/)

This provides a useful count as a metric for what is valuable in the data.
It's helps to demonstrate that the data from IATI is not perfect.

#### [IATI Registry Refresher](https://github.com/IATI/IATI-Registry-Refresher)

This data is pulled from `https://iatiregistry.org/api/3/` , which is indicated in the code [here](https://github.com/IATI/IATI-Registry-Refresher/blob/master/grab_urls.php#L33).

#### [IATI Public Validator](https://validator.iatistandard.org)

Provides some kind of structural validation. Doesn't do semantic validation.

### [Development Initaitives](http://www.devinit.org)

> an independent international development organisation that focuses on the role of data in driving poverty eradication and sustainable development.[Source](http://devinit.org/about/)

There are a number of individuals at Development Initaitives (DI) who are on the IATI secretariat.
This means that
Contracted out to
DI also updates the codebase

#### D-Portal

This tool is used to interrogate data, as well as search for activities related to a term.
[Link to the code](https://github.com/devinit/d-portal)

There's a UI

    demonstrate IATI, particularly an activity
    If you're trying to render XML, you can hopefully reuse that code.

In terms of integrating tools, it might be useful to link through to the D-Portal UI, in order to interrogate specific activities.

One thing that is useful is that it can give you an idea of what's going on with financials.
D-Portal does good visualization of the financial data for example.

If someone can't go in to the XML data themselves.
Organisations use D-Portal to more usefully see what there data look like at a human-readable level.
This tool gives a narrative from the raw data format.

It interprets the IDs and creates the links for you.
This is really useful, because it creates the relationships between the various organisations.

### [Open Data Services](https://opendataservices.coop/)

> We help people publish and use open data

#### [IATI COVE](https://iati.cove.opendataservices.coop/)

> CoVE is an web application to Convert, Validate and Explore data following certain open data standards - including 360Giving, Open Contracting Data Standard, IATI and the Beneficial Ownership Data Standard ([Source](https://github.com/OpenDataServices/cove/))

[Link to the Code](https://github.com/OpenDataServices/cove/)
Written in python.
Also a converter.
If you want to get data in to a usable format.
It also validates against code list.e.g. If a code wasn't on the list
Ruleset checks - e.g.your end date is before your start date.
Converts the XML to a spreadsheet. Every time there is a jump in cardinality, it creates another tab.(e.g.1 to many relationship, means creating another table)

### DFID

#### DevTracker
DevTracker is DFID's platform for publishing its data. It uses IATI data as the underlying store.
It relies on [OIPA](https://www.OIPA.nl) to pull its data.

#### [SQL to IATI](https://github.com/dfid/sql-to-iati-database)

Takes a bunch of internal databases that DFID has and pushes the data in to XML and IATI schema.

### [Publish What You Fund](http://www.publishwhatyoufund.org)

#### [data-quality-tester](http://dataqualitytester.publishwhatyoufund.org/)

> Test your IATI data against the Publish What You Fund Aid Transparency Index tests.[Source](https://github.com/pwyf/data-quality-tester)

#### [IATI Canary](https://iati-canary.herokuapp.com/)

> checks to ensure data is both available and compliant with the IATI schema.

If there’s a problem, you’ll be notified by email [Source](https://iati-canary.herokuapp.com/)

Note that this tool is opt-in.

#### [iati-decipher](https://iati-decipher.publishwhatyoufund.org/)

> Browser plugins for deciphering IATI organisation files.

[Link to the code](https://github.com/pwyf/iati-decipher). Written in Javascript.

### [Code for IATI](https://codeforiati.org/)

> Tools and guidance contributed by community members, in support of IATI infrastructure, publishers and data users.

Non-official, group of developers who have projects surrounding IATI.
list of community tools that exist outisde of the offical IATI tools.

#### [Data Dump](https://iati-data-dump.codeforiati.org/)

This hosts a zip file of data (currently ~450mb) and hosts it on Dropbox.
It relies on the [IATI Registry Refresher](https://github.com/codeforIATI/iati-data-dump) mentioned earlier and fetches data from the old data store.
[The code can be found here](https://github.com/codeforIATI/iati-data-dump).

#### [iatikit](https://iatikit.readthedocs.io/en/stable/index.html)

This is a python library that allows us to access IATI data using python (rather than say, querying raw data from the XML, CSV or JSON endpoints).

IATIkit downloads the iati data dump on dropbox and additionally downloads metadata from the API on at `https://iatiregistry.org/api/3/` .
The specifc download code can be found [here](https://github.com/codeforIATI/iatikit/blob/dev/iatikit/utils/download.py).

#### [Org-ID Guide](https://org-id.guide)

TODO: check that this is the correct organisation that builds this.
Tool for constructing an identifier.
It will show you all of the different lists that you could use to get your identifier from.
If you were working with those who might not have already published on IATI, you could direct them to the tool.

### [Zimmerman Zimmerman](https://www.zimmermanzimmerman.nl/)

> Providing data services to Governments, The UN family, The Global Fund, municipalities and non profit foundations.[Source](https://www.zimmermanzimmerman.nl/)

#### [OIPA](https://www.OIPA.nl)

> OIPA extracts and stores raw IATI XML files from the IATI Registry and makes it available as API endpoints to build data driven information solutions.

OIPA extracts all published IATI XML files from the IATI Registry and makes them available in a normalised PostgreSQL database, that you can access using a RESTful API.
This was built in order to make IATI data more usable to others.
This is what DFID uses for DevTracker and is built with Python and Django.
However, it is apparent from their repo, that OIPA is now becoming iata.cloud ...

#### [IATI Cloud](http://iati.cloud/)

[Link to the code](https://github.com/zimmerman-zimmerman/iati.cloud/).
This is becoming the new IATI datastore (as discussed earlier in the document).
From the author's understanding, it is not yet mature and most of the tools are

#### [openaidNL](https://openaid.nl/)

A visualization tool for data on the Dutch government's IATI data. Predominantly web based, using Javascript, HTML and JS.[Link to Code](https://github.com/zimmerman-zimmerman/OPENAID-IATI-PORTAL).

### Additional Code

This document is by no means extensive.
I encourage anyone reading this to continue reviewing [Github Repositories that are involved in IATI](https://github.com/search?p=1&q=IATI&type=Repositories)
and add to this document via a pull request.

## Thoughts and reflections

Where do things fit in the toolchain?

Where do we go from here?
[This is the discussion board for the IATI community](https://discuss.iatistandard.org/).
I suggest signing up to keep in the loop here.

Where is our value add for the users?

Where is the value add within the pipeline?

