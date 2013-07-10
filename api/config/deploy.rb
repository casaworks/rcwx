set :application, "royalcanin api service"
set :repository,  "https://github.com/cuijiemmx/nora.git"

set :scm, :git

ssh_options[:forward_agent] = true
default_run_options[:pty] = true
default_run_options[:shell] = '/bin/bash'

set :user, "root"
set :deploy_to, "/var/www/royalcanin"
set :deploy_via, :remote_cache

server "geekernel.com", :app

task :restart_service do
end

after "deploy", :restart_service
