module.exports = {
    apps : [{
        name: 'RetrieveCareersWorker',
        script: 'run_retrieve_careers_worker.bat',
        exec_interpreter: "none",
        exec_mode: 'fork',
        instances: 1,
        autorestart: true,
        watch: false,
        max_memory_restart: '1G',
        cwd: 'D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\',
    }]
};
