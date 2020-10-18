upstream channels-backend {
    server {};
}

server {
    listen 80;
    server_name 0.0.0.0;
    charset utf-8;

    client_max_body_size 128M;


    location / {
        proxy_pass http://channels-backend;
    }

    location /ws {
        proxy_pass http://channels-backend;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }
}