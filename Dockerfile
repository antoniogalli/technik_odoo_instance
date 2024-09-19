FROM odoo:13.0

USER root

RUN apt-get update
RUN apt-get install -y gettext

COPY tmpl.conf /etc/odoo
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
RUN ls -l /

USER odoo

ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["odoo"]
