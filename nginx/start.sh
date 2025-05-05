#!/bin/sh

cat <<EOF > /etc/nginx/nginx.conf
events {}

http {
    upstream frontend {
        server frontend:${FRONTEND_PORT};
    }

    upstream backend {
        server backend:${BACKEND_PORT};
    }
    
    server {
        listen 80;
        server_name 0.0.0.0;

        # Redirige las solicitudes a /api/ al backend
        location /api/ {
            rewrite ^/api/(.*) /\$1 break;
            proxy_pass http://backend/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        # Redirige todas las demás solicitudes al frontend
        location / {
            proxy_pass http://frontend/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
            proxy_set_header X-Forwarded-Host \$host;
        }
    }
}
EOF

# Iniciar Nginx
nginx -g "daemon off;"