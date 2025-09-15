FROM n8nio/n8n:latest
USER root
RUN apk add --no-cache python3 py3-pip && ln -sf python3 /usr/bin/python
COPY agents/requirements.txt /opt/agents/requirements.txt
RUN pip install --no-cache-dir -r /opt/agents/requirements.txt
COPY agents /opt/agents
ENV N8N_BASIC_AUTH_ACTIVE=true \
    N8N_BASIC_AUTH_USER=admin \
    N8N_BASIC_AUTH_PASSWORD=change_me \
    N8N_HOST=0.0.0.0 \
    N8N_PORT=5678 \
    N8N_PROTOCOL=http
EXPOSE 5678
CMD ["n8n"]
