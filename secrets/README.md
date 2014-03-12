Secrets
=======

Google analytics
----------------

To make the data-fetch from Google Analytics work, a `client_secrets.json` file
containing credentials needs to be created and added to this directory.  Some
details are given in [the GA
tutorial](https://developers.google.com/analytics/solutions/articles/hello-analytics-api),
but in summary:

 - create a project for the dashboard in [the google developers
   console](https://console.developers.google.com/project)
 - For the project, go to the "APIs & auth" section on the dashboard, and
   ensure that the "Analytics API" is turned on.
 - Go to the "Credentials" section on the dashboard, and click the "Create New
   Client ID" button, to create a new OAuth 2.0 client ID.
 - Pick the "Installed Application" option, and a type of "other"
 - Download the JSON for the newly created client (using the "Download JSON" button underneath it).
 - Copy this into the `secrets` directory, and rename it to `client_secrets.json`

The generated `client_secrets.json` file should not be added to git!
