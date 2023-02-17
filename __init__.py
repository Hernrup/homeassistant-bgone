__version__ = "1.0.0"

from homeassistant.helpers import device_registry as dr
import re
import logging
logger = logging.getLogger('bgone')

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "bgone"


def setup(hass, config):
    device_registry = dr.async_get(hass)

    def handle_hello(call):
        """Handle the service call."""
        event_id = 'bgone'
        dry_run = bool(call.data.get("dry_run", 0))
        filter_ = str(call.data.get("filter", ''))
        logger.info(filter_)
        logger.info(dry_run)

        p = re.compile(filter_)
        devices = {d.name: d.id for d in device_registry.devices.values() if p.match(str(d.name))}
        
        payload = {'dry_run': dry_run, 'filter': filter_, 'devices': devices}
        logger.info(payload)

        hass.bus.fire(event_id, payload)

        if dry_run:
            return

        for name, id_ in devices.items():
            logger.info(f'deleting {name}')
            device_registry.async_remove_device(id_)

    hass.services.register(DOMAIN, "fire_event", handle_hello)

    # Return boolean to indicate that initialization was successfully.
    return True
