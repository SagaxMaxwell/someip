# SOMEIP

- Implement someip and someip sd protocols


# Run

- Create `.env` file

```ascii
# CONFIG
CONFIG_PATH = "./configuration/hima"


# LOG
LOG_NAME = "someip test"
LOG_PATH = "./test.log"
LOG_LEVEL = "0"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

- Create `configuration/mdc.toml` file

```toml
[address]
host = "192.168.62.1"
port = 30501
```

- Create `configuration/tbox.toml` file

```toml
[address]
host = "192.168.62.1"
port = 30501
```

- Create `configuration/vdc.toml` file

```toml
[address]
host = "192.168.62.1"
port = 30501
```

- Create packet file

```toml
[protocol]
# "someip" or "someip sd"
type = "someip"


[fields]
service_id = 0x8D03
method_id = 0x0001
protocol_version = 0x01
interface_version = 0x01
message_type = 0x01
return_code = 0x01
payload = [0x00, 0x00, 0x00, 0x01]
```

- Create virtual environment

```bash
python -m venv venv

./venv/Scripts/activate # windows

./venv/bin/activate # linux

pip install -r ./requirements.txt

python ./main.py
```
