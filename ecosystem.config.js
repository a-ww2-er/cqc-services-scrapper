module.exports = {
  apps: [{
    name: 'cqc-scraper',        // Process name
    cmd: 'python3',             // Command to run
    args: 'mainScraper.py',     // Script to execute
    cwd: '/root/cqc-services-scrapper', // Working directory
    interpreter: '',            // Not needed since using 'cmd'
    env: {
      NODE_ENV: 'development',
    },
    env_production: {
      NODE_ENV: 'production',
    },
    watch: true,               // Disable file watching
    autorestart: false,          // Auto-restart if process fails
    max_memory_restart: '1G',   // Restart if memory exceeds 1GB
    log_file: 'combined.log',   // Combined log output
    out_file: 'out.log',        // Standard output log
    error_file: 'error.log',    // Error output log
    time: true                  // Prefix logs with timestamp
  }]
};
