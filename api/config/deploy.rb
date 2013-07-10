set :application, "royalcanin api service"
set :repository,  "git@acelinked.com:mofashi/web.git"

set :scm, :git

ssh_options[:forward_agent] = true
default_run_options[:pty] = true
default_run_options[:shell] = '/bin/bash'

set :user, "deploy"
set :deploy_to, "/data/deploy/mofashi/web"
set :deploy_via, :remote_cache
set :use_sudo, false

server "acelinked.com", :app

task :restart_mofashi_web do
  with_user("cuijie", "cuijie1984") do
    run "#{sudo} restart mofashi-web"
  end
end

after "deploy", :restart_mofashi_web

def with_user(new_user, new_pass, &block)
  old_user, old_pass = user, password
  set :user, new_user
  set :password, new_pass
  close_sessions
  yield
  set :user, old_user
  set :password, old_pass
  close_sessions
end
 
def close_sessions
  sessions.values.each { |session| session.close }
  sessions.clear
end
