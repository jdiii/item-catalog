# Job Board
This is a job board app made to complete the "item catalog" project in Udacity's full-stack developer nanodegree.

## Installation
* 1. Install VirtualBox. You can download it here [here](https://www.virtualbox.org/wiki/Downloads)
* 2. Install Vagrant. You can download it [here](https://www.vagrantup.com/downloads)
* 3. `git clone` the full-stack nanodegree VM
* 3. `git clone` this repo to the /vagrant directory of the VM
* 4. Create a "client_secret.json" file and move it to the item-catalog directory.
	* go to the [Google Developer Console](https://console.developers.google.com), create a new app, create new OAuth client ID, and download the client_secret.json file
* 5. In the newly created directory, run `vagrant up`
* 6. SSH to the VM with the `vagrant ssh` command and `cd /vagrant/item-catalog`
* 7. run `python database_setup.py` to create the database schema
* 8. (optional) run `python fake_data.py` to populate the database with fake database
* 9. run `python project.py` to start the Flask web server
* 10. visit `http://localhost:5000/` in a browser to view the site

## Security
Login is via OAuth2 with your Google Account. A Google Account is required to create content.

Cross-site request forgery attacks are prevented with a state token for endpoints that require a valid login.

## Permissions
Anyone can view the companies and job listings for a company (/companies/) and (/companies/{{id}}/jobs). You must be logged in to create a category or post a job. You must be the creator of a company to edit or delete it, post jobs in it, or edit/delete the job postings.
