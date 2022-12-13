# test-prioritization

### For data downloading

Firstly, create the token for working with API

* Enter the https://teamcity.jetbrains.com and create the user
* Go to the settings and create your personal `TOKEN`
* Create the `.env` in the root of your project and write following:
```
TOKEN=<your_teamcity_access_token>
```
* Run `download_data.py` in `scripts/`
* To work with the downloaded data you need to unpack the `data.zip` archive in the root of the repository.
