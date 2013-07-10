set :application, "royalcanin api service"
set :repository,  "https://github.com/cuijiemmx/nora.git"

set :scm, :git

ssh_options[:forward_agent] = true
default_run_options[:pty] = true
default_run_options[:shell] = '/bin/bash'

set :user, "casa"
set :deploy_to, "/var/www/royalcanin"
set :deploy_via, :remote_cache
set :use_sudo, false

server "geekernel.com", :app

#task :restart_mofashi_web do
#  with_user("cuijie", "cuijie1984") do
#    run "#{sudo} restart mofashi-web"
#  end
#end

task :restart_service do
	
end

after "deploy", :restart_service

#def with_user(new_user, new_pass, &block)
#  old_user, old_pass = user, password
#  set :user, new_user
#  set :password, new_pass
#  close_sessions
#  yield
#  set :user, old_user
#  set :password, old_pass
#  close_sessions
#end
# 
#def close_sessions
#  sessions.values.each { |session| session.close }
#  sessions.clear
#end
