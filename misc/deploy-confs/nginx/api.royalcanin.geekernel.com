server {
	listen       80;
	server_name api.royalcanin.geekernel.com;
	location / {  
                include uwsgi_params;
		uwsgi_pass unix:///run/uwsgi/app/api.royalcanin.geekernel.com/api.royalcanin.geekernel.com.socket;
		uwsgi_param UWSGI_CHDIR /home/casa/deploy/royalcanin/api;
		uwsgi_param UWSGI_MODULE api;
		uwsgi_param UWSGI_CALLABLE app;
        }  
}
