FROM nginx:1.13.1

RUN groupadd -r unprivileged --gid=999 \
    && useradd -m -r -g unprivileged --uid=999 unprivileged

COPY wait-for-it.sh /wait-for-it.sh
COPY entrypoint.sh /entrypoint.sh

COPY nginx.conf /etc/nginx/nginx.conf
COPY backend_proxy.conf /etc/nginx/backend_proxy.conf
COPY backend.conf /etc/nginx/conf.d/backend.conf

ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]