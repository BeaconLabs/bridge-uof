![Use of force data collection tool](https://raw.githubusercontent.com/bayesimpact/bridge-uof/master/app/assets/images/bayes_bridge_uof_1600px.png)

## Introduction

**Bridge-UOF** is an application developed for California police departments by San Francisco technology nonprofit [Bayes Impact](http://www.bayesimpact.org/), in collaboration with the [California Department of Justice](https://oag.ca.gov/). It is the first product released in our larger [Bridge initative](http://www.bayesimpact.org/focus/justice) to rebuild police-community relations through data.

The app helps police officers determine which incidents require reporting, fill out or upload incident information, and send the report to the state. Law enforcement agencies can manage employees and incident flow, perform analytics, and communicate with the state. The state can oversee all agencies and track reporting completion.

Its first implementation is in California under the name [URSUS](http://ursusdemo.doj.ca.gov/), as a result of [Assembly Bill 71](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201520160AB71).

Our reasons for open-sourcing Bridge-UOF are two-fold: (1) to foster transparency in government software, and (2) to be a useful model for other states and localities who wish to implement similar initiatives.

## More information on Bridge and Bayes Impact

* [Bayes Impact website](http://www.bayesimpact.org)
* [Bridge](http://www.bayesimpact.org/focus/justice) at Bayes Impact
* [Blog post](http://www.bayesimpact.org/stories/?name=bridge-uof-launch) launching this product, with much context and press links
* [Live demo of this application](http://demo-bridge-uof.bayesimpact.org)

## Installation

_Note: These instructions assume that you're running a Unix-like system._

To simplify the process of developing, testing, and deploying Bridge-UOF, we use [Docker](https://docs.docker.com/engine/installation/) containers.

1. Install [Docker](https://docs.docker.com/engine/installation/) and [docker-compose](https://docs.docker.com/compose/install/) and start the Docker daemon.

2. Set up your `local.env` configuration file. To start, just copy the provided `local.env.example` file, then tweak as needed:
  ```
  cp local.env.example local.env
  ```

3. Set up a `data/ori.csv` file. This file is a listing of police departments by their ORI codes. If you have a database of police departments handy, you can create this file to follow the format specified in `data/ori.csv.example` _(let us know if you have any questions)_. If not, simply copy over the example file:
  ```
  cp data/ori.csv.example data/ori.csv
  ```

4. Generate necessary Ruby and JS files from the ORI data.
  ```
  docker-compose build data
  docker-compose run data
  ```
  Note that this just runs `make` inside a container that has python and the appropriate libraries installed.

5. You can now start up a Docker container running the web app:
  ```
  docker-compose up --build -d web
  ```

6. Point your browser to `<IP address of your Docker container>:3000` and you should see the Bridge-UOF landing page.

### Authentication Modes

Bridge-UOF supports three different authentication modes, specified in `local.env`:

* In `DEMO` mode (used on our [public demo server](http://demo-bridge-uof.bayesimpact.org)), a new account is created whenever a user logs in without a cookie. All accounts have admin privileges and each account is in a separate, sandboxed "department".
* In `DEVISE` mode (used for testing), log-in and sign-up is handled via a form.
* In `SITEMINDER` mode (used in production), accounts are controlled via encrypted cookies generated by Siteminder authentication software.

Note that `DEVISE` mode uses a slightly different schema for users than the other two modes, so if you switch to or from `DEVISE` mode you should kill and recreate the DynamoDB container (or destroy all tables if you're running on a physical DynamoDB instance) and restart the application.

### Servers

Note that running Bridge-UOF in development mode actually starts 3 different servers _(see [`docker-compose.yml`](https://github.com/bayesimpact/ab71/blob/master/docker-compose.yml for the full details)_:

1. The Rails server (`<docker IP>:3000`). _(In production, we run this behind [nginx](https://www.nginx.com/).)_
2. The [DynamoDB](https://aws.amazon.com/dynamodb/) local server (`<docker IP>:8000`), which can be accessed with the JavaScript shell at `<docker IP>:8000/shell` (instructions on this shell [here](http://docs.aws.amazon.com/amazondynamodb/latest/gettingstartedguide/GettingStarted.JsShell.html)). _(In production this is replaced with keys to use the real Amazon-hosted DynamoDB.)_
3. The mailcatcher server (`<docker IP>:1080`), which intercepts email and displays it in a simple web interface. _(In production this is replaced with a real SMTP server, like [Amazon SES](https://aws.amazon.com/ses/) or similar.)_

## Using the app

There are two main workflows in Bridge, the incident creation workflow (performed by all users) and the review and submission workflow (performed by admins only). In demo mode, all accounts are admin accounts and so can try out both.

- To create an incident, click on the New Incident button in the top-right menu and go through the four steps (screener, general info, involved civilians, involved officers) to fill out the incident report. When the incident is ready, click "Send for review" to mark it as reviewable. You can view the status of your completed and draft incidents in your dashboard.

- To review incidents within your agency as an admin user, go to your dashboard and see if any incidents are awaiting your approval. (In demo mode, you are an agency of one, so you'll have to either fill out some incidents first or click the "Generate 10 Fake Incidents" button.) You can view each incident, edit it if necessary, and mark it as approved when ready. Then, during the state submission window (generally, the first few months of a new year), you can go to the State Submission page and submit all of your agency's approved incidents to the state. You can also see some statistics about your agency in the Analytics page.

## Testing

To run the linter:
```
rubocop
```

To run the test suite:
```
docker-compose up --build test
docker-compose up --build test-devise-only
```

We use [CircleCI](https://circleci.com/) for continuous integration (see the `circle.yml` file).

## Contributing

See `CONTRIBUTING.md`.

## License

Bridge-UOF is released under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).
