dask_worker_options = [
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
	'arg': 'worker-port',
	'type': str,
	'options': None,
	'default': None,
	'description': "Serving computation port, defaults to random. When creating multiple workers with --nworkers, a sequential range of worker ports may be used by specifying the first and last available ports like <first-port>:<last-port>. For example, --worker-port=3000:3026 will use ports 3000, 3001, ..., 3025, 3026.",
	},
	{
	'arg': 'nanny-port',
	'type': str,
	'options': None,
	'default': None,
	'description': "Serving nanny port, defaults to random. When creating multiple nannies with --nworkers, a sequential range of nanny ports may be used by specifying the first and last available ports like <first-port>:<last-port>. For example, --nanny-port=3000:3026 will use ports 3000, 3001, ..., 3025, 3026.",
	},
	{
	'arg': 'dashboard-address',
	'type': str,
	'options': None,
	'default': None,
	'description': "Address on which to listen for diagnostics dashboard",
	},
	{
	'arg': ['dashboard', 'no-dashboard'],
	'type': 'binary',
	'options': None,
	'default': 'dashboard',
	'description': "Launch the dashboard.  [default: --dashboard]",
	},
	{
	'arg': 'listen-address',
	'type': str,
	'options': None,
	'default': None,
	'description': "The address to which the worker binds. Example: tcp://0.0.0.0:9000 or tcp://:9000 for IPv4+IPv6",
	},
	{
	'arg': 'contact-address',
	'type': str,
	'options': None,
	'default': None,
	'description': "The address the worker advertises to the scheduler for communication with it and other workers. Example: tcp://127.0.0.1:9000",
	},
	{
	'arg': 'host',
	'type': str,
	'options': None,
	'default': None,
	'description': "Serving host. Should be an ip address that is visible to the scheduler and other workers. See --listen-address and --contact-address if you need different listen and contact addresses. See --interface.",
	},
	{
	'arg': 'interface',
	'type': str,
	'options': None,
	'default': None,
	'description': "Network interface like 'eth0' or 'ib0'",
	},
	{
	'arg': 'protocol',
	'type': str,
	'options': None,
	'default': None,
	'description': "Protocol like tcp, tls, or ucx",
	},
	{
	'arg': 'nthreads',
	'type': int,
	'options': None,
	'default': None,
	'description': "Number of threads per process.",
	},
	{
	'arg': 'nworkers',
	'type': str,
	'options': None,
	'default': 'auto',
	'description': "Number of worker processes to launch. If negative, then (CPU_COUNT + 1 + nworkers) is used. Set to 'auto' to set nworkers and nthreads dynamically based on CPU_COUNT",
	},
	{
	'arg': 'name',
	'type': str,
	'options': None,
	'default': None,
	'description': "A unique name for this worker like 'worker-1'. If used with --nworkers then the process number will be appended like name-0, name-1, name-2, ...",
	},
	{
	'arg': 'memory-limit',
	'type': str,
	'options': None,
	'default': 'auto',
	'description': "Bytes of memory per process that the worker can use. This can be:\n- an integer (bytes), note 0 is a special case for no memory management.\n- a float (fraction of total system memory).\n- a string (like 5GB or 5000M).\n- 'auto' for automatically computing the memory limit.  [default: auto]",
	},
	{
	'arg': ['nanny', 'no-nanny'],
	'type': 'binary',
	'options': None,
	'default': 'nanny',
	'description': "Start workers in nanny process for management [default: --nanny]",
	},
	{
	'arg': 'pid-file',
	'type': str,
	'options': None,
	'default': None,
	'description': "File to write the process PID.",
	},
	{
	'arg': 'local-directory',
	'type': str,
	'options': None,
	'default': None,
	'description': "Directory to place worker files",
	},
	{
	'arg': 'resources',
	'type': str,
	'options': None,
	'default': None,
	'description': "Resources for task constraints like \"GPU=2 MEM=10e9\". Resources are applied separately to each worker process (only relevant when starting multiple worker processes with '--nworkers').",
	},
	{
	'arg': 'scheduler-file',
	'type': str,
	'options': None,
	'default': None,
	'description': "Filename to JSON encoded scheduler information. Use with dask-scheduler --scheduler-file",
	},
	{
	'arg': 'death-timeout',
	'type': str,
	'options': None,
	'default': None,
	'description': "Seconds to wait for a scheduler before closing",
	},
	{
	'arg': 'dashboard-prefix',
	'type': str,
	'options': None,
	'default': None,
	'description': "Prefix for the dashboard",
	},
	{
	'arg': 'lifetime',
	'type': str,
	'options': None,
	'default': None,
	'description': "If provided, shut down the worker after this duration.",
	},
	{
	'arg': 'lifetime-stagger',
	'type': str,
	'options': None,
	'default': '0',
	'description': "Random amount by which to stagger lifetime values  [default: 0 seconds]",
	},
	{
	'arg': 'worker-class',
	'type': str,
	'options': None,
	'default': 'dask.distributed.Worker',
	'description': "Worker class used to instantiate workers from.  [default: dask.distributed.Worker]",
	},
	{
	'arg': ['lifetime-restart', 'no-lifetime-restart'],
	'type': 'binary',
	'options': None,
	'default': 'no-lifetime-restart',
	'description': "Whether or not to restart the worker after the lifetime lapses. This assumes that you are using the --lifetime and --nanny  keywords  [default: no-lifetime-restart]",
	},
	{
	'arg': 'preload',
	'type': str,
	'options': None,
	'default': None,
	'description': "Module that should be loaded by each worker process like \"foo.bar\" or \"/path/to/foo.py\".",
	},
	{
	'arg': 'preload-nanny',
	'type': str,
	'options': None,
	'default': None,
	'description': "Module that should be loaded by each nanny like \"foo.bar\" or \"/path/to/foo.py\".",
	},
]