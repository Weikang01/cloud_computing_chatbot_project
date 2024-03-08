#!/bin/sh

# Replace '__API_SERVER_URL__' with the value of VITE_API_SERVER_URL in index.html
sed -i 's|__API_SERVER_URL__|'${VITE_API_SERVER_URL}'|g' /usr/share/nginx/html/index.html

# Start Nginx in the foreground
exec nginx -g 'daemon off;'
