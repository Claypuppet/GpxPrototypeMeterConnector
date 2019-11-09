import datetime
import re


class Measurement(object):
    _df = r"\((?P<year>\d{2})(?P<month>\d{2})(?P<day>\d{2})(?P<hour>\d{2})(?P<min>\d{2})(?P<sec>\d{2})(?P<ws>W|S)\)"

    started = False
    completed = False
    exception = False

    raw = ''
    version = None
    sn_pow = None
    sn_gas = None
    cons_1 = None
    cons_2 = None
    prod_1 = None
    prod_2 = None
    tariff = None
    gas = None

    pow_fail = None
    long_pow_fail = None
    vol_sag_1 = None
    vol_sag_2 = None
    vol_sag_3 = None
    vol_swell_1 = None
    vol_swell_2 = None
    vol_swell_3 = None

    # Power measurement
    power_moment = None
    power_consumption = None
    power_production = None

    # Gas measurement
    gas_moment = None

    def parse_line(self, line: str):
        if line.strip() == '':
            return
        self.raw += line

        try:
            if line.startswith('1-3:0.2.8'):
                self.version = int(re.search(r"\((\d+)\)", line)[1])
            elif line.startswith('0-0:1.0.0'):
                moment = re.search(self._df, line)
                self.power_moment = datetime.datetime(
                    year=2000 + int(moment.group("year")),
                    month=int(moment.group("month")),
                    day=int(moment.group("day")),
                    hour=int(moment.group("hour")) - (1 if moment.group("ws") == "S" else 0),
                    minute=int(moment.group("min")),
                    second=int(moment.group("sec")),
                ).astimezone(datetime.timezone.utc)
            elif line.startswith('0-0:96.1.1'):
                self.sn_pow = re.search(r"\((.*)\)", line)[1]
            elif line.startswith('1-0:1.8.1'):
                self.cons_1 = float(re.search(r"\((\d+\.\d+)\*kWh\)", line)[1])
            elif line.startswith('1-0:1.8.2'):
                self.cons_2 = float(re.search(r"\((\d+\.\d+)\*kWh\)", line)[1])
            elif line.startswith('1-0:2.8.1'):
                self.prod_1 = float(re.search(r"\((\d+\.\d+)\*kWh\)", line)[1])
            elif line.startswith('1-0:2.8.2'):
                self.prod_2 = float(re.search(r"\((\d+\.\d+)\*kWh\)", line)[1])
            elif line.startswith('0-0:96.14.0'):
                self.tariff = int(re.search(r"\((\d+)\)", line)[1])
            elif line.startswith('1-0:1.7.0'):
                self.power_consumption = float(re.search(r"\((\d+\.\d+)\*kW\)", line)[1])
            elif line.startswith('1-0:2.7.0'):
                self.power_production = float(re.search(r"\((\d+\.\d+)\*kW\)", line)[1])
            elif line.startswith('0-0:96.7.21'):
                self.pow_fail = int(re.search(r"\((\d+)\)", line)[1])
            elif line.startswith('0-0:96.7.9'):
                self.long_pow_fail = int(re.search(r"\((\d+)\)", line)[1])
            elif line.startswith('1-0:99:97.0'):
                # TODO: parse fail logs
                pass
            elif line.startswith('1-0:32.32.0'):
                self.vol_sag_1 = int(re.search(r"\((\d+)\)", line)[1])
            elif line.startswith('1-0:52.32.0'):
                self.vol_sag_2 = int(re.search(r"\((\d+)\)", line)[1])
            elif line.startswith('1-0:72:32.0'):
                self.vol_sag_3 = int(re.search(r"\((\d+)\)", line)[1])
            elif line.startswith('1-0:32.36.0'):
                self.vol_swell_1 = int(re.search(r"\((\d+)\)", line)[1])
            elif line.startswith('1-0:52.36.0'):
                self.vol_swell_2 = int(re.search(r"\((\d+)\)", line)[1])
            elif line.startswith('1-0:72.36.0'):
                self.vol_swell_3 = int(re.search(r"\((\d+)\)", line)[1])
            elif line.startswith('0-1:96.1.0'):
                self.sn_gas = re.search(r"\(([^)]+)\)", line)[1]
            elif line.startswith('0-1:24.2.1'):
                moment = re.search(self._df, line)
                self.gas_moment = datetime.datetime(
                    year=2000 + int(moment.group("year")),
                    month=int(moment.group("month")),
                    day=int(moment.group("day")),
                    hour=int(moment.group("hour")) + (1 if moment.group("ws") == "S" else 0),
                    minute=int(moment.group("min")),
                    second=int(moment.group("sec")),
                ).astimezone(datetime.timezone.utc)
                self.gas = float(re.search(r"\((\d+\.\d+)\*m3\)", line)[1])
            elif line.startswith('!'):
                self.completed = True
            elif line.startswith('/'):
                self.started = True
        except Exception as e:
            self.exception = True
            pass

    def is_complete(self):
        return self.started and self.completed and not self.exception

    def as_dict(self):
        return {
            'raw': self.raw.replace('\r', '').replace('\n', ';;'),
            'version': self.version,
            'sn_pow': self.sn_pow,
            'sn_gas': self.sn_gas,
            'cons_1': self.cons_1,
            'cons_2': self.cons_2,
            'prod_1': self.prod_1,
            'prod_2': self.prod_2,
            'tariff': self.tariff,
            'gas': self.gas,
            'pow_fail': self.pow_fail,
            'long_pow_fail': self.long_pow_fail,
            'vol_sag_1': self.vol_sag_1,
            'vol_sag_2': self.vol_sag_2,
            'vol_sag_3': self.vol_sag_3,
            'vol_swell_1': self.vol_swell_1,
            'vol_swell_2': self.vol_swell_2,
            'vol_swell_3': self.vol_swell_3,
            'power_moment': self.power_moment and self.power_moment.isoformat(),
            'power_consumption': self.power_consumption,
            'power_production': self.power_production,
            'gas_moment': self.gas_moment and self.gas_moment.isoformat(),
        }
