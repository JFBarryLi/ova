FROM python:3.9

COPY ./ /ova/

ENV PIP_CONFIG_FILE pip.conf

RUN cd /ova \
  && apt-get -y update \
  && apt-get -y install -y dumb-init \
  && pip install --no-cache-dir -r requirements.txt


ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]
CMD        [ "/ova/entrypoint.sh" ]
