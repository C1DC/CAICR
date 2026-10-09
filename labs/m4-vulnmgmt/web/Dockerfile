# Deliberately leaky web server for the M4 Nikto exercise: real Apache (so it
# emits a Server header), directory indexing left on for /backup/, and several
# "interesting" files a scanner will flag. Training target only.
FROM httpd:2.4-alpine
# Expose the server version banner (ServerTokens Full) and keep Indexes on.
RUN sed -i 's/^#\?ServerTokens.*/ServerTokens Full/' /usr/local/apache2/conf/httpd.conf || true \
    && echo "ServerTokens Full" >> /usr/local/apache2/conf/httpd.conf \
    && echo "ServerSignature On" >> /usr/local/apache2/conf/httpd.conf
COPY htdocs/ /usr/local/apache2/htdocs/
