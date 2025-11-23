# KrakenDB

KrakenDB is a small credential database with semi-automatic setup, bulk loading, and flexible searching.

## Usage

### Setting up the database

Use the setup script to get MySQL ready, create the database and tables, and make a limited user:

```bash
./setup.sh
```

After running it, you'll get a username and password for the limited user. Just put them into a `.env` file:

```bash
DB_USER=<username>
DB_PASSWORD=<password>
DB_HOST=localhost
```

---

### Loading credentials

You can load credentials from a file and assign them to a user. If you skip the user, it will default to `<BLANK>`:

```bash
python3 load-creds.py -f example-creds/dump-creds.txt -u userAdmin
```

---

### Searching credentials

You can search the database and optionally dump results to a file. Wildcards (`*`) work too. For example, to get all passwords ending with `123` and save them:

```bash
python3 search-creds.py -p "*123" -f "dump_new.txt"
```

You can do the same for users or descriptions:

```bash
python3 search-creds.py -u "admin*" -f "users_dump.txt"
```
