dask_scheduler_options = [
	{
	'arg': 'host',
	'type': str,
	'options': None,
	'default': None,
	'description': "URI, IP or hostname of this server",
	},
	{
	'arg': 'port',
	'type': int,
	'options': None,
	'default': None,
	'description': "Serving port",
	},
	{
	'arg': 'interface',
	'type': str,
	'options': None,
	'default': None,
	'description': "Preferred network interface like 'eth0' or ib0",
	},
	{
	'arg': 'protocol',
	'type': str,
	'options': None,
	'default': None,
	'description': "Protocol like tcp, tls, or ucx",
	},
	{
	'arg': 'tls-ca-file',
	'type': str,
	'options': None,
	'default': None,
	'description': "CA cert(s) file for TLS (in PEM format)",
	},
	{
	'arg': 'tls-cert',
	'type': str,
	'options': None,
	'default': None,
	'description': "certificate file for TLS (in PEM format)",
	},
	{
	'arg': 'tls-key',
	'type': str,
	'options': None,
	'default': None,
	'description': "private key file for TLS (in PEM format)",
	},
	{
	'arg': 'dashboard-address',
	'type': str,
	'options': None,
	'default': '8787',
	'description': "Address on which to listen for diagnostics dashboard  [default: :8787]",
	},
	{
	'arg': ['dashboard', 'no-dashboard'],
	'type': 'binary',
	'options': None,
	'default': 'dashboard',
	'description': "Launch the Dashboard [default: --dashboard]",
	},
	{
	'arg': ['show', 'no-show'],
	'type': 'binary',
	'options': None,
	'default': 'show',
	'description': "Show web UI [default: --show]",
	},
	{
	'arg': 'dashboard-prefix',
	'type': str,
	'options': None,
	'default': None,
	'description': "Prefix for the dashboard app",
	},
	{
	'arg': 'use-xheaders',
	'type': bool,
	'options': None,
	'default': False,
	'description': "User xheaders in dashboard app for ssl ermination in header  [default: False]",
	},
	{
	'arg': 'pid-file',
	'type': str,
	'options': None,
	'default': None,
	'description': "File to write the process PID",
	},
	{
	'arg': 'scheduler-file',
	'type': str,
	'options': None,
	'default': None,
	'description': "File to write connection information. This may be a good way to share connection information if your cluster is on a shared network file system.",
	},
	{
	'arg': 'preload',
	'type': str,
	'options': None,
	'default': None,
	'description': "Module that should be loaded by the scheduler process  like 'foo.ba' or '/path/to/foo.py'.",
	},
	{
	'arg': 'idle-timeout',
	'type': str,
	'options': None,
	'default': None,
	'description': "Time of inactivity after which to kill the scheduler",
	},
]