# Evil Corporation Job Board
This is an app created as part of the "Item Catalog" project in Udacity's full-stack developer nanodegree.

The app is a job board meant to connect large employers that practice such shady business practices as bribery, collusion, tax fraud, or toxic dumping with like-minded job candidates (or "henchmen", as it were).


## Installation
* 1. Install VirtualBox. You can download it here [here](https://www.virtualbox.org/wiki/Downloads)
* 2. Install Vagrant. You can download it [here](https://www.vagrantup.com/downloads)
* 3. Clone the Udacity full-stack VM to your computer using the command `git clone https://github.com/udacity/fullstack-nanodegree-vm`
* 3. From the newly created directory, run `cd /vagrant` followed by `git clone https://github.com/jdiii/item-catalog.git`
* 4. Create a Google client ID and download the client_secret json file Google provides. Store it in the `/item-catalog` directory as `client_secrets.json`
	* [There are directions for how to create a client ID here](https://developers.google.com/identity/sign-in/web/devconsole-project)
* 5. In the newly created directory, run `vagrant up`
* 6. SSH to the VM with the `vagrant ssh`
* 7. `cd /vagrant/item-catalog`
* 8. use `python database_setup.py` to create the database
* 9. (optional) use `python fake_data.py` to populate the database with fake data
* 10. Start the Flask web server with `python project.py`
* 11. visit `http://localhost:5000/` in a browser to view the site

## Security
Login is via OAuth2 with your Google Account. A Google Account is required to create content.

## Permissions
Anyone can view the companies and job listings for a company (/companies/) and (/companies/{{id}}/jobs). You must be logged in to create a category or post a job. You must be the creator of a company to edit or delete it, post jobs in it, or edit/delete the job postings.
