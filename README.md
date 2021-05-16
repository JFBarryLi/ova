![CI](https://github.com/JFBarryLi/ova/actions/workflows/ci.yml/badge.svg)

# Ontario Vaccine Alert

OVA is a Discord bot that polls vaccine.covaxonbooking.ca looking for vaccine booking availability.
Cancellations and reschedules are happening all the time, thus freeing up booking slots.
When this bot detects a change in availability, it sends an alert on Discord, notifying users to reschedule to an earlier date.

## Intallation

```bash
pip install git+https://github.com/JFBarryLi/ova.git
```

## Local Development

```bash
git clone https://github.com/JFBarryLi/ova.git
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

To build and run in Docker:

```bash
docker-compose up --build
```

## Usage

#### Bot commands on discord:

```bash
$help
$get_next
$pause
$start
```

Use this to retrieve next available dates locally:

```bash
./ova/available.py
```

## License
See [LICENSE](./LICENSE) for more information.
