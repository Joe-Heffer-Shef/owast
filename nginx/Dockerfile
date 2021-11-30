FROM nginx:1.20

RUN rm /etc/nginx/conf.d/default.conf

# Generate self-signed certificate
# https://www.openssl.org/docs/manmaster/man1/openssl-req.html
# -nodes (short for no DES) means no passphrase (insecure)
RUN openssl req -x509 -nodes -days 9999 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/C=GB/ST=England/L=Sheffield/O=The University of Sheffield/CN=owast.shef.ac.uk"
