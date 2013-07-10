<VirtualHost api.royalcanin.geekernel.com:80>
    ServerName api.royalcanin.geekernel.com
    WSGIDaemonProcess api threads=5
    WSGIScriptAlias / /var/www/royalcanin/current/api/api.wsgi
    <Directory /var/www/royalcanin/current/api/>
        WSGIProcessGroup api 
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>
