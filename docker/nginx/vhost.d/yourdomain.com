# server block context
location /static/ {
    alias /app/staticfiles/;
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location /uploads/ {
    alias /app/uploads/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
